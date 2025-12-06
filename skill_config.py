DOMAIN_SKILLS = {

    "software_engineer": [
        "python", "java", "c++", "c#", "oop", "dsa",
        "algorithms", "data structures", "git", "api",
        "rest", "sql", "debugging", "django", "flask",
        "spring", "dotnet", "testing", "system design"
    ],

    "data_science": [
        "python", "numpy", "pandas", "statistics",
        "probability", "linear regression", "classification",
        "clustering", "machine learning", "deep learning",
        "nlp", "matplotlib", "seaborn", "scikit-learn",
        "tensorflow", "pytorch", "feature engineering",
        "model validation"
    ],

    "web_development": [
        "html", "css", "javascript", "bootstrap",
        "react", "angular", "vue", "node", "express",
        "frontend", "backend", "rest api", "ui", "ux",
        "responsive design", "tailwind", "mongodb", "mysql"
    ],

    "devops_cloud": [
        "linux", "docker", "kubernetes", "jenkins",
        "aws", "azure", "gcp", "terraform", "ci/cd",
        "monitoring", "networking", "cloud security",
        "automation", "bash", "gitlab ci"
    ],

    "ui_ux_design": [
        "figma", "adobe xd", "wireframing",
        "user research", "prototyping", "ui patterns",
        "design systems", "interaction design",
        "accessibility", "usability testing"
    ],

    "product_management": [
        "roadmapping", "agile", "scrum", "jira",
        "stakeholder management", "market research",
        "requirements gathering", "prioritization",
        "product strategy", "wireframing", "metrics",
        "release planning"
    ],

    "cybersecurity": [
        "network security", "linux", "firewalls",
        "ethical hacking", "penetration testing",
        "siem", "incident response", "cryptography",
        "threat analysis", "osint", "vulnerability scanning"
    ],

    "business_analyst": [
        "excel", "sql", "requirements gathering",
        "brd", "frd", "data visualization", "power bi",
        "tableau", "analysis", "uml", "documentation",
        "stakeholder communication"
    ],

    "digital_marketing": [
        "seo", "sem", "google ads", "meta ads",
        "email marketing", "analytics", "content writing",
        "branding", "keyword research", "social media marketing",
        "campaign management"
    ],

    "hr_talent_acquisition": [
        "recruitment", "linkedin sourcing", "screening",
        "interviewing", "hrms", "ats", "employee engagement",
        "onboarding", "payroll basics", "communication",
        "conflict management"
    ]
}

QUESTION_BANK = {

    # ===== SOFTWARE ENGINEERING =====
    "python": [
        "Explain list vs tuple.",
        "What is a lambda function?",
        "What is list comprehension?",
        "Difference between shallow and deep copy?"
    ],
    "java": [
        "What is JVM, JRE and JDK?",
        "Explain inheritance in Java.",
    ],
    "c++": [
        "What is polymorphism in C++?",
        "Explain constructor vs destructor."
    ],
    "oop": [
        "Explain the 4 principles of OOP with examples.",
        "What is abstraction vs encapsulation?"
    ],
    "dsa": [
        "What is the difference between array and linked list?",
        "Explain time complexity of binary search."
    ],
    "git": [
        "What is git pull vs git fetch?",
        "Explain branching strategy."
    ],
    "api": [
        "What is REST?",
        "Explain difference between GET and POST."
    ],
    "sql": [
        "Explain joins.",
        "What is normalization?"
    ],
    "django": [
        "What is Django ORM?",
        "Explain middleware in Django."
    ],
    "flask": [
        "What is Flask routing?",
        "How to handle session in Flask?"
    ],

    # ===== DATA SCIENCE / ML =====
    "numpy": [
        "What is broadcasting in numpy?",
        "Difference between reshape and ravel?"
    ],
    "pandas": [
        "Explain groupby vs apply.",
        "How merging works in pandas?"
    ],
    "statistics": [
        "What is p-value?",
        "Explain central limit theorem."
    ],
    "ml": [
        "What is overfitting?",
        "Explain supervised vs unsupervised learning."
    ],
    "deep learning": [
        "What is a neural network?",
        "Explain activation functions."
    ],
    "nlp": [
        "What is tokenization?",
        "Explain stemming vs lemmatization."
    ],
    "tensorflow": [
        "What is a tensor?",
        "Explain gradient descent."
    ],
    "pytorch": [
        "What is autograd?",
        "Difference between model.eval() and model.train()?"
    ],

    # ===== WEB DEVELOPMENT =====
    "html": [
        "What is semantic HTML?",
        "Explain difference between div and span."
    ],
    "css": [
        "What is flexbox?",
        "Difference between margin and padding?"
    ],
    "javascript": [
        "What is hoisting?",
        "Explain promises."
    ],
    "react": [
        "How does React state work?",
        "What is virtual DOM?"
    ],
    "node": [
        "What is event loop?",
        "Explain middleware concept."
    ],
    "frontend": [
        "What is responsive design?",
        "Explain accessibility basics."
    ],
    "backend": [
        "What is MVC?",
        "Explain authentication vs authorization."
    ],

    # ===== DevOps / Cloud =====
    "linux": [
        "What is chmod?",
        "Explain process vs thread in Linux."
    ],
    "docker": [
        "What is containerization?",
        "Explain Dockerfile layers."
    ],
    "kubernetes": [
        "What is a pod?",
        "Explain deployment vs service."
    ],
    "aws": [
        "What is EC2?",
        "Explain S3 bucket lifecycle."
    ],
    "azure": [
        "Explain Azure App Service.",
        "What is Azure VM scale set?"
    ],
    "terraform": [
        "What is IAC (Infrastructure as Code)?",
        "Explain Terraform state files."
    ],

    # ===== UI/UX =====
    "figma": [
        "What is auto-layout in Figma?",
        "How do components and variants work?"
    ],
    "wireframing": [
        "What is low-fidelity vs high-fidelity design?",
        "Purpose of user personas?"
    ],
    "ux": [
        "What is usability testing?",
        "Explain UI vs UX."
    ],

    # ===== PRODUCT MANAGEMENT =====
    "agile": [
        "Explain Scrum vs Kanban.",
        "What is sprint planning?"
    ],
    "requirements": [
        "What is BRD vs FRD?",
        "Explain user stories."
    ],
    "metrics": [
        "What are KPIs?",
        "What is product-market fit?"
    ],

    # ===== CYBERSECURITY =====
    "network security": [
        "What is firewall?",
        "Explain phishing attack."
    ],
    "ethical hacking": [
        "Difference between black box vs white box testing?",
        "Explain OWASP top 10."
    ],
    "siem": [
        "What is SIEM?",
        "Explain incident logging."
    ],

    # ===== BUSINESS ANALYST =====
    "excel": [
        "What are pivot tables?",
        "Explain VLOOKUP vs INDEX/MATCH."
    ],
    "power bi": [
        "What is DAX?",
        "Explain page filters vs report filters."
    ],
    "tableau": [
        "What is calculated field?",
        "Explain dashboards vs worksheets."
    ],

    # ===== DIGITAL MARKETING =====
    "seo": [
        "What is on-page SEO?",
        "Explain keyword density."
    ],
    "google ads": [
        "Explain CPC vs CPM.",
        "How does Quality Score work?"
    ],
    "social media marketing": [
        "What is engagement rate?",
        "Difference between organic vs paid reach?"
    ],

    # ===== HR / Talent Acquisition =====
    "recruitment": [
        "Explain end-to-end recruitment lifecycle.",
        "What is competency-based interviewing?"
    ],
    "ats": [
        "What is Applicant Tracking System?",
        "How do resume scoring algorithms work?"
    ],
    "onboarding": [
        "Explain employee onboarding process.",
        "Difference between HRBP vs Recruiter?"
    ],
}