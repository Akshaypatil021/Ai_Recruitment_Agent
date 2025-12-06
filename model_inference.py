# model_inference.py

import os
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict, Any
from skill_config import DOMAIN_SKILLS, QUESTION_BANK

BASE_DIR = os.path.dirname(__file__)

# paths to saved models
CLASSIFIER_PATH = os.path.join(BASE_DIR, "resume_classifier.joblib")
EMBED_MODEL_PATH = os.path.join(BASE_DIR, "embed_model.joblib")

# Load embedding model आणि classifier
EMBED_MODEL = joblib.load(EMBED_MODEL_PATH)           # SentenceTransformer object save केला होता
CLASSIFIER = joblib.load(CLASSIFIER_PATH)            # LogisticRegression

LABELS = CLASSIFIER.classes_.tolist()                # ['rejected', 'selected'] असे काहीतरी

def predict_score_and_label(resume_text: str):
    """
    दिलेल्या resume_text साठी:
    - embedding काढतो
    - classifier ने selected/rejected predict करतो
    - max probability score परत करतो
    """
    if not resume_text.strip():
        # text नाही तर direct reject सारखं हाताळ
        return 0.0, "rejected", []

    # (1, dim) embedding
    emb = EMBED_MODEL.encode([resume_text])
    # probabilities for each label
    probs = CLASSIFIER.predict_proba(emb)[0]   # e.g. [0.2, 0.8]
    best_idx = int(np.argmax(probs))
    label = LABELS[best_idx]
    score = float(probs[best_idx])            # 0–1

    return score, label, probs.tolist()

# ------- SKILL + RULE BASED AI LAYER (NEW) ---------

def detect_skills(resume_text: str, domain: str) -> Tuple[List[str], List[str]]:
    text = resume_text.lower()
    domain_skill_list = DOMAIN_SKILLS.get(domain, [])
    
    found = []
    missing = []

    for skill in domain_skill_list:
        if skill.lower() in text:
            found.append(skill)
        else:
            missing.append(skill)

    return found, missing


def generate_skill_based_questions(matched_skills: List[str]) -> List[str]:
    questions: List[str] = []

    for skill in matched_skills:
        qs = QUESTION_BANK.get(skill.lower())
        if qs:
            questions.extend(qs)

    if not questions:
        questions = [
            "Tell me about yourself professionally.",
            "What was your toughest project and why?",
            "What skill do you want to improve and how?"
        ]

    return questions

def run_analysis(
    *,
    candidate_id: str,
    resume_text: str,
    domain: str,
    resume_path: str | None = None,
    name: str | None = None,
    email: str | None = None,
    source: str = "candidate_portal",
) -> Dict[str, Any]:

    # ---- ML Prediction ----
    ml_score, ml_label, _ = predict_score_and_label(resume_text)

    # ---- Skill Match reasoning ----
    found_skills, missing_skills = detect_skills(resume_text, domain)

    total = len(found_skills) + len(missing_skills)
    rule_score = len(found_skills) / total if total > 0 else 0.0

    # Combine ML + rule score
    final_score = round((ml_score + rule_score) / 2, 2)

    selected = ml_label == "selected"

    # ---- Strength & Improvements ----
    strengths = (
        [f"You already know: {', '.join(found_skills)}"]
        if found_skills else
        ["No strong domain-specific skills detected."]
    )

    improvements = (
        [f"Improve in: {', '.join(missing_skills)}"]
        if missing_skills else
        ["You covered major skills for this domain!"]
    )

    # ---- AI-based Q generation ----
    questions = generate_skill_based_questions(found_skills)

    analysis = {
        "candidate_id": candidate_id,
        "name": name,
        "email": email,
        "source": source,
        "domain": domain,
        "resume_path": resume_path,
        "resume_text": resume_text,
        "score": final_score,        # ML + rule score blend
        "ml_score": ml_score,
        "rule_score": rule_score,
        "selected": selected,
        "matched_skills": found_skills,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "improvements": improvements,
        "questions": questions,
    }

    return analysis
