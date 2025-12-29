"""
Phase A - Resume Classification Model Training
This script trains a simple ML model using 20
resumes (PDF/DOCX) + labels.csv and creates two
files: resume_classifier.joblib (Logistic Regression
classifier) embed_model.joblib (sentence-
transformers embedding model) We will then use
this in app.py to predict selected/rejected for a
new resume.
"""

import os
import csv
import joblib

from PyPDF2 import PdfReader
import docx
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# === PATHS ===
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "training_data")
RESUME_DIR = os.path.join(DATA_DIR, "resumes")
LABEL_FILE = os.path.join(DATA_DIR, "labels.csv")


# === STEP 1: Resume text extractor (same logic as app.py) ===
def extract_text_from_file(file_path: str) -> str:
    ext = file_path.rsplit(".", 1)[1].lower()

    if ext == "pdf":
        text_chunks = []
        try:
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    text_chunks.append(page_text)
        except Exception as e:
            print("PDF parse error:", e)
            return ""
        return "\n".join(text_chunks)

    elif ext == "docx":
        try:
            d = docx.Document(file_path)
            return "\n".join(p.text for p in d.paragraphs)
        except Exception as e:
            print("DOCX parse error:", e)
            return ""

    else:
        # अन्य formats साठी support नाही
        return ""


# === STEP 2: Dataset load करणे ===
def load_dataset():
    texts = []
    labels = []

    if not os.path.exists(LABEL_FILE):
        raise FileNotFoundError(f"labels.csv not found at {LABEL_FILE}")

    with open(LABEL_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row["filename"].strip()
            label = row["label"].strip()

            resume_path = os.path.join(RESUME_DIR, filename)
            if not os.path.exists(resume_path):
                print(f"[WARN] Resume file not found: {resume_path}, skipping")
                continue

            text = extract_text_from_file(resume_path)
            if not text.strip():
                print(f"[WARN] Empty text extracted from: {resume_path}, skipping")
                continue

            texts.append(text)
            labels.append(label)

    print(f"[INFO] Loaded {len(texts)} resumes with labels")
    return texts, labels


def main():
    # 1) Load data
    texts, labels = load_dataset()
    if len(texts) < 5:
        print("[ERROR] Too few resumes to train a model. Add more data.")
        return

    # 2) Load embedding model
    print("[INFO] Loading sentence-transformers model...")
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    print("[INFO] Creating embeddings...")
    X = embed_model.encode(texts)   # shape: (N, dim)
    y = labels

    # 3) Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4) Train classifier
    print("[INFO] Training Logistic Regression classifier...")
    clf = LogisticRegression(max_iter=500)
    clf.fit(X_train, y_train)

    # 5) Evaluate
    y_pred = clf.predict(X_test)
    print("\n=== Classification Report (Validation Set) ===")
    print(classification_report(y_test, y_pred))

    # 6) Save models
    model_path = os.path.join(BASE_DIR, "resume_classifier.joblib")
    embed_path = os.path.join(BASE_DIR, "embed_model.joblib")

    joblib.dump(clf, model_path)
    joblib.dump(embed_model, embed_path)

    print(f"\n[SAVED] Classifier -> {model_path}")
    print(f"[SAVED] Embedding model -> {embed_path}")
    print("[DONE] Training pipeline finished.")


if __name__ == "__main__":
    main()
