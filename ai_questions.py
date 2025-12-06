# ai_questions.py
"""
Ollama (llama3:latest) वापरून interview questions + improvement tips generate करणारा module.
"""

import os
import json
import re
import requests

# Ollama server config
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3:latest")


def _parse_json_from_content(content: str):
    """
    काही वेळा model pure JSON न देता extra text देतो,
    म्हणून content मधून JSON भाग शोधून parse करतो.
    """
    content = content.strip()

    # 1) direct JSON try
    try:
        return json.loads(content)
    except Exception:
        pass

    # 2) ```json ...``` ब्लॉक असेल तर
    m = re.search(r"```json(.*?)```", content, re.DOTALL | re.IGNORECASE)
    if m:
        block = m.group(1).strip()
        return json.loads(block)

    # 3) पहिल्या { ते शेवटच्या } पर्यंत
    m2 = re.search(r"\{.*\}", content, re.DOTALL)
    if m2:
        block = m2.group(0)
        return json.loads(block)

    # fail
    raise ValueError("No valid JSON found in model content")


def _domain_fallback_questions(domain: str):
    domain = (domain or "").lower()
    if "data" in domain:
        return [
            "Explain one data project from your resume in detail.",
            "How did you handle missing values in your dataset?",
            "Which evaluation metric did you use and why?",
            "Describe a time when your model did not work as expected.",
            "How do you decide which features are important?"
        ]
    if "web" in domain:
        return [
            "Walk me through one web app you built.",
            "How did you handle authentication and authorization?",
            "What performance optimisations did you implement?",
            "Explain a layout or responsiveness issue you solved.",
            "How did you connect frontend and backend?"
        ]
    if "software" in domain:
        return [
            "Describe the architecture of one software project you worked on.",
            "How did you manage version control and branching?",
            "Explain a bug that was hard to debug and how you fixed it.",
            "How do you ensure code quality in your projects?",
            "What design patterns have you used?"
        ]
    # generic
    return [
        "Tell me about one project from your resume in detail.",
        "Which skill from your resume do you want to improve first, and why?",
        "Describe a situation where you faced a difficult technical challenge.",
        "How do you usually learn a new technology?",
        "Tell me about a time you worked in a team."
    ]


def generate_ai_questions(analysis: dict):
    """
    analysis = CANDIDATE_ANALYSIS[candidate_id]
    Return: (questions_list, improvements_list)
    """

    resume_text = (analysis.get("resume_text") or "")[:4000]
    domain = analysis.get("domain") or "general"
    score = analysis.get("score") or 0
    strengths = analysis.get("strengths") or []
    improvements = analysis.get("improvements") or []

    system_prompt = (
        "You are an unbiased technical interviewer for an AI recruitment system. "
        "You see a candidate's resume, model score and skill analysis, and you must "
        "generate interview questions and improvement tips.\n\n"
        "IMPORTANT: You MUST respond with ONLY valid JSON in this exact format:\n"
        '{"questions": ["q1", "q2", "..."], "improvements": ["tip1", "tip2", "..."]}\n'
        "No extra text, no explanation outside the JSON."
    )

    user_prompt = f"""
Candidate domain: {domain}
Model score (0-1): {score}

Strengths detected:
{strengths}

Improvement areas detected:
{improvements}

Resume text:
\"\"\"{resume_text}\"\"\"

Generate:
- 5 focused, domain-specific interview questions
- 3 very practical improvement tips
Return ONLY JSON with keys "questions" and "improvements".
"""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        content = data["message"]["content"]

        parsed = _parse_json_from_content(content)

        questions = parsed.get("questions", [])
        improv = parsed.get("improvements", [])

        if not isinstance(questions, list):
            questions = [str(questions)]
        if not isinstance(improv, list):
            improv = [str(improv)]

        # किमान 5 questions enforce कर
        if len(questions) < 5:
            extra = _domain_fallback_questions(domain)
            # जे अस्तित्वात नाहीत तेच add कर
            for q in extra:
                if q not in questions:
                    questions.append(q)
                if len(questions) >= 5:
                    break

        return questions, improv

    except Exception as e:
        print("Error talking to Ollama / parsing JSON:", e)
        # Fallback – आता domain-specific fallback
        fallback_q = _domain_fallback_questions(domain)
        fallback_improv = [
            "Add more measurable impact to your project descriptions.",
            "Include links to GitHub or live demos wherever possible.",
            "Focus on strengthening 1–2 core skills instead of many shallow ones.",
        ]
        return fallback_q, fallback_improv
