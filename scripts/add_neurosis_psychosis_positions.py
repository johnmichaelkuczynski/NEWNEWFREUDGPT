#!/usr/bin/env python3
"""
Add Kuczynski's Neurosis vs Psychosis positions to the database.
These positions cover neurosis, psychosis, gender psychology, compulsive work,
stuttering, learning from adversity, writing rules, business, and more.
"""

import json
from datetime import datetime

neurosis_psychosis_positions = [
    {
        "id": "NP-0001",
        "position_id": "NP-0001",
        "text": "Psychosis is a mental impairment precipitated and sustained by a break with external reality. Psychosis is a mental impairment that is precipitated and sustained by a break with external reality.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0002",
        "position_id": "NP-0002",
        "text": "Neurosis is a mental impairment precipitated and sustained by a break with one's emotional condition. Neurosis is a mental impairment that is precipitated and sustained by a break with one's emotional condition.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0003",
        "position_id": "NP-0003",
        "text": "The neurotic flees from his emotions. The neurotic flees from his emotions; the psychotic flees from reality.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0004",
        "position_id": "NP-0004",
        "text": "The psychotic flees from reality. The neurotic flees from his emotions; the psychotic flees from reality.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0005",
        "position_id": "NP-0005",
        "text": "Neurosis may lead to a blunting of one's awareness of certain aspects of external reality. Neurosis may lead to a blunting of one's awareness of certain aspects of external reality, but any such loss of awareness is subordinate to loss of awareness of one's emotional condition.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0006",
        "position_id": "NP-0006",
        "text": "Any loss of awareness in neurosis is subordinate to loss of awareness of one's emotional condition. Neurosis may lead to a blunting of one's awareness of certain aspects of external reality, but any such loss of awareness is subordinate to loss of awareness of one's emotional condition.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0007",
        "position_id": "NP-0007",
        "text": "Psychosis may lead to a disruption of one's understanding of one's emotional condition. Similarly, psychosis may lead to a disruption of one's understanding of one's emotional condition, but any such disturbance is subordinate to the psychotic's loss of awareness of external reality.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0008",
        "position_id": "NP-0008",
        "text": "Any disturbance in psychosis is subordinate to the psychotic's loss of awareness of external reality. Similarly, psychosis may lead to a disruption of one's understanding of one's emotional condition, but any such disturbance is subordinate to the psychotic's loss of awareness of external reality.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0009",
        "position_id": "NP-0009",
        "text": "Neurosis and psychosis are not mirror images of each other. Though symmetrical in the just-described respects, neurosis and psychosis are ultimately not mirror images of each other.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis vs Psychosis"
    },
    {
        "id": "NP-0010",
        "position_id": "NP-0010",
        "text": "Psychosis involves a partial regression to a condition of psychological infancy. This is a consequence of the fact that psychosis involves a partial regression to a condition of psychological infancy, the operative term being 'partial.'",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0011",
        "position_id": "NP-0011",
        "text": "An infant is not psychotic. An infant is not psychotic.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Developmental Psychology"
    },
    {
        "id": "NP-0012",
        "position_id": "NP-0012",
        "text": "The infant's psychological condition is integrated and healthy. The infant's psychological condition is integrated and healthy, even though the infant's understanding of reality is even more subjective, and therefore more projective, than that of the adult psychotic.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Developmental Psychology"
    },
    {
        "id": "NP-0013",
        "position_id": "NP-0013",
        "text": "The adult psychotic has the psychological architecture of both an adult and an infant. The adult psychotic, on the other hand, has the psychological architecture of an adult as well as that of an infant.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0014",
        "position_id": "NP-0014",
        "text": "The psychotic has two entirely distinct and incompatible ways of processing information. Therefore, the psychotic has two entirely distinct and incompatible ways of processing information.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0015",
        "position_id": "NP-0015",
        "text": "The psychotic does not have a unified value system. He does not have a unified value system; he does not have a unified understanding of how to implement such values as he has; and his psychological condition is therefore one of utter disarray.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0016",
        "position_id": "NP-0016",
        "text": "The psychotic does not have a unified understanding of how to implement values. He does not have a unified value system; he does not have a unified understanding of how to implement such values as he has; and his psychological condition is therefore one of utter disarray.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0017",
        "position_id": "NP-0017",
        "text": "The psychological condition of the psychotic is one of utter disarray. He does not have a unified value system; he does not have a unified understanding of how to implement such values as he has; and his psychological condition is therefore one of utter disarray.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0018",
        "position_id": "NP-0018",
        "text": "Nothing comparable to the psychotic's condition holds of the neurotic. And therein lies the peculiarly damaging nature of psychosis. Nothing comparable holds of the neurotic.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis vs Psychosis"
    },
    {
        "id": "NP-0019",
        "position_id": "NP-0019",
        "text": "Neurosis is about containing threats to one's integration by repressing them. Neurosis is about containing threats to one's integration by repressing them.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0020",
        "position_id": "NP-0020",
        "text": "To repress a conceit is to bury one's knowledge of its emotional valence in the unconscious. To repress a conceit is not to bury one's knowledge of it in the unconscious; it is rather to bury one's knowledge of its emotional valence in the unconscious.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Repression"
    },
    {
        "id": "NP-0021",
        "position_id": "NP-0021",
        "text": "The neurotic's condition is one of relatively unimpaired intellectual awareness. As a result, the neurotic's condition is one of relatively unimpaired intellectual awareness.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0022",
        "position_id": "NP-0022",
        "text": "The neurotic may have heightened intellectual awareness. In fact, in some circumscribed ways, it may be even be a condition heightened intellectual awareness, owing to the fact that the neurotic is likely to compensate for his impoverished emotional state by hypercathecting his intellect.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0023",
        "position_id": "NP-0023",
        "text": "The neurotic compensates for his impoverished emotional state by hypercathecting his intellect. In fact, in some circumscribed ways, it may be even be a condition heightened intellectual awareness, owing to the fact that the neurotic is likely to compensate for his impoverished emotional state by hypercathecting his intellect.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0024",
        "position_id": "NP-0024",
        "text": "The neurotic has a hyper-stable, though also an ossified psyche. Moreover, by stripping the contents of consciousness of their emotional valences, the neurotic guarantees that he has a hyper-stable, though also an ossified psyche.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0025",
        "position_id": "NP-0025",
        "text": "The essence of psychosis is an inability to organize consciously experienced emotion. The essence of psychosis is an inability to organize consciously experienced emotion; the essence of neurosis is an inability to have consciously experienced emotion.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0026",
        "position_id": "NP-0026",
        "text": "The essence of neurosis is an inability to have consciously experienced emotion. The essence of psychosis is an inability to organize consciously experienced emotion; the essence of neurosis is an inability to have consciously experienced emotion.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0027",
        "position_id": "NP-0027",
        "text": "The psychotic is paralyzed by a superabundance of emotion. The former is paralyzed by a superabundance of emotion, the latter by lack of it.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Psychosis"
    },
    {
        "id": "NP-0028",
        "position_id": "NP-0028",
        "text": "The neurotic is paralyzed by a lack of emotion. The former is paralyzed by a superabundance of emotion, the latter by lack of it.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Neurosis"
    },
    {
        "id": "NP-0029",
        "position_id": "NP-0029",
        "text": "For men, happiness is about forging one's own identity. For men, happiness is about forging one's own identity.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0030",
        "position_id": "NP-0030",
        "text": "For women, happiness is about being loved. For women, happiness is about being loved.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Female Psychology"
    },
    {
        "id": "NP-0031",
        "position_id": "NP-0031",
        "text": "Men are happy if they triumphed over their own fathers. Men are happy if they triumphed over their own fathers, and women are happy if their fathers loved them.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0032",
        "position_id": "NP-0032",
        "text": "Women are happy if their fathers loved them. Men are happy if they triumphed over their own fathers, and women are happy if their fathers loved them.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Female Psychology"
    },
    {
        "id": "NP-0033",
        "position_id": "NP-0033",
        "text": "For a man to triumph over his father is for him not to submit to his father. For a man to triumph over his father is for him not to submit to his father.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0034",
        "position_id": "NP-0034",
        "text": "For a man to triumph over his father is for him to establish his own identity. It is for him to establish his own identity.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0035",
        "position_id": "NP-0035",
        "text": "A man can establish his own identity by doing the opposite of what his father does. He can establish his own identity by doing the opposite of what his father does.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0036",
        "position_id": "NP-0036",
        "text": "Schopenhauer established his identity by doing the opposite of what his father did. Schopenhauer's father was a wealthy merchant. Schopenhauer was a great philosopher who spoke with contempt of merchants.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0037",
        "position_id": "NP-0037",
        "text": "A man can establish his identity by doing what his father does but doing it better. He can establish his identity by doing what his father does but doing it better.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0038",
        "position_id": "NP-0038",
        "text": "Mozart established his identity by doing what his father did but doing it better. Mozart's father was a good composer; Mozart was a great composer.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0039",
        "position_id": "NP-0039",
        "text": "Donald Trump established his identity by doing what his father did but doing it better. Trump's father was a moderately successful business man; Trump is an extremely successful businessman.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0040",
        "position_id": "NP-0040",
        "text": "A man can fail in three ways. There are three ways a man can fail.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0041",
        "position_id": "NP-0041",
        "text": "A man can fail by trying to fill his father's shoes but failing. He can try to fill his father's shoes but fail.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0042",
        "position_id": "NP-0042",
        "text": "A man can fail by submitting to his father without trying to fill his shoes. He can submit to his father without even going so far as to try to fill his shoes.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0043",
        "position_id": "NP-0043",
        "text": "A man can fail by having no father at all. He can have no father at all and thus have no father to triumph over or to fail to triumph over.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Male Psychology"
    },
    {
        "id": "NP-0044",
        "position_id": "NP-0044",
        "text": "Compulsive Work is about avoidance. Compulsive Work is about avoidance.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Compulsive Behavior",
        "subcategory": "Workaholism"
    },
    {
        "id": "NP-0045",
        "position_id": "NP-0045",
        "text": "There are two kinds of workaholics. Here one must distinguish between two kinds of workaholics.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Compulsive Behavior",
        "subcategory": "Workaholism"
    },
    {
        "id": "NP-0046",
        "position_id": "NP-0046",
        "text": "The workaholic who loves what he is doing works because he wants to work. There is the workaholic who loves what he is doing: this person works because he wants to work.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Compulsive Behavior",
        "subcategory": "Workaholism"
    },
    {
        "id": "NP-0047",
        "position_id": "NP-0047",
        "text": "The workaholic who hates what he is doing works because he doesn't want to work. Then there is the workaholic who hates what he is doing: this person works because he doesn't want to work.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Compulsive Behavior",
        "subcategory": "Workaholism"
    },
    {
        "id": "NP-0048",
        "position_id": "NP-0048",
        "text": "The workaholic who loves his work is not working compulsively. The workaholic who loves his work is not working compulsively, and this form of workaholism is not about avoidance.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Compulsive Behavior",
        "subcategory": "Workaholism"
    },
    {
        "id": "NP-0049",
        "position_id": "NP-0049",
        "text": "The workaholic who hates his work is working compulsively. But the workaholic who hates his work is working compulsively, and this form of workaholism is about avoidance.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Compulsive Behavior",
        "subcategory": "Workaholism"
    },
    {
        "id": "NP-0050",
        "position_id": "NP-0050",
        "text": "The workaholic who hates his work is avoiding doing what he wants to do. This type of workaholic is avoiding doing what he wants to do, and because he hates what he is doing, he has to do it compulsively.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Compulsive Behavior",
        "subcategory": "Workaholism"
    },
    {
        "id": "NP-0051",
        "position_id": "NP-0051",
        "text": "Stuttering is about not speaking with a single voice. Stuttering is about not speaking with a single voice.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Speech Disorders",
        "subcategory": "Stuttering"
    },
    {
        "id": "NP-0052",
        "position_id": "NP-0052",
        "text": "Two distinct currents of thought attempt to control one's speech in stuttering. Two distinct currents of thought are attempting to control one's speech.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Speech Disorders",
        "subcategory": "Stuttering"
    },
    {
        "id": "NP-0053",
        "position_id": "NP-0053",
        "text": "To the extent that these two thought-currents are evenly matched, one stutters. To the extent that these two thought-currents are evenly matched, one stutters.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Speech Disorders",
        "subcategory": "Stuttering"
    },
    {
        "id": "NP-0054",
        "position_id": "NP-0054",
        "text": "To the extent that one of these thought currents dominates the other, speech is normal. To the extent that one of these thought currents dominates the other, speech is normal.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Speech Disorders",
        "subcategory": "Stuttering"
    },
    {
        "id": "NP-0055",
        "position_id": "NP-0055",
        "text": "Men are self-contained and women are not. Men are self-contained and woman are not. That is the difference between men and women.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Gender Differences"
    },
    {
        "id": "NP-0056",
        "position_id": "NP-0056",
        "text": "Men who are not self-contained are not really men. Obviously there are men who are not self-contained and there are women who are self-contained. But such men are not really men, and such women are not really women.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Gender Differences"
    },
    {
        "id": "NP-0057",
        "position_id": "NP-0057",
        "text": "Women who are self-contained are not really women. Obviously there are men who are not self-contained and there are women who are self-contained. But such men are not really men, and such women are not really women.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Gender Psychology",
        "subcategory": "Gender Differences"
    },
    {
        "id": "NP-0058",
        "position_id": "NP-0058",
        "text": "One learns from adversity, not from failure. One learns from adversity, not from failure.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Adversity vs Failure"
    },
    {
        "id": "NP-0059",
        "position_id": "NP-0059",
        "text": "One learns more from failure than from success is a common but false claim. That one learns more from failure than from success.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Adversity vs Failure"
    },
    {
        "id": "NP-0060",
        "position_id": "NP-0060",
        "text": "One does not learn more from failure than from success. This is not true.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Adversity vs Failure"
    },
    {
        "id": "NP-0061",
        "position_id": "NP-0061",
        "text": "Success opens up new and unforeseen vistas. Each success opened up new and completely unforeseen vistas.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Success"
    },
    {
        "id": "NP-0062",
        "position_id": "NP-0062",
        "text": "Failure is a dead end from which one learns nothing. Each failure was nothing but a dead end, from which I learned nothing, except that what I was doing led to a dead end.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Adversity vs Failure"
    },
    {
        "id": "NP-0063",
        "position_id": "NP-0063",
        "text": "One learns nothing from failure. One learns nothing from failure.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Adversity vs Failure"
    },
    {
        "id": "NP-0064",
        "position_id": "NP-0064",
        "text": "One learns from adversity. One learns from adversity.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Adversity vs Failure"
    },
    {
        "id": "NP-0065",
        "position_id": "NP-0065",
        "text": "Failure is not adversity. Failure is not adversity.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Adversity vs Failure"
    },
    {
        "id": "NP-0066",
        "position_id": "NP-0066",
        "text": "Failure is the end-result of adversity not triumphed over. Failure is the end-result of adversity that was not triumphed over.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Learning and Growth",
        "subcategory": "Adversity vs Failure"
    },
    {
        "id": "NP-0067",
        "position_id": "NP-0067",
        "text": "Everybody wants money. Does everybody want money? Yes. Everybody.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Motivation",
        "subcategory": "Money"
    },
    {
        "id": "NP-0068",
        "position_id": "NP-0068",
        "text": "Monks, scholars, writers, and 'starving artists' who seem to spurn money still want money. That is itself a way of wanting money.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Motivation",
        "subcategory": "Money"
    },
    {
        "id": "NP-0069",
        "position_id": "NP-0069",
        "text": "The attitude of a scholar living in squalid conditions towards money is like a jilted lover. His attitude towards money is that of a jilted and petulant lover.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Motivation",
        "subcategory": "Money"
    },
    {
        "id": "NP-0070",
        "position_id": "NP-0070",
        "text": "Overblown feelings are the opposite of what they are supposed to be. Overblown feelings are the opposite of what they are supposed to be.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Emotions",
        "subcategory": "Emotional Authenticity"
    },
    {
        "id": "NP-0071",
        "position_id": "NP-0071",
        "text": "Emotions that are what they seem to be are not intensely scrutinized by those who have them. Emotions that are what they seem to be are not the objects of intense scrutiny on the part of those who have them.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Emotions",
        "subcategory": "Emotional Authenticity"
    },
    {
        "id": "NP-0072",
        "position_id": "NP-0072",
        "text": "Attitudes pressed into tendentious narratives about oneself are the opposite of what they seem. Attitudes that are pressed into the service of tendentious narratives about oneself are the opposite of what they seem to be.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Emotions",
        "subcategory": "Emotional Authenticity"
    },
    {
        "id": "NP-0073",
        "position_id": "NP-0073",
        "text": "The #1 Rule of Writing is to immediately write down every thought. The Number #1 Rule of Writing is that one must immediately write down every thought that occurs to one.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Creativity",
        "subcategory": "Writing"
    },
    {
        "id": "NP-0074",
        "position_id": "NP-0074",
        "text": "If one waits to write down a thought, the moment will pass. If one waits, the moment will pass, never to be recovered.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Creativity",
        "subcategory": "Writing"
    },
    {
        "id": "NP-0075",
        "position_id": "NP-0075",
        "text": "Memorizing a thought is irrelevant because the original idea is a foil for unconscious ideas. It is irrelevant that one should 'memorize' what it is that one wanted to say, since the idea that originally came to mind was merely a foil for a constellation of unconscious ideas.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Creativity",
        "subcategory": "Writing"
    },
    {
        "id": "NP-0076",
        "position_id": "NP-0076",
        "text": "The Number #1 rule of writing is complete honesty. Elsewhere I have said that the Number #1 rule of writing is complete honest.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Creativity",
        "subcategory": "Writing"
    },
    {
        "id": "NP-0077",
        "position_id": "NP-0077",
        "text": "Following the rule of immediately writing down thoughts makes one an honest writer. If one follows the above-stated injunction, one is ipso facto an honest writer.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Creativity",
        "subcategory": "Writing"
    },
    {
        "id": "NP-0078",
        "position_id": "NP-0078",
        "text": "Lack of coordination is due to a failure to be centered. Lack of coordination has to do with a failure to be centered, which in turn has to do with a failure to have an objective that one truly believes in.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Mind-Body",
        "subcategory": "Coordination"
    },
    {
        "id": "NP-0079",
        "position_id": "NP-0079",
        "text": "Lack of physical coordination is a manifestation of lack of psychological coordination. Lack of physical coordination is accompanied by, since it is a manifestation of, a lack of psychological coordination.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Mind-Body",
        "subcategory": "Coordination"
    },
    {
        "id": "NP-0080",
        "position_id": "NP-0080",
        "text": "A psychological condition is pathological if it restricts freedom. A given psychological condition is pathological if it restricts freedom and non-pathological if it does not.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Freedom and Pathology"
    },
    {
        "id": "NP-0081",
        "position_id": "NP-0081",
        "text": "A condition is counter-pathological if it augments freedom. A given condition is positively counter-pathological if it augments freedom, even if it is unusual or even unique.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Psychopathology",
        "subcategory": "Freedom and Pathology"
    },
    {
        "id": "NP-0082",
        "position_id": "NP-0082",
        "text": "The #1 Rule of Business is to do what comes naturally. The #1 Rule rule of business is that you must do what comes naturally to you.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Business Psychology",
        "subcategory": "Success"
    },
    {
        "id": "NP-0083",
        "position_id": "NP-0083",
        "text": "One must not go against their own nature in business. You must not go against your own grain.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Business Psychology",
        "subcategory": "Success"
    },
    {
        "id": "NP-0084",
        "position_id": "NP-0084",
        "text": "Working hard against one's nature leads to failure in business. You must work hard, but you must not work hard fighting your own nature.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Business Psychology",
        "subcategory": "Success"
    },
    {
        "id": "NP-0085",
        "position_id": "NP-0085",
        "text": "Writer's block only afflicts those not writing from the heart. Just as writer's block only afflicts those who are not writing from the heart, so 'entrepreneur's block' only afflicts those who are not working from the heart.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Creativity",
        "subcategory": "Writer's Block"
    },
    {
        "id": "NP-0086",
        "position_id": "NP-0086",
        "text": "Entrepreneur's block only afflicts those not working from the heart. So 'entrepreneur's block' only afflicts those who are not working from the heart.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Business Psychology",
        "subcategory": "Success"
    },
    {
        "id": "NP-0087",
        "position_id": "NP-0087",
        "text": "Choosing a path because it aligns with who you are leads to success. When people choose a given path because it is who they are, they succeed.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Business Psychology",
        "subcategory": "Success"
    },
    {
        "id": "NP-0088",
        "position_id": "NP-0088",
        "text": "Choosing a path because of an agenda leads to failure. When they do so because they have an agenda, they do not.",
        "work": "Neurosis vs Psychosis",
        "domain": "PSYCHOLOGY",
        "category": "Business Psychology",
        "subcategory": "Success"
    }
]

def add_positions_to_database():
    db_path = "data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json"
    
    with open(db_path, 'r') as f:
        database = json.load(f)
    
    initial_count = len(database["positions"])
    print(f"Initial position count: {initial_count}")
    
    existing_ids = {p.get("id") or p.get("position_id") for p in database["positions"]}
    
    added = 0
    for pos in neurosis_psychosis_positions:
        if pos["id"] not in existing_ids:
            database["positions"].append(pos)
            added += 1
    
    final_count = len(database["positions"])
    print(f"Added {added} new positions")
    print(f"Final position count: {final_count}")
    
    database["metadata"] = database.get("metadata", {})
    database["metadata"]["last_updated"] = datetime.now().isoformat()
    database["metadata"]["total_positions"] = final_count
    database["metadata"]["neurosis_psychosis_positions"] = len(neurosis_psychosis_positions)
    
    with open(db_path, 'w') as f:
        json.dump(database, f, indent=2)
    
    print(f"Database saved to {db_path}")
    return added

if __name__ == "__main__":
    add_positions_to_database()
