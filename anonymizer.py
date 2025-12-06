# anonymizer.py
"""
Resume मधून bias निर्माण करणारी माहिती काढण्यासाठी simple anonymizer.

काय काढतो:
- Email
- Phone numbers
- Name / DOB / Address सारख्या lines (keywords वरून)
- Mr./Ms./Mrs./Shri type titles

हे perfect नाही, पण bias कमी करण्यासाठी पुरेसं आहे (college project level).
"""

import re

EMAIL_PATTERN = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
PHONE_PATTERN = re.compile(r"(\+?\d[\d\-\s]{8,}\d)")  # लांब digit sequence
TITLE_PATTERN = re.compile(r"\b(Mr\.?|Mrs\.?|Ms\.?|Miss|Shri|Smt\.?)\b", re.IGNORECASE)


def anonymize_resume(text: str) -> str:
    if not text:
        return text

    # 1) email → [EMAIL]
    text = EMAIL_PATTERN.sub("[EMAIL]", text)

    # 2) phone → [PHONE]
    text = PHONE_PATTERN.sub("[PHONE]", text)

    # 3) titles remove (Mr/Ms/Mrs/Shri etc.)
    text = TITLE_PATTERN.sub("[TITLE]", text)

    # 4) line-wise processing for Name/Address/DOB etc.
    lines = text.splitlines()
    clean_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # खूप simple rules: Name / Address / DOB ने सुरू होणाऱ्या lines काढून टाक
        lowered = stripped.lower()
        if lowered.startswith("name:") or lowered.startswith("full name:"):
            clean_lines.append("Name: [ANONYMIZED]")
            continue

        if lowered.startswith("dob") or lowered.startswith("date of birth"):
            clean_lines.append("DOB: [ANONYMIZED]")
            continue

        if lowered.startswith(("address", "location", "current address", "permanent address")):
            clean_lines.append("Address: [ANONYMIZED]")
            continue

        # पहिल्या 3–4 lines मधली जास्त capital असलेली छोटी line name असण्याची शक्यता असते
        if i <= 3 and 1 <= len(stripped.split()) <= 4:
            # letters जास्त आणि digits नाहीत तर आपण मानतो की ही नावाची line असेल
            if any(c.isalpha() for c in stripped) and not any(c.isdigit() for c in stripped):
                clean_lines.append("[CANDIDATE NAME]")
                continue

        clean_lines.append(line)

    return "\n".join(clean_lines)
