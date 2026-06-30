# Google OAuth login for FreudGPT.
# Adapted from the Replit "flask_google_oauth" integration blueprint to the
# existing psycopg2 + Flask-session architecture (no SQLAlchemy / flask-login).
# Do not use flask-dance.

import json
import os
import secrets

import psycopg2
import requests
from flask import Blueprint, redirect, request, session, url_for
from oauthlib.oauth2 import WebApplicationClient

GOOGLE_CLIENT_ID = (os.environ.get("GOOGLE_OAUTH_CLIENT_ID") or "").strip()
GOOGLE_CLIENT_SECRET = (os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET") or "").strip()
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
DATABASE_URL = os.environ.get("DATABASE_URL")

google_auth = Blueprint("google_auth", __name__)


def is_configured():
    return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)


def redirect_uri_hint():
    domain = os.environ.get("REPLIT_DEV_DOMAIN", "your-app-domain")
    return f"https://{domain}/google_login/callback"


def ensure_users_table():
    """Create the users table if it does not exist.

    Matches the existing (Replit Auth style) schema so we never diverge from a
    pre-existing users table on an already-provisioned database.
    """
    if not DATABASE_URL:
        return
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid(),
                username VARCHAR UNIQUE,
                email VARCHAR UNIQUE,
                first_name VARCHAR,
                last_name VARCHAR,
                profile_image_url VARCHAR,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
            """
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[google_auth] Could not ensure users table: {e}")


def _upsert_user(email, first_name, last_name, picture):
    if not DATABASE_URL:
        return
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (email, first_name, last_name, profile_image_url, updated_at)
            VALUES (%s, %s, %s, %s, NOW())
            ON CONFLICT (email) DO UPDATE
              SET first_name = EXCLUDED.first_name,
                  last_name = EXCLUDED.last_name,
                  profile_image_url = EXCLUDED.profile_image_url,
                  updated_at = NOW()
            """,
            (email, first_name, last_name, picture),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[google_auth] Could not upsert user: {e}")


def _client():
    return WebApplicationClient(GOOGLE_CLIENT_ID)


@google_auth.route("/google_login")
def login():
    if not is_configured():
        return (
            "Google login is not configured yet. The site owner must set "
            "GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET.",
            503,
        )

    try:
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL, timeout=10).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    except Exception as e:
        print(f"[google_auth] Discovery fetch failed: {e}")
        return "Could not reach Google sign-in. Please try again.", 502

    # CSRF protection: random state stored in the session and verified on callback.
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    request_uri = _client().prepare_request_uri(
        authorization_endpoint,
        # External protocol must be https to match the whitelisted redirect URI.
        redirect_uri=request.base_url.replace("http://", "https://") + "/callback",
        scope=["openid", "email", "profile"],
        state=state,
    )
    return redirect(request_uri)


@google_auth.route("/google_login/callback")
def callback():
    if not is_configured():
        return "Google login is not configured.", 503

    # Verify CSRF state before doing anything else.
    expected_state = session.pop("oauth_state", None)
    returned_state = request.args.get("state")
    if not expected_state or returned_state != expected_state:
        return "Invalid or expired login state. Please try signing in again.", 400

    if request.args.get("error"):
        return "Google sign-in was cancelled or denied.", 400

    code = request.args.get("code")
    if not code:
        return "Missing authorization code from Google.", 400

    try:
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL, timeout=10).json()
        token_endpoint = google_provider_cfg["token_endpoint"]

        client = _client()
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url.replace("http://", "https://"),
            redirect_url=request.base_url.replace("http://", "https://"),
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
            timeout=10,
        )
        token_response.raise_for_status()

        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body, timeout=10)
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()
    except Exception as e:
        print(f"[google_auth] Token/userinfo exchange failed: {e}")
        return "Google sign-in failed. Please try again.", 502

    if not userinfo.get("email_verified"):
        return "User email not available or not verified by Google.", 400

    users_email = userinfo["email"]
    first_name = userinfo.get("given_name") or users_email.split("@")[0]
    last_name = userinfo.get("family_name")
    users_name = first_name
    picture = userinfo.get("picture")

    _upsert_user(users_email, first_name, last_name, picture)

    session["username"] = users_name
    session["email"] = users_email
    session["picture"] = picture
    session["auth_provider"] = "google"

    return redirect(url_for("index"))


@google_auth.route("/google_logout")
def logout():
    session.pop("username", None)
    session.pop("email", None)
    session.pop("picture", None)
    session.pop("auth_provider", None)
    return redirect(url_for("index"))
