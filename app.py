import os
import uuid
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
)
from PyPDF2 import PdfReader
import docx  # from python-docx

from werkzeug.utils import secure_filename
from skill_config import DOMAIN_SKILLS, QUESTION_BANK
from nlp_engine import detect_skills_nlp   # (आत्ता use नसला तरी ठेवू)
from insights_engine import infer_candidate_traits, detect_project_based_profile
from model_inference import predict_score_and_label
from ai_questions import generate_ai_questions
from anonymizer import anonymize_resume
from db_models import init_db, save_candidate_summary, fetch_candidates_with_stats
from model_inference import predict_score_and_label


app = Flask(__name__)

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

# simple in-memory "DB"
CANDIDATE_ANALYSIS = {}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(file_path: str) -> str:
    """
    Resume मधून text extract करणारी helper.
    PDF आणि DOCX properly handle करतो.
    .doc साठी simple message.
    """
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

    elif ext == "doc":
        # old Word format – extra libs नको म्हणून simple
        return "[INFO] .doc format not fully supported. Please upload PDF or DOCX for better analysis."

    else:
        return ""


# ---------- SIMPLE SKILL MATCH HELPER ----------
def detect_skills(resume_text: str, domain: str):
    """
    DOMAIN_SKILLS वरून resume मधले skills शोधतो.
    return: (found_skills, missing_skills)
    """
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


# ---------- PAGE ROUTES ----------

@app.route("/")
def root():
    return redirect("/index.html")


@app.route("/index.html")
def index_page():
    return render_template("index.html")


@app.route("/skills.html")
def skills_page():
    return render_template("skills.html")


@app.route("/questions.html")
def questions_page():
    return render_template("questions.html")


@app.route("/reports.html")
def reports_page():
    return render_template("reports.html")

@app.route("/hr/selected")
def hr_selected():
    return render_template("HR/selected.html")


@app.route("/hr/bulk-upload")
def hr_bulk_upload():
    return render_template("HR/bulk_upload.html")

# ---------- API: ANALYZE RESUME ----------

@app.route("/api/analyze_resume", methods=["POST"])
def analyze_resume():
    """
    Expect form-data:
      - name: candidate name (optional पण आपण पाठवतो)
      - email: candidate email
      - resume: file
      - domain: string (e.g., data_science)
    """
    file = request.files.get("resume")
    domain = request.form.get("domain")
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()

    if file is None or file.filename == "":
        return jsonify({"error": "No resume file provided."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use PDF, DOC or DOCX."}), 400

    if not domain:
        return jsonify({"error": "Job domain is required."}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    candidate_id = str(uuid.uuid4())

    # 🔹 1) RESUME TEXT EXTRACT
    raw_resume_text = extract_text_from_file(save_path)

    # 🔹 1.1 Bias removal – anonymize personal details
    resume_text = anonymize_resume(raw_resume_text)

    print("\n=== RESUME TEXT PREVIEW (ANONYMIZED) ===")
    print(resume_text[:500])
    print("========================================\n")

    # 🔹 2) MODEL-BASED SCORE & LABEL
    # returns: (score_0_to_1, label_string, prob_vector)
    ml_score, quality_label, prob_vector = predict_score_and_label(resume_text)

    # 🔹 3) domain-wise default courses/projects
    domain_profiles = {
        "software_engineer": {
            "courses": [
                "Data Structures & Algorithms mastery",
                "Clean Code + SOLID principles",
                "Object-Oriented System Design Basics",
            ],
            "projects": [
                "Build a REST API with authentication",
                "Low-level design of a feature (e.g., Library Management, Parking System)",
            ],
        },

        "data_science": {
            "courses": [
                "Machine Learning with Scikit-Learn & TensorFlow",
                "Statistics for Data Science",
                "Data Visualization (Matplotlib / PowerBI)",
            ],
            "projects": [
                "Kaggle classification/regression model with report",
                "Mini project on sentiment analysis or recommendation system",
            ],
        },

        "web_development": {
            "courses": [
                "React or Angular from scratch",
                "Backend APIs with Node/Python",
                "UI/UX fundamentals",
            ],
            "projects": [
                "Full-stack CRUD application with login",
                "Responsive animated portfolio site",
            ],
        },

        "devops_cloud": {
            "courses": [
                "Linux + Bash scripting",
                "Docker + Kubernetes basics",
                "CI/CD pipeline fundamentals",
            ],
            "projects": [
                "Deploy an app on AWS/GCP/Azure",
                "CI/CD automation project (GitHub Actions/Jenkins)",
            ],
        },

        "ui_ux": {
            "courses": [
                "Figma / Adobe XD Masterclass",
                "Wireframing + Prototyping workflows",
                "Color theory + typography",
            ],
            "projects": [
                "Design system for a SaaS dashboard",
                "Mobile app prototype with usability testing",
            ],
        },

        "product_management": {
            "courses": [
                "Agile + Scrum essentials",
                "Roadmap planning & prioritization",
                "Stakeholder communication",
            ],
            "projects": [
                "Create PRD + mockups for a new app",
                "Build product roadmap for a business problem",
            ],
        },

        "cybersecurity": {
            "courses": [
                "Ethical hacking fundamentals",
                "Network security basics",
                "OWASP Top 10",
            ],
            "projects": [
                "Vulnerability assessment report",
                "Secure API security audit mini project",
            ],
        },

        "business_analyst": {
            "courses": [
                "SQL fundamentals",
                "Flow diagrams + BRD writing",
                "Requirements lifecycle documentation",
            ],
            "projects": [
                "Case study – requirement analysis for an HR system",
                "Dashboard + reporting implementation",
            ],
        },

        "digital_marketing": {
            "courses": [
                "SEO + Google Analytics",
                "Content + Social media strategy",
                "Paid campaign optimization",
            ],
            "projects": [
                "Run a real/Mock campaign and analyse metrics",
                "SEO analysis + strategy report",
            ],
        },

        "hr_talent": {
            "courses": [
                "HR communication & interviewing",
                "Screening + JD drafting",
                "Excel + ATS basics",
            ],
            "projects": [
                "Create full hiring pipeline for a role",
                "End-to-end onboarding process workflow",
            ],
        },
    }

    profile = domain_profiles.get(domain)
    if profile is None:
        # safety fallback – जर domain चुकीचा आला तर generic वापरू
        profile = {
            "courses": ["Take 1–2 structured online courses focused on this domain."],
            "projects": ["Build at least one strong portfolio project in this domain."],
        }

    # 🔹 4) Smart Scoring + Strength Mapping (NLP skills + model score)

    # 4a) skills (simple keyword-based)
    found_skills, missing_skills = detect_skills(resume_text, domain)

    # 4b) traits + profile-type (from insights_engine)
    try:
        traits = infer_candidate_traits(resume_text) or []
    except Exception as e:
        print("traits error:", e)
        traits = []

    try:
        # adjust signature if your function expects different args
        profile_type = detect_project_based_profile(resume_text, found_skills)
    except TypeError:
        # fallback if it only needs text
        profile_type = detect_project_based_profile(resume_text)
    except Exception as e:
        print("profile_type error:", e)
        profile_type = None

    # score purely from model
    score = ml_score
    selected = (quality_label == "selected")

    # Strengths = found skills
    strengths = (
        [f"You already know: {', '.join(found_skills)}"]
        if found_skills
        else ["No domain matching skills detected yet."]
    )

    # Improvements = missing skills
    improvements = (
        [f"Improve in: {', '.join(missing_skills)}"]
        if missing_skills
        else ["You covered all skills for this domain!"]
    )

    # 🔹 5) Build interview questions (base – नंतर llama3 वरून अजून येतील)
    questions = []

    # 5a) skill-based questions
    for skill in found_skills:
        qs = QUESTION_BANK.get(skill.lower(), [])
        questions.extend(qs)

    # 5b) personality/profile-based questions
    if profile_type == "project_oriented":
        questions.append("Explain a complex project you built end-to-end.")
        questions.append("What was your biggest architecture decision?")
    elif profile_type == "balanced":
        questions.append("Explain how you applied theory into projects.")
    elif profile_type == "theory_oriented":
        questions.append("You seem theory-strong — how do you plan to build real projects?")

    # 5c) soft skill–based questions
    traits_lower = {t.lower() for t in traits}

    if "leadership" in traits_lower:
        questions.append("Describe a time when you led a team.")
    if "communication" in traits_lower:
        questions.append("How do you handle client communication?")
    if "problem_solving" in traits_lower or "problem-solving" in traits_lower:
        questions.append("Tell me about a difficult technical bug you solved.")

    # जर काही प्रश्न मिळाले नाहीत तर generic fallback
    if not questions:
        questions = [
            "Tell me about yourself professionally.",
            "What major project are you most proud of?",
            "How do you handle problem solving?",
        ]

    # 🔹 6) Final analysis object
    analysis = {
        "candidate_id": candidate_id,
        "name": name,
        "email": email,
        "domain": domain,
        "resume_path": save_path,
        "resume_text": resume_text,
        "score": round(score, 2),
        "selected": selected,
        "model_label": quality_label,
        "model_prob_vector": prob_vector,
        "matched_skills": found_skills,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "improvements": improvements,
        "suggested_courses": profile["courses"],
        "suggested_projects": profile["projects"],
        "questions": questions,
        "profile_type": profile_type,
        "personality_traits": traits,
    }

    # in-memory + DB save
    CANDIDATE_ANALYSIS[candidate_id] = analysis
    save_candidate_summary(analysis)

    return jsonify(
        {
            "candidate_id": candidate_id,
            "score": round(score, 2),
            "selected": selected,
            "matched_skills": found_skills,
            "message": "Resume uploaded and analyzed with ML-based scoring.",
        }
    )


# ---------- API: SKILL REPORT ----------

@app.route("/api/skill_report", methods=["GET"])
def skill_report():
    candidate_id = request.args.get("candidate_id")
    if not candidate_id:
        return jsonify({"error": "candidate_id is required as a query parameter."}), 400

    analysis = CANDIDATE_ANALYSIS.get(candidate_id)
    if analysis is None:
        return jsonify({"error": "No analysis found for this candidate_id."}), 404

    return jsonify(
        {
            "candidate_id": candidate_id,
            "domain": analysis.get("domain"),
            "score": analysis.get("score"),
            "selected": analysis.get("selected"),
            "model_label": analysis.get("model_label"),
            "strengths": analysis.get("strengths", []),
            "improvements": analysis.get("improvements", []),
            "suggested_courses": analysis.get("suggested_courses", []),
            "suggested_projects": analysis.get("suggested_projects", []),
            "profile_type": analysis.get("profile_type"),
            "personality_traits": analysis.get("personality_traits", []),
        }
    )


# ---------- API: QUESTIONS (Ollama llama3) ----------

@app.route("/api/questions", methods=["GET"])
def get_questions():
    """
    Candidate च्या analysis वरून Ollama llama3 कडून live questions + improvements आणतो.
    """
    candidate_id = request.args.get("candidate_id")
    if not candidate_id:
        return jsonify({"error": "candidate_id is required as a query parameter."}), 400

    analysis = CANDIDATE_ANALYSIS.get(candidate_id)
    if analysis is None:
        return jsonify({"error": "No analysis found for this candidate_id."}), 404

    # 🔥 llama3 कडून fresh AI questions
    questions, improv = generate_ai_questions(analysis)

    return jsonify(
        {
            "candidate_id": candidate_id,
            "domain": analysis.get("domain"),
            "questions": questions,
            "improvements": improv,
        }
    )


# ---------- API: CANDIDATES LIST + STATS ----------

@app.route("/api/candidates", methods=["GET"])
def list_candidates():
    """
    HR / reporting साठी – latest candidates + basic stats.
    Optional query param: ?limit=50
    """
    try:
        limit = int(request.args.get("limit", 50))
    except ValueError:
        limit = 50

    rows, stats = fetch_candidates_with_stats(limit=limit)

    return jsonify(
        {
            "candidates": rows,
            "stats": {
                "total": stats["total"],
                "selected": stats["selected"],
                "rejected": stats["rejected"],
                "avg_score": stats["avg_score"],
            },
        }
    )

@app.route("/api/candidates", methods=["GET"])
def list_selected_candidates():
    """
    HR ला selected candidates list पाहता येईल
    """
    selected_list = []

    for cid, data in CANDIDATE_ANALYSIS.items():
        if data.get("selected", False):  # फक्त shortlisted
            selected_list.append({
                "id": cid,
                "name": data.get("name"),
                "email": data.get("email"),
                "domain": data.get("domain"),
                "score": data.get("score"),
                "resume": data.get("resume_path")
            })

    return jsonify(selected_list)



@app.route("/api/hr/bulk_analyze", methods=["POST"])
def bulk_analyze_resume():
    files = request.files.getlist("resumes")
    domain = request.form.get("domain")

    if not files or len(files) == 0:
        return jsonify({"error": "No resumes uploaded"}), 400

    processed = []

    for file in files:
        if not allowed_file(file.filename):
            continue

        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        # Extract text
        resume_text = extract_text_from_file(save_path)

        # ML inference
        score, label, probs = predict_score_and_label(resume_text)

        candidate_id = str(uuid.uuid4())

        # Save into DB
        CANDIDATE_ANALYSIS[candidate_id] = {
            "candidate_id": candidate_id,
            "name": filename,
            "email": None,
            "domain": domain,
            "resume_path": save_path,
            "resume_text": resume_text,
            "score": round(score, 2),
            "selected": label == "selected",
        }

        processed.append({
            "id": candidate_id,
            "file": filename,
            "score": score,
            "selected": (label == "selected")
        })

    return jsonify({
        "message": "Bulk screening completed",
        "processed": processed
    })
 
if __name__ == "__main__":
    # DB tables तयार करा (पहिल्यांदा run होताना)
    init_db()
    app.run(debug=True)
