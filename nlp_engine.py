import spacy
import nltk
from nltk.corpus import stopwords

# Load NLP models
try:
    nltk.data.find("corpora/stopwords")
except:
    nltk.download("stopwords")

nlp = spacy.load("en_core_web_sm")
STOPWORDS = set(stopwords.words("english"))

def preprocess_text(text: str):
    """Convert resume into cleaned NLP tokens."""
    doc = nlp(text.lower())
    tokens = []

    for token in doc:
        if token.is_stop or token.is_punct or token.text in STOPWORDS:
            continue
        tokens.append(token.lemma_)
    
    return set(tokens)

def detect_skills_nlp(resume_text: str, domain_skills: list):
    """
    Receive NLP tokens and detect found/missing skills
    """
    resume_tokens = preprocess_text(resume_text)

    found = []
    missing = []

    for skill in domain_skills:
        skill_variants = {
            skill.lower(),
            skill.lower().replace(" ", "")
        }

        if any(variant in resume_tokens for variant in skill_variants):
            found.append(skill)
        else:
            missing.append(skill)

    return found, missing
