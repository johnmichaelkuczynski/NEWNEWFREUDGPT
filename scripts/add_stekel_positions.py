#!/usr/bin/env python3
"""
Add Wilhelm Stekel positions to the Freud database.
Stekel was an early psychoanalyst, contemporary of Freud, and expert on OCD.
"""

import json
from datetime import datetime

stekel_positions = [
    # Nervous Anxiety States and Their Treatment (Part 1)
    {"id": "STEKEL-0001", "text": "Anxiety neurosis originates from repressed psychic conflicts rather than purely physiological causes.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Anxiety Theory"},
    {"id": "STEKEL-0002", "text": "Every anxiety has a specific ideational content that can be uncovered through analysis.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Anxiety Theory"},
    {"id": "STEKEL-0003", "text": "Anxiety serves as a signal of forbidden wishes threatening to emerge into consciousness.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Anxiety Theory"},
    {"id": "STEKEL-0004", "text": "Physical symptoms of anxiety are symbolic expressions of underlying mental conflicts.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Anxiety Theory"},
    {"id": "STEKEL-0005", "text": "The analyst must adopt an active therapeutic approach rather than passive listening.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Active Therapy"},
    {"id": "STEKEL-0006", "text": "Short-term treatment can be effective for anxiety disorders.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Active Therapy"},
    {"id": "STEKEL-0007", "text": "Dreams provide direct access to the sources of anxiety.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Dream Analysis"},
    {"id": "STEKEL-0008", "text": "Sexual conflicts are central but not exclusive causes of anxiety states.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Anxiety Theory"},
    {"id": "STEKEL-0009", "text": "The patient's resistance itself contains diagnostic information.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Resistance"},
    {"id": "STEKEL-0010", "text": "Cure requires bringing unconscious material to conscious awareness.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Therapeutic Goals"},
    
    # The Language of Dreams (Part 1)
    {"id": "STEKEL-0011", "text": "Dreams use a universal symbolic language comprehensible across cultures.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0012", "text": "Symbols have relatively fixed meanings that can be catalogued.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0013", "text": "Every dream contains both manifest and latent content.", "work": "The Language of Dreams", "subcategory": "Dream Structure"},
    {"id": "STEKEL-0014", "text": "Dreams represent wish-fulfillments, including death wishes.", "work": "The Language of Dreams", "subcategory": "Dream Theory"},
    {"id": "STEKEL-0015", "text": "Bipolar symbolism allows single symbols to represent opposites.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0016", "text": "The dreamer's associations alone are insufficient for interpretation.", "work": "The Language of Dreams", "subcategory": "Dream Interpretation"},
    {"id": "STEKEL-0017", "text": "Analyst expertise in symbolism is necessary for proper dream analysis.", "work": "The Language of Dreams", "subcategory": "Dream Interpretation"},
    {"id": "STEKEL-0018", "text": "Dreams often contain prophetic elements regarding the dreamer's future actions.", "work": "The Language of Dreams", "subcategory": "Dream Theory"},
    {"id": "STEKEL-0019", "text": "Recurring dreams indicate unresolved central conflicts.", "work": "The Language of Dreams", "subcategory": "Dream Analysis"},
    {"id": "STEKEL-0020", "text": "Dream interpretation should be completed within a single session when possible.", "work": "The Language of Dreams", "subcategory": "Dream Technique"},
    
    # Auto-Erotism (Part 1)
    {"id": "STEKEL-0021", "text": "Masturbation guilt produces more pathology than the act itself.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    {"id": "STEKEL-0022", "text": "Fantasies accompanying masturbation reveal core neurotic conflicts.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    {"id": "STEKEL-0023", "text": "Excessive masturbation can indicate deeper psychological disturbance.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    {"id": "STEKEL-0024", "text": "Cultural attitudes toward masturbation create unnecessary suffering.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    {"id": "STEKEL-0025", "text": "The content of masturbatory fantasy is diagnostically significant.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    {"id": "STEKEL-0026", "text": "Masturbation serves as substitute gratification for unavailable objects.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    {"id": "STEKEL-0027", "text": "Compulsive masturbation differs qualitatively from normal self-stimulation.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    {"id": "STEKEL-0028", "text": "Physical consequences attributed to masturbation are largely mythological.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    {"id": "STEKEL-0029", "text": "Treatment should address the underlying conflicts, not the behavior itself.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Treatment"},
    {"id": "STEKEL-0030", "text": "Shame and secrecy intensify the pathogenic effects of masturbation guilt.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbation"},
    
    # Frigidity in Woman (Part 1)
    {"id": "STEKEL-0031", "text": "Female frigidity is primarily psychogenic rather than constitutional.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0032", "text": "Unconscious hostility toward men commonly underlies frigidity.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0033", "text": "Early sexual trauma contributes to later sexual inhibition.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0034", "text": "Frigidity often represents unconscious revenge against the partner.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0035", "text": "Women's sexuality is as intense as men's when inhibitions are removed.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0036", "text": "Clitoral fixation can prevent vaginal responsiveness.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0037", "text": "Marital unhappiness frequently manifests as sexual dysfunction.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0038", "text": "Frigidity may serve defensive purposes against feared pregnancy.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0039", "text": "Identification with a cold or punitive mother contributes to frigidity.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0040", "text": "Successful treatment requires uncovering specific unconscious determinants.", "work": "Frigidity in Woman", "subcategory": "Treatment"},
    
    # Sexual Aberrations - Fetishism (Part 1)
    {"id": "STEKEL-0041", "text": "Fetishism represents displacement of sexual interest from whole object to part.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0042", "text": "The fetish object typically has symbolic connection to early experiences.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0043", "text": "Fetishism serves to manage castration anxiety.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0044", "text": "The fetish allows sexual functioning that would otherwise be impossible.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0045", "text": "Fetishistic tendencies exist on a continuum in normal sexuality.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0046", "text": "Specific fetish choices are determined by individual history.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0047", "text": "Fetishism can represent fixation at a pre-genital developmental stage.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0048", "text": "The fetish provides reassurance against unconscious fears.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0049", "text": "Female fetishism exists but manifests differently than male fetishism.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0050", "text": "Treatment requires uncovering the original trauma or fixation point.", "work": "Sexual Aberrations", "subcategory": "Treatment"},
    
    # Sadism and Masochism (Part 1)
    {"id": "STEKEL-0051", "text": "Sadism and masochism are fundamentally interrelated phenomena.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    {"id": "STEKEL-0052", "text": "Every sadist harbors masochistic tendencies and vice versa.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    {"id": "STEKEL-0053", "text": "Sadistic and masochistic tendencies exist in attenuated form in all individuals.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    {"id": "STEKEL-0054", "text": "Sadism represents aggression eroticized and directed outward.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    {"id": "STEKEL-0055", "text": "Masochism involves aggression turned against the self.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    {"id": "STEKEL-0056", "text": "Guilt feelings play a central role in masochistic formations.", "work": "Sadism and Masochism", "subcategory": "Masochism"},
    {"id": "STEKEL-0057", "text": "Early experiences of pain and pleasure becoming linked create predisposition to sadomasochism.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    {"id": "STEKEL-0058", "text": "Power dynamics in sadomasochistic conditions reflect early parent-child relationships.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    {"id": "STEKEL-0059", "text": "Moral masochism manifests in self-defeating life patterns.", "work": "Sadism and Masochism", "subcategory": "Masochism"},
    {"id": "STEKEL-0060", "text": "Cultural factors influence the expression of sadomasochistic tendencies.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    
    # Disorders of the Instincts and the Emotions (Part 1)
    {"id": "STEKEL-0061", "text": "Instinctual life follows lawful patterns that can be scientifically studied.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Instinct Theory"},
    {"id": "STEKEL-0062", "text": "Emotional disorders represent disturbances in instinctual equilibrium.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Instinct Theory"},
    {"id": "STEKEL-0063", "text": "Repressed instincts find substitute outlets in symptoms.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Symptom Formation"},
    {"id": "STEKEL-0064", "text": "Ambivalence characterizes all emotional attachments.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Ambivalence"},
    {"id": "STEKEL-0065", "text": "Hatred and love coexist toward the same objects.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Ambivalence"},
    {"id": "STEKEL-0066", "text": "Instinctual conflicts underlie all psychoneuroses.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Neurosis Theory"},
    {"id": "STEKEL-0067", "text": "Each individual has characteristic patterns of emotional response.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Character"},
    {"id": "STEKEL-0068", "text": "Affect can become detached from its original ideational content.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Affect Theory"},
    {"id": "STEKEL-0069", "text": "Emotional disorders are treatable through psychoanalytic methods.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Treatment"},
    {"id": "STEKEL-0070", "text": "The transformation of instincts follows predictable pathways.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Instinct Theory"},
    
    # Compulsion and Doubt (Part 1)
    {"id": "STEKEL-0071", "text": "Obsessional neurosis involves the return of repressed aggressive wishes.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0072", "text": "Doubt represents paralysis between opposing impulses.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0073", "text": "Compulsive rituals serve to undo or prevent imagined harm.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0074", "text": "Magical thinking underlies obsessional symptoms.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0075", "text": "The obsessional's conscientiousness masks unconscious hostility.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0076", "text": "Isolation of affect is a primary defense in obsessional neurosis.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0077", "text": "Obsessional symptoms often relate to death wishes toward loved ones.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0078", "text": "Reaction formation transforms hatred into excessive concern.", "work": "Compulsion and Doubt", "subcategory": "Defense Mechanisms"},
    {"id": "STEKEL-0079", "text": "The obsessional character involves over-control and rigidity.", "work": "Compulsion and Doubt", "subcategory": "Character"},
    {"id": "STEKEL-0080", "text": "Treatment must address both the symptom and the underlying character structure.", "work": "Compulsion and Doubt", "subcategory": "Treatment"},
    
    # Technique of Analytical Psychotherapy (Part 1)
    {"id": "STEKEL-0081", "text": "Active intervention by the analyst accelerates therapeutic progress.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Active Therapy"},
    {"id": "STEKEL-0082", "text": "Treatment should be time-limited rather than open-ended.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Treatment Frame"},
    {"id": "STEKEL-0083", "text": "The analyst should interpret directly rather than waiting for patient insight.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Interpretation"},
    {"id": "STEKEL-0084", "text": "Dream interpretation should be central to every analytic session.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Dream Analysis"},
    {"id": "STEKEL-0085", "text": "Resistance should be confronted promptly and directly.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Resistance"},
    {"id": "STEKEL-0086", "text": "The analyst's intuition is a valid therapeutic instrument.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Technique"},
    {"id": "STEKEL-0087", "text": "Therapeutic flexibility should replace rigid adherence to rules.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Technique"},
    {"id": "STEKEL-0088", "text": "The initial sessions are crucial for establishing therapeutic direction.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Treatment Frame"},
    {"id": "STEKEL-0089", "text": "Termination should occur when central conflicts are resolved.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Termination"},
    {"id": "STEKEL-0090", "text": "The analyst must remain emotionally engaged while maintaining objectivity.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Countertransference"},
    
    # Impotence in the Male (Part 1)
    {"id": "STEKEL-0091", "text": "Male impotence is predominantly psychogenic in origin.", "work": "Impotence in the Male", "subcategory": "Male Sexuality"},
    {"id": "STEKEL-0092", "text": "Castration anxiety is the most common unconscious cause of male impotence.", "work": "Impotence in the Male", "subcategory": "Castration Anxiety"},
    {"id": "STEKEL-0093", "text": "Impotence often reflects hostility toward women.", "work": "Impotence in the Male", "subcategory": "Male Sexuality"},
    {"id": "STEKEL-0094", "text": "Mother fixation contributes to inability to function with other women.", "work": "Impotence in the Male", "subcategory": "Oedipal Complex"},
    {"id": "STEKEL-0095", "text": "Performance anxiety creates self-fulfilling prophecy of failure.", "work": "Impotence in the Male", "subcategory": "Anxiety"},
    {"id": "STEKEL-0096", "text": "Impotence may serve unconscious purposes such as punishing the partner.", "work": "Impotence in the Male", "subcategory": "Male Sexuality"},
    {"id": "STEKEL-0097", "text": "Homosexual tendencies may manifest as heterosexual impotence.", "work": "Impotence in the Male", "subcategory": "Homosexuality"},
    {"id": "STEKEL-0098", "text": "Guilt over sexuality contributes to erectile dysfunction.", "work": "Impotence in the Male", "subcategory": "Guilt"},
    {"id": "STEKEL-0099", "text": "The specific circumstances of impotence reveal its meaning.", "work": "Impotence in the Male", "subcategory": "Diagnosis"},
    {"id": "STEKEL-0100", "text": "Psychoanalytic treatment can resolve most cases of psychogenic impotence.", "work": "Impotence in the Male", "subcategory": "Treatment"},
    
    # Bi-Sexual Love (Part 1)
    {"id": "STEKEL-0101", "text": "Constitutional bisexuality is universal in human beings.", "work": "Bi-Sexual Love", "subcategory": "Bisexuality"},
    {"id": "STEKEL-0102", "text": "Exclusive heterosexuality or homosexuality represents developmental outcome.", "work": "Bi-Sexual Love", "subcategory": "Sexual Development"},
    {"id": "STEKEL-0103", "text": "Homosexual components exist in all heterosexual relationships.", "work": "Bi-Sexual Love", "subcategory": "Bisexuality"},
    {"id": "STEKEL-0104", "text": "Same-sex friendships contain sublimated homosexual elements.", "work": "Bi-Sexual Love", "subcategory": "Sublimation"},
    {"id": "STEKEL-0105", "text": "Bisexual conflicts contribute to many neurotic symptoms.", "work": "Bi-Sexual Love", "subcategory": "Bisexuality"},
    {"id": "STEKEL-0106", "text": "Cultural forces shape the expression of bisexual tendencies.", "work": "Bi-Sexual Love", "subcategory": "Culture"},
    {"id": "STEKEL-0107", "text": "Jealousy often contains unconscious homosexual components.", "work": "Bi-Sexual Love", "subcategory": "Jealousy"},
    {"id": "STEKEL-0108", "text": "Identification with the opposite sex parent influences sexual orientation.", "work": "Bi-Sexual Love", "subcategory": "Identification"},
    {"id": "STEKEL-0109", "text": "Latent homosexuality may manifest in various disguised forms.", "work": "Bi-Sexual Love", "subcategory": "Homosexuality"},
    {"id": "STEKEL-0110", "text": "Recognition of bisexual nature can be therapeutically liberating.", "work": "Bi-Sexual Love", "subcategory": "Treatment"},
    
    # Peculiarities of Behavior (Part 1)
    {"id": "STEKEL-0111", "text": "Wandering mania represents flight from intolerable inner conflicts.", "work": "Peculiarities of Behavior", "subcategory": "Impulse Disorders"},
    {"id": "STEKEL-0112", "text": "Dipsomania involves periodic breakthrough of repressed impulses.", "work": "Peculiarities of Behavior", "subcategory": "Impulse Disorders"},
    {"id": "STEKEL-0113", "text": "Kleptomania symbolically enacts forbidden sexual or aggressive wishes.", "work": "Peculiarities of Behavior", "subcategory": "Kleptomania"},
    {"id": "STEKEL-0114", "text": "Pyromania connects fire-setting to sexual excitement and aggression.", "work": "Peculiarities of Behavior", "subcategory": "Pyromania"},
    {"id": "STEKEL-0115", "text": "These impulse disorders share common underlying mechanisms.", "work": "Peculiarities of Behavior", "subcategory": "Impulse Disorders"},
    {"id": "STEKEL-0116", "text": "Each impulsive act has specific symbolic meaning for the individual.", "work": "Peculiarities of Behavior", "subcategory": "Symbolism"},
    {"id": "STEKEL-0117", "text": "The compulsive nature indicates ego-dystonic conflict.", "work": "Peculiarities of Behavior", "subcategory": "Ego"},
    {"id": "STEKEL-0118", "text": "Temporary dissociative states accompany many impulsive acts.", "work": "Peculiarities of Behavior", "subcategory": "Dissociation"},
    {"id": "STEKEL-0119", "text": "Treatment requires uncovering the specific unconscious determinants.", "work": "Peculiarities of Behavior", "subcategory": "Treatment"},
    {"id": "STEKEL-0120", "text": "These behaviors represent compromise formations between wish and defense.", "work": "Peculiarities of Behavior", "subcategory": "Compromise Formation"},
    
    # Dream Interpretation New Developments (Part 1)
    {"id": "STEKEL-0121", "text": "Symbol interpretation can proceed with less reliance on free association.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Technique"},
    {"id": "STEKEL-0122", "text": "Telepathic elements may appear in dreams.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Theory"},
    {"id": "STEKEL-0123", "text": "Dreams frequently predict future behavior of the dreamer.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Theory"},
    {"id": "STEKEL-0124", "text": "Analyst expertise permits more rapid dream interpretation.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Technique"},
    {"id": "STEKEL-0125", "text": "Certain symbols have consistent meanings across dreamers.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0126", "text": "The dream's emotional tone provides interpretive guidance.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Interpretation"},
    {"id": "STEKEL-0127", "text": "Series of dreams should be interpreted as connected narratives.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Analysis"},
    {"id": "STEKEL-0128", "text": "Counter-will dreams express opposition to conscious intentions.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Theory"},
    {"id": "STEKEL-0129", "text": "Dreams reveal the patient's transference to the analyst.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Transference"},
    {"id": "STEKEL-0130", "text": "Brief focused dream analysis can produce therapeutic results.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Technique"},
    
    # Autobiography
    {"id": "STEKEL-0131", "text": "Early family experiences shaped his later psychological interests.", "work": "Autobiography", "subcategory": "Biography"},
    {"id": "STEKEL-0132", "text": "His relationship with Freud was formative but ultimately conflictual.", "work": "Autobiography", "subcategory": "Biography"},
    {"id": "STEKEL-0133", "text": "Independent thinking led to break with psychoanalytic orthodoxy.", "work": "Autobiography", "subcategory": "Biography"},
    {"id": "STEKEL-0134", "text": "Clinical observation took precedence over theoretical allegiance.", "work": "Autobiography", "subcategory": "Methodology"},
    {"id": "STEKEL-0135", "text": "His therapeutic innovations arose from practical clinical necessity.", "work": "Autobiography", "subcategory": "Active Therapy"},
    {"id": "STEKEL-0136", "text": "Personal struggles informed his understanding of neurosis.", "work": "Autobiography", "subcategory": "Biography"},
    {"id": "STEKEL-0137", "text": "The psychoanalytic movement suffered from dogmatism and politics.", "work": "Autobiography", "subcategory": "History"},
    {"id": "STEKEL-0138", "text": "His active therapy technique developed from dissatisfaction with passive methods.", "work": "Autobiography", "subcategory": "Active Therapy"},
    {"id": "STEKEL-0139", "text": "Recognition of his contributions was impeded by institutional factors.", "work": "Autobiography", "subcategory": "History"},
    {"id": "STEKEL-0140", "text": "Psychological understanding should serve humanitarian purposes.", "work": "Autobiography", "subcategory": "Ethics"},
    
    # Nervous Anxiety States (Part 2)
    {"id": "STEKEL-0141", "text": "Anxiety attacks often represent disguised orgastic experiences.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Anxiety Theory"},
    {"id": "STEKEL-0142", "text": "Agoraphobia conceals fear of sexual temptation in public spaces.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Phobias"},
    {"id": "STEKEL-0143", "text": "Heart anxiety symbolizes conflicts about forbidden love.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Somatic Symptoms"},
    {"id": "STEKEL-0144", "text": "Free-floating anxiety attaches itself to available environmental objects.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Anxiety Theory"},
    {"id": "STEKEL-0145", "text": "Childhood anxiety experiences establish templates for adult neurosis.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Development"},
    {"id": "STEKEL-0146", "text": "Anxiety can function as self-punishment for forbidden wishes.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Anxiety Theory"},
    {"id": "STEKEL-0147", "text": "Phobias represent externalization of internal dangers.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Phobias"},
    {"id": "STEKEL-0148", "text": "The choice of anxiety symptom is never arbitrary.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Symptom Choice"},
    {"id": "STEKEL-0149", "text": "Secondary gain maintains anxiety symptoms once established.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Secondary Gain"},
    {"id": "STEKEL-0150", "text": "Therapeutic success requires emotional reliving, not mere intellectual insight.", "work": "Nervous Anxiety States and Their Treatment", "subcategory": "Catharsis"},
    
    # Language of Dreams (Part 2)
    {"id": "STEKEL-0151", "text": "Death in dreams often symbolizes sexual climax.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0152", "text": "Flying dreams typically represent sexual excitement and erection.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0153", "text": "Water symbolism connects to birth and maternal themes.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0154", "text": "Falling dreams express moral anxiety about sexual surrender.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0155", "text": "Teeth dreams relate to masturbation guilt and castration fears.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0156", "text": "Left and right in dreams represent wrong and right morally.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0157", "text": "Numbers in dreams carry specific symbolic significance.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0158", "text": "Animals in dreams represent instinctual drives or specific persons.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0159", "text": "Buildings and rooms symbolize the human body and its parts.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0160", "text": "Travel dreams represent life's journey and approaching death.", "work": "The Language of Dreams", "subcategory": "Dream Symbolism"},
    
    # Auto-Erotism (Part 2)
    {"id": "STEKEL-0161", "text": "Masturbatory equivalents appear in many seemingly innocent habits.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbatory Equivalents"},
    {"id": "STEKEL-0162", "text": "Nail-biting and hair-pulling serve as disguised masturbatory substitutes.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Masturbatory Equivalents"},
    {"id": "STEKEL-0163", "text": "The transition from masturbation to partner sexuality can be problematic.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Sexual Development"},
    {"id": "STEKEL-0164", "text": "Retained masturbation in marriage indicates psychological fixation.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Fixation"},
    {"id": "STEKEL-0165", "text": "Masturbation fantasies often involve forbidden incestuous objects.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Fantasy"},
    {"id": "STEKEL-0166", "text": "The struggle against masturbation depletes psychic energy.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Repression"},
    {"id": "STEKEL-0167", "text": "Religious prohibitions intensify masturbation conflicts.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Religion"},
    {"id": "STEKEL-0168", "text": "Masturbation serves as consolation for narcissistic injuries.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Narcissism"},
    {"id": "STEKEL-0169", "text": "Excessive guilt indicates the fantasy content is particularly forbidden.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "Guilt"},
    {"id": "STEKEL-0170", "text": "Masturbation conflicts contribute to obsessional symptom formation.", "work": "Auto-Erotism: Onanism and Neurosis", "subcategory": "OCD"},
    
    # Frigidity in Woman (Part 2)
    {"id": "STEKEL-0171", "text": "Vaginismus represents physical barricade against unwanted penetration.", "work": "Frigidity in Woman", "subcategory": "Vaginismus"},
    {"id": "STEKEL-0172", "text": "Disgust reactions to sexuality indicate repressed anal erotism.", "work": "Frigidity in Woman", "subcategory": "Anal Erotism"},
    {"id": "STEKEL-0173", "text": "Women who cannot achieve orgasm often harbor unconscious prostitution fantasies.", "work": "Frigidity in Woman", "subcategory": "Fantasy"},
    {"id": "STEKEL-0174", "text": "Frigidity toward the husband may coexist with responsiveness to fantasy objects.", "work": "Frigidity in Woman", "subcategory": "Fantasy"},
    {"id": "STEKEL-0175", "text": "Fear of loss of control underlies many cases of anorgasmia.", "work": "Frigidity in Woman", "subcategory": "Control"},
    {"id": "STEKEL-0176", "text": "Penis envy contributes to rejection of feminine sexual role.", "work": "Frigidity in Woman", "subcategory": "Penis Envy"},
    {"id": "STEKEL-0177", "text": "Unconscious lesbianism may manifest as heterosexual frigidity.", "work": "Frigidity in Woman", "subcategory": "Homosexuality"},
    {"id": "STEKEL-0178", "text": "The wedding night often establishes patterns of later dysfunction.", "work": "Frigidity in Woman", "subcategory": "Marriage"},
    {"id": "STEKEL-0179", "text": "Women's sexual response requires psychological as well as physical stimulation.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0180", "text": "Frigidity can represent loyalty to the father against the husband.", "work": "Frigidity in Woman", "subcategory": "Oedipal Complex"},
    
    # Fetishism (Part 2)
    {"id": "STEKEL-0181", "text": "Shoe and foot fetishism relates to childhood position viewing adults.", "work": "Sexual Aberrations", "subcategory": "Foot Fetishism"},
    {"id": "STEKEL-0182", "text": "Hair fetishism often connects to pubic hair and genital symbolism.", "work": "Sexual Aberrations", "subcategory": "Hair Fetishism"},
    {"id": "STEKEL-0183", "text": "Clothing fetishes represent the absent body beneath.", "work": "Sexual Aberrations", "subcategory": "Clothing Fetishism"},
    {"id": "STEKEL-0184", "text": "Rubber and leather fetishism involves skin symbolism and maternal contact.", "work": "Sexual Aberrations", "subcategory": "Material Fetishism"},
    {"id": "STEKEL-0185", "text": "The fetish object must be present for sexual arousal to occur.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0186", "text": "Fetishism develops when normal pathways to satisfaction are blocked.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0187", "text": "The fetishist knows his interest is abnormal yet cannot change it.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0188", "text": "Partial fetishistic interests enhance normal sexuality.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0189", "text": "The smell of the fetish object often carries special significance.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    {"id": "STEKEL-0190", "text": "Fetishism represents arrest at the stage of forepleasure.", "work": "Sexual Aberrations", "subcategory": "Fetishism"},
    
    # Sadism and Masochism (Part 2)
    {"id": "STEKEL-0191", "text": "Beating fantasies originate in childhood and persist unconsciously.", "work": "Sadism and Masochism", "subcategory": "Fantasy"},
    {"id": "STEKEL-0192", "text": "The masochist orchestrates scenarios to achieve desired suffering.", "work": "Sadism and Masochism", "subcategory": "Masochism"},
    {"id": "STEKEL-0193", "text": "Sadistic pornography consumption reveals latent sadistic tendencies.", "work": "Sadism and Masochism", "subcategory": "Sadism"},
    {"id": "STEKEL-0194", "text": "Sexual murder represents the extreme of sadistic fusion.", "work": "Sadism and Masochism", "subcategory": "Sadism"},
    {"id": "STEKEL-0195", "text": "Masochistic surrender provides relief from the burden of autonomy.", "work": "Sadism and Masochism", "subcategory": "Masochism"},
    {"id": "STEKEL-0196", "text": "Humiliation serves sexual purposes in masochistic scenarios.", "work": "Sadism and Masochism", "subcategory": "Masochism"},
    {"id": "STEKEL-0197", "text": "The roles of sadist and masochist can alternate within individuals.", "work": "Sadism and Masochism", "subcategory": "Sadomasochism"},
    {"id": "STEKEL-0198", "text": "Verbal cruelty serves sadistic purposes equivalent to physical cruelty.", "work": "Sadism and Masochism", "subcategory": "Sadism"},
    {"id": "STEKEL-0199", "text": "Masochistic character invites mistreatment in everyday life.", "work": "Sadism and Masochism", "subcategory": "Character"},
    {"id": "STEKEL-0200", "text": "Religious asceticism often contains eroticized masochistic elements.", "work": "Sadism and Masochism", "subcategory": "Religion"},
    
    # Disorders of Instincts (Part 2)
    {"id": "STEKEL-0201", "text": "Jealousy contains projected unfaithfulness wishes.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Jealousy"},
    {"id": "STEKEL-0202", "text": "Envy represents oral-acquisitive impulses directed at others' possessions.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Envy"},
    {"id": "STEKEL-0203", "text": "Greed indicates insatiable oral fixation.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Oral Fixation"},
    {"id": "STEKEL-0204", "text": "Anger serves to destroy obstacles to instinctual satisfaction.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Anger"},
    {"id": "STEKEL-0205", "text": "Fear protects the ego from overwhelming stimulation.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Fear"},
    {"id": "STEKEL-0206", "text": "Shame relates to exhibitionistic wishes and their prohibition.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Shame"},
    {"id": "STEKEL-0207", "text": "Disgust represents reaction formation against attraction to the forbidden.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Disgust"},
    {"id": "STEKEL-0208", "text": "Boredom indicates blocked libidinal and aggressive drives.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Boredom"},
    {"id": "STEKEL-0209", "text": "Enthusiasm represents libido directed toward idealized objects.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Enthusiasm"},
    {"id": "STEKEL-0210", "text": "Emotional blunting suggests massive repression of affect.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Affect"},
    
    # Compulsion and Doubt (Part 2)
    {"id": "STEKEL-0211", "text": "Counting compulsions relate to forbidden numerical symbolism.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0212", "text": "Washing rituals attempt to cleanse moral contamination.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0213", "text": "Checking behaviors seek to undo aggressive wishes.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0214", "text": "Hoarding represents anal retention and control.", "work": "Compulsion and Doubt", "subcategory": "Hoarding"},
    {"id": "STEKEL-0215", "text": "Touching compulsions involve forbidden contact wishes.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0216", "text": "Ordering and arranging defend against chaos of impulses.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0217", "text": "The obsessional's precision masks underlying sloppiness wishes.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0218", "text": "Blasphemous obsessions express rebellion against parental authority.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0219", "text": "Fear of contamination projects internal sense of dirtiness.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0220", "text": "Symmetry compulsions represent attempts at psychic balance.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    
    # Technique (Part 2)
    {"id": "STEKEL-0221", "text": "The first dream in analysis reveals the core neurotic conflict.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Dream Analysis"},
    {"id": "STEKEL-0222", "text": "Homework assignments accelerate therapeutic progress.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Active Therapy"},
    {"id": "STEKEL-0223", "text": "The analyst should share relevant personal experiences when helpful.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Self-Disclosure"},
    {"id": "STEKEL-0224", "text": "Silence from the analyst can be countertherapeutic.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Active Therapy"},
    {"id": "STEKEL-0225", "text": "Direct questioning elicits material not produced spontaneously.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Technique"},
    {"id": "STEKEL-0226", "text": "The patient's lies and evasions are themselves diagnostic.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Resistance"},
    {"id": "STEKEL-0227", "text": "Physical symptoms should be addressed alongside psychological ones.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Psychosomatic"},
    {"id": "STEKEL-0228", "text": "Therapeutic optimism influences treatment outcome positively.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Therapeutic Attitude"},
    {"id": "STEKEL-0229", "text": "Confrontation of defenses must be timed appropriately.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Timing"},
    {"id": "STEKEL-0230", "text": "Analysis of the patient's current life takes precedence over childhood excavation.", "work": "Technique of Analytical Psychotherapy", "subcategory": "Focus"},
    
    # Impotence (Part 2)
    {"id": "STEKEL-0231", "text": "Premature ejaculation represents hostility disguised as eagerness.", "work": "Impotence in the Male", "subcategory": "Premature Ejaculation"},
    {"id": "STEKEL-0232", "text": "Retarded ejaculation indicates withholding from the partner.", "work": "Impotence in the Male", "subcategory": "Retarded Ejaculation"},
    {"id": "STEKEL-0233", "text": "Selective impotence reveals the psychological nature of the condition.", "work": "Impotence in the Male", "subcategory": "Male Sexuality"},
    {"id": "STEKEL-0234", "text": "Prostitute-madonna splitting prevents unified sexual functioning.", "work": "Impotence in the Male", "subcategory": "Splitting"},
    {"id": "STEKEL-0235", "text": "Fear of venereal disease masks deeper castration concerns.", "work": "Impotence in the Male", "subcategory": "Castration Anxiety"},
    {"id": "STEKEL-0236", "text": "Impotence on wedding night reflects incest taboo transfer to wife.", "work": "Impotence in the Male", "subcategory": "Oedipal Complex"},
    {"id": "STEKEL-0237", "text": "Alcohol-facilitated potency indicates anxiety-based inhibition.", "work": "Impotence in the Male", "subcategory": "Anxiety"},
    {"id": "STEKEL-0238", "text": "Morning erections prove organic capacity in psychogenic cases.", "work": "Impotence in the Male", "subcategory": "Diagnosis"},
    {"id": "STEKEL-0239", "text": "Impotence can express unconscious refusal of paternity.", "work": "Impotence in the Male", "subcategory": "Fatherhood"},
    {"id": "STEKEL-0240", "text": "Partner change sometimes reveals the relational nature of dysfunction.", "work": "Impotence in the Male", "subcategory": "Relationship"},
    
    # Bisexual Love (Part 2)
    {"id": "STEKEL-0241", "text": "Intense hatred of homosexuals often masks attraction.", "work": "Bi-Sexual Love", "subcategory": "Homophobia"},
    {"id": "STEKEL-0242", "text": "Don Juanism represents flight from homosexual tendencies.", "work": "Bi-Sexual Love", "subcategory": "Don Juanism"},
    {"id": "STEKEL-0243", "text": "Certain career choices reflect sublimated homosexual interests.", "work": "Bi-Sexual Love", "subcategory": "Sublimation"},
    {"id": "STEKEL-0244", "text": "Excessive masculinity may defend against feminine identification.", "work": "Bi-Sexual Love", "subcategory": "Masculinity"},
    {"id": "STEKEL-0245", "text": "Paranoid jealousy contains homosexual projection.", "work": "Bi-Sexual Love", "subcategory": "Paranoia"},
    {"id": "STEKEL-0246", "text": "Hero worship contains homosexual admiration.", "work": "Bi-Sexual Love", "subcategory": "Identification"},
    {"id": "STEKEL-0247", "text": "Some heterosexual dysfunction results from unacknowledged homosexuality.", "work": "Bi-Sexual Love", "subcategory": "Homosexuality"},
    {"id": "STEKEL-0248", "text": "Dreams frequently reveal bisexual content.", "work": "Bi-Sexual Love", "subcategory": "Dreams"},
    {"id": "STEKEL-0249", "text": "Homosexual panic occurs when defenses against awareness fail.", "work": "Bi-Sexual Love", "subcategory": "Homosexual Panic"},
    {"id": "STEKEL-0250", "text": "Object choice develops through complex identification processes.", "work": "Bi-Sexual Love", "subcategory": "Object Choice"},
    
    # Peculiarities (Part 2)
    {"id": "STEKEL-0251", "text": "The kleptomaniac typically steals objects of symbolic rather than material value.", "work": "Peculiarities of Behavior", "subcategory": "Kleptomania"},
    {"id": "STEKEL-0252", "text": "Pyromaniacs often experience urinary symptoms alongside fire-setting urges.", "work": "Peculiarities of Behavior", "subcategory": "Pyromania"},
    {"id": "STEKEL-0253", "text": "Dipsomanic episodes follow specific psychological precipitants.", "work": "Peculiarities of Behavior", "subcategory": "Dipsomania"},
    {"id": "STEKEL-0254", "text": "Wandering episodes often lead to locations of symbolic significance.", "work": "Peculiarities of Behavior", "subcategory": "Wandering"},
    {"id": "STEKEL-0255", "text": "Amnesia for impulsive acts serves defensive purposes.", "work": "Peculiarities of Behavior", "subcategory": "Amnesia"},
    {"id": "STEKEL-0256", "text": "Impulsive behaviors often occur at symbolically significant times.", "work": "Peculiarities of Behavior", "subcategory": "Timing"},
    {"id": "STEKEL-0257", "text": "The gambler seeks punishment through losing as much as winning.", "work": "Peculiarities of Behavior", "subcategory": "Gambling"},
    {"id": "STEKEL-0258", "text": "Compulsive buying represents symbolic incorporation.", "work": "Peculiarities of Behavior", "subcategory": "Compulsive Buying"},
    {"id": "STEKEL-0259", "text": "Trichotillomania involves aggression turned against the self.", "work": "Peculiarities of Behavior", "subcategory": "Trichotillomania"},
    {"id": "STEKEL-0260", "text": "Multiple peculiarities often coexist in the same individual.", "work": "Peculiarities of Behavior", "subcategory": "Comorbidity"},
    
    # Dream Interpretation (Part 2)
    {"id": "STEKEL-0261", "text": "Anxiety dreams represent failed wish-fulfillment attempts.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Anxiety Dreams"},
    {"id": "STEKEL-0262", "text": "Punishment dreams satisfy superego demands.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Punishment Dreams"},
    {"id": "STEKEL-0263", "text": "The day residue provides material for deeper wishes to attach to.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Day Residue"},
    {"id": "STEKEL-0264", "text": "Examination dreams relate to sexual testing and adequacy fears.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Examination Dreams"},
    {"id": "STEKEL-0265", "text": "Naked dreams express exhibitionistic wishes and shame.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Naked Dreams"},
    {"id": "STEKEL-0266", "text": "Pursuit dreams represent flight from one's own desires.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Chase Dreams"},
    {"id": "STEKEL-0267", "text": "Dreams of deceased persons express unresolved relationships.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Death Dreams"},
    {"id": "STEKEL-0268", "text": "Recurring dreams cease when their meaning is understood.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Recurring Dreams"},
    {"id": "STEKEL-0269", "text": "Children's dreams are more transparent than adults'.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Child Dreams"},
    {"id": "STEKEL-0270", "text": "The dreamer is represented by multiple figures in the same dream.", "work": "The Interpretation of Dreams: New Developments", "subcategory": "Dream Figures"},
    
    # Autobiography (Part 2)
    {"id": "STEKEL-0271", "text": "Medical training provided essential foundation for psychological work.", "work": "Autobiography", "subcategory": "Training"},
    {"id": "STEKEL-0272", "text": "Vienna's intellectual atmosphere fostered psychoanalytic development.", "work": "Autobiography", "subcategory": "History"},
    {"id": "STEKEL-0273", "text": "Patients were his primary teachers about the nature of neurosis.", "work": "Autobiography", "subcategory": "Clinical Learning"},
    {"id": "STEKEL-0274", "text": "Writing served as method of clarifying and developing ideas.", "work": "Autobiography", "subcategory": "Writing"},
    {"id": "STEKEL-0275", "text": "Controversy stimulated rather than discouraged his productivity.", "work": "Autobiography", "subcategory": "Controversy"},
    {"id": "STEKEL-0276", "text": "Each patient presented unique manifestations of universal conflicts.", "work": "Autobiography", "subcategory": "Clinical Method"},
    {"id": "STEKEL-0277", "text": "His Jewish background influenced his outsider perspective.", "work": "Autobiography", "subcategory": "Identity"},
    {"id": "STEKEL-0278", "text": "World War I demonstrated mass psychological phenomena.", "work": "Autobiography", "subcategory": "War Psychology"},
    {"id": "STEKEL-0279", "text": "Emigration disrupted but did not end his professional contributions.", "work": "Autobiography", "subcategory": "Emigration"},
    {"id": "STEKEL-0280", "text": "Scientific integrity required willingness to challenge established views.", "work": "Autobiography", "subcategory": "Integrity"},
    
    # Anger
    {"id": "STEKEL-0281", "text": "Anger originates from frustrated instinctual drives seeking discharge.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Anger"},
    {"id": "STEKEL-0282", "text": "Repressed anger converts into anxiety and physical symptoms.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Anger"},
    {"id": "STEKEL-0283", "text": "Rage against loved ones produces guilt requiring symptomatic expiation.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Anger"},
    {"id": "STEKEL-0284", "text": "Murderous wishes exist universally but remain largely unconscious.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Aggression"},
    {"id": "STEKEL-0285", "text": "Anger toward parents persists beneath conscious filial devotion.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Parental Anger"},
    {"id": "STEKEL-0286", "text": "Passive-aggressive behavior represents disguised anger expression.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Passive-Aggression"},
    {"id": "STEKEL-0287", "text": "Self-directed anger underlies depression and self-destructive behavior.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Self-Aggression"},
    {"id": "STEKEL-0288", "text": "Righteous indignation often masks personal hostile motives.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Anger"},
    {"id": "STEKEL-0289", "text": "Anger in dreams appears symbolically as storms, fire, and wild animals.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Dream Symbolism"},
    {"id": "STEKEL-0290", "text": "Therapeutic expression of anger produces symptomatic relief.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Catharsis"},
    
    # Male Sexuality
    {"id": "STEKEL-0291", "text": "Male sexual development requires successful detachment from maternal object.", "work": "Impotence in the Male", "subcategory": "Male Development"},
    {"id": "STEKEL-0292", "text": "Castration anxiety shapes all aspects of masculine sexuality.", "work": "Impotence in the Male", "subcategory": "Castration Anxiety"},
    {"id": "STEKEL-0293", "text": "Potency depends upon integration of tender and sensual currents.", "work": "Impotence in the Male", "subcategory": "Potency"},
    {"id": "STEKEL-0294", "text": "The male fears engulfment by the female during intercourse.", "work": "Impotence in the Male", "subcategory": "Engulfment Fear"},
    {"id": "STEKEL-0295", "text": "Competition with the father establishes patterns of sexual rivalry.", "work": "Impotence in the Male", "subcategory": "Oedipal Complex"},
    {"id": "STEKEL-0296", "text": "Male homosexuality represents identification with mother rather than father.", "work": "Bi-Sexual Love", "subcategory": "Male Homosexuality"},
    {"id": "STEKEL-0297", "text": "Don Juanism compensates for underlying doubts about masculinity.", "work": "Impotence in the Male", "subcategory": "Don Juanism"},
    {"id": "STEKEL-0298", "text": "Performance anxiety reflects deeper fears of inadequacy and judgment.", "work": "Impotence in the Male", "subcategory": "Performance Anxiety"},
    {"id": "STEKEL-0299", "text": "Male sexuality requires overcoming incest barrier to achieve partner satisfaction.", "work": "Impotence in the Male", "subcategory": "Incest Barrier"},
    {"id": "STEKEL-0300", "text": "Premature ejaculation often expresses unconscious contempt for the partner.", "work": "Impotence in the Male", "subcategory": "Premature Ejaculation"},
    
    # Female Sexuality
    {"id": "STEKEL-0301", "text": "Female sexuality is no less intense than male when freed from inhibition.", "work": "Frigidity in Woman", "subcategory": "Female Sexuality"},
    {"id": "STEKEL-0302", "text": "Vaginal orgasm represents mature feminine sexuality.", "work": "Frigidity in Woman", "subcategory": "Orgasm"},
    {"id": "STEKEL-0303", "text": "Women's sexuality develops through transfer of erotism from clitoris to vagina.", "work": "Frigidity in Woman", "subcategory": "Sexual Development"},
    {"id": "STEKEL-0304", "text": "Penis envy influences but does not determine feminine development.", "work": "Frigidity in Woman", "subcategory": "Penis Envy"},
    {"id": "STEKEL-0305", "text": "Maternal identification shapes the woman's sexual receptivity.", "work": "Frigidity in Woman", "subcategory": "Identification"},
    {"id": "STEKEL-0306", "text": "Female masochism is culturally reinforced rather than biologically determined.", "work": "Frigidity in Woman", "subcategory": "Female Masochism"},
    {"id": "STEKEL-0307", "text": "Women's sexual fantasies often contain surrender and ravishment themes.", "work": "Frigidity in Woman", "subcategory": "Fantasy"},
    {"id": "STEKEL-0308", "text": "Frigidity serves multiple defensive functions against feared intimacy.", "work": "Frigidity in Woman", "subcategory": "Defense"},
    {"id": "STEKEL-0309", "text": "The father's attitude toward the daughter shapes her later sexual response.", "work": "Frigidity in Woman", "subcategory": "Father-Daughter"},
    {"id": "STEKEL-0310", "text": "Women's capacity for multiple orgasms indicates rich erotic potential.", "work": "Frigidity in Woman", "subcategory": "Orgasm"},
    
    # OCD - 100 Positions
    {"id": "STEKEL-0311", "text": "Obsessional symptoms defend against breakthrough of murderous impulses.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0312", "text": "The obsessional's doubt paralyzes action to prevent feared aggression.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0313", "text": "Magical thinking underlies rituals designed to prevent catastrophe.", "work": "Compulsion and Doubt", "subcategory": "Magical Thinking"},
    {"id": "STEKEL-0314", "text": "Anal-erotic fixation contributes to obsessional character formation.", "work": "Compulsion and Doubt", "subcategory": "Anal Character"},
    {"id": "STEKEL-0315", "text": "Cleanliness compulsions symbolically address moral contamination.", "work": "Compulsion and Doubt", "subcategory": "Washing"},
    {"id": "STEKEL-0316", "text": "The obsessional's orderliness defends against chaotic destructive wishes.", "work": "Compulsion and Doubt", "subcategory": "Orderliness"},
    {"id": "STEKEL-0317", "text": "Religious scrupulosity masks rebellion against divine and parental authority.", "work": "Compulsion and Doubt", "subcategory": "Scrupulosity"},
    {"id": "STEKEL-0318", "text": "Obsessional symptoms represent compromise between wish and prohibition.", "work": "Compulsion and Doubt", "subcategory": "Compromise Formation"},
    {"id": "STEKEL-0319", "text": "The obsessional delays decisions to avoid responsibility for outcomes.", "work": "Compulsion and Doubt", "subcategory": "Indecision"},
    {"id": "STEKEL-0320", "text": "Thought-action fusion makes thinking equivalent to doing for the obsessional.", "work": "Compulsion and Doubt", "subcategory": "Thought-Action Fusion"},
    
    # Personal Fulfillment
    {"id": "STEKEL-0321", "text": "Neurosis represents blocked pathways to genuine satisfaction.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Fulfillment"},
    {"id": "STEKEL-0322", "text": "Self-knowledge is prerequisite for authentic living.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Self-Knowledge"},
    {"id": "STEKEL-0323", "text": "Creative work provides sublimated expression of instinctual drives.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Creativity"},
    {"id": "STEKEL-0324", "text": "Love relationships require integration of sexuality and tenderness.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Love"},
    {"id": "STEKEL-0325", "text": "Fulfillment demands courage to acknowledge forbidden wishes.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Courage"},
    {"id": "STEKEL-0326", "text": "Work satisfaction depends upon alignment with genuine interests.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Work"},
    {"id": "STEKEL-0327", "text": "The neurotic sacrifices fulfillment to maintain repression.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Neurosis"},
    {"id": "STEKEL-0328", "text": "Liberation from parental complexes enables autonomous adult functioning.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Autonomy"},
    {"id": "STEKEL-0329", "text": "Acceptance of mortality intensifies appreciation of present living.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Mortality"},
    {"id": "STEKEL-0330", "text": "Personal fulfillment requires reconciliation with one's bisexual nature.", "work": "Disorders of the Instincts and the Emotions", "subcategory": "Bisexuality"},
    
    # OCD Extended (100 positions continued)
    {"id": "STEKEL-0331", "text": "Obsessional neurosis originates from repressed aggressive and murderous impulses.", "work": "Compulsion and Doubt", "subcategory": "OCD"},
    {"id": "STEKEL-0332", "text": "The obsessional's doubt represents paralysis between love and hate.", "work": "Compulsion and Doubt", "subcategory": "Ambivalence"},
    {"id": "STEKEL-0333", "text": "Compulsive rituals serve to magically undo or prevent imagined harm.", "work": "Compulsion and Doubt", "subcategory": "Rituals"},
    {"id": "STEKEL-0334", "text": "Anal-erotic fixation forms the libidinal foundation of obsessional character.", "work": "Compulsion and Doubt", "subcategory": "Anal Character"},
    {"id": "STEKEL-0335", "text": "The obsessional's conscientiousness masks unconscious cruelty.", "work": "Compulsion and Doubt", "subcategory": "Character"},
    {"id": "STEKEL-0336", "text": "Isolation of affect separates ideas from their emotional significance.", "work": "Compulsion and Doubt", "subcategory": "Isolation"},
    {"id": "STEKEL-0337", "text": "Reaction formation transforms hatred into excessive solicitude.", "work": "Compulsion and Doubt", "subcategory": "Reaction Formation"},
    {"id": "STEKEL-0338", "text": "Death wishes toward loved ones generate overwhelming guilt.", "work": "Compulsion and Doubt", "subcategory": "Death Wishes"},
    {"id": "STEKEL-0339", "text": "The obsessional substitutes thinking for acting.", "work": "Compulsion and Doubt", "subcategory": "Intellectualization"},
    {"id": "STEKEL-0340", "text": "Omnipotence of thought makes thinking equivalent to doing.", "work": "Compulsion and Doubt", "subcategory": "Magical Thinking"},
    {"id": "STEKEL-0341", "text": "Washing compulsions symbolize cleansing of moral guilt.", "work": "Compulsion and Doubt", "subcategory": "Washing"},
    {"id": "STEKEL-0342", "text": "Checking behaviors attempt to verify that harm has not occurred.", "work": "Compulsion and Doubt", "subcategory": "Checking"},
    {"id": "STEKEL-0343", "text": "Counting rituals impose order on threatening chaos.", "work": "Compulsion and Doubt", "subcategory": "Counting"},
    {"id": "STEKEL-0344", "text": "The obsessional fears loss of control over destructive impulses.", "work": "Compulsion and Doubt", "subcategory": "Control"},
    {"id": "STEKEL-0345", "text": "Perfectionism defends against fear of making harmful mistakes.", "work": "Compulsion and Doubt", "subcategory": "Perfectionism"},
    {"id": "STEKEL-0346", "text": "The obsessional's punctuality masks wishes to frustrate others by lateness.", "work": "Compulsion and Doubt", "subcategory": "Punctuality"},
    {"id": "STEKEL-0347", "text": "Obsessional slowness represents unconscious defiance.", "work": "Compulsion and Doubt", "subcategory": "Slowness"},
    {"id": "STEKEL-0348", "text": "The obsessional's fairness compensates for wishes to cheat.", "work": "Compulsion and Doubt", "subcategory": "Fairness"},
    {"id": "STEKEL-0349", "text": "Obsessional symptoms tend to spread and proliferate over time.", "work": "Compulsion and Doubt", "subcategory": "Symptom Spread"},
    {"id": "STEKEL-0350", "text": "The obsessional experiences ideas as foreign intrusions.", "work": "Compulsion and Doubt", "subcategory": "Ego-Dystonic"},
]

for pos in stekel_positions:
    pos["position_id"] = pos["id"]
    pos["domain"] = "PSYCHOLOGY"
    pos["category"] = "Stekel Analysis"

def main():
    db_path = "data/FREUD_DATABASE_UNIFIED.json"
    
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    if isinstance(db, dict) and 'positions' in db:
        positions = db['positions']
    elif isinstance(db, list):
        positions = db
    else:
        print("Unexpected database structure")
        return
    
    existing_ids = {p.get('id', p.get('position_id', '')) for p in positions}
    
    new_positions = []
    for pos in stekel_positions:
        if pos['id'] not in existing_ids:
            new_positions.append(pos)
    
    print(f"Found {len(new_positions)} new Stekel positions to add")
    
    positions.extend(new_positions)
    
    if isinstance(db, dict):
        db['positions'] = positions
        if 'metadata' in db:
            db['metadata']['total_positions'] = len(positions)
            db['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            db['metadata']['stekel_expansion'] = f"Wilhelm Stekel - {len(new_positions)} positions on OCD, anxiety, dreams, sexuality, and active therapy"
    
    with open(db_path, 'w') as f:
        json.dump(db, f, indent=2)
    
    print(f"Database now has {len(positions)} total positions")
    print(f"Added {len(new_positions)} positions from Wilhelm Stekel")

if __name__ == "__main__":
    main()
