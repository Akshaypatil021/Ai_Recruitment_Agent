import re

BEHAVIOUR_PATTERNS = {
    "leadership": r"(led|managed|supervised|team lead|mentored|organized|guided)",
    "communication": r"(presented|communicated|collaborated|client interaction|stakeholder)",
    "problem_solving": r"(debugged|optimized|resolved|diagnosed|analyzed)",
    "teamwork": r"(worked with|collaborated|team|cross-functional)",
    "self_learning": r"(self learned|self-taught|certification|training|bootcamp|hackathon)",
    "innovation": r"(built|developed|designed|created|invented|prototype)",
}

PROJECT_INDICATORS = [
    "project",
    "implemented",
    "built",
    "created",
    "developed",
    "designed",
]

def infer_candidate_traits(resume_text):
    text = resume_text.lower()

    inferred_traits = []

    for trait, pattern in BEHAVIOUR_PATTERNS.items():
        if re.search(pattern, text):
            inferred_traits.append(trait)

    return inferred_traits

def detect_project_based_profile(resume_text):
    """Detect if candidate is execution/project oriented or theory oriented"""
    text = resume_text.lower()

    project_hits = sum(1 for word in PROJECT_INDICATORS if word in text)

    if project_hits >= 3:
        return "project_oriented"
    elif project_hits >= 1:
        return "balanced"
    else:
        return "theoretical"
