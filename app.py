# app.py — Full Flask backend for Attach to Tech

from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attach_to_tech.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------- DATABASE MODELS ------------

class QuoteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    service = db.Column(db.String(120), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

class PartnerApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # 'partner' or 'hire'
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    details = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize DB
if not os.path.exists('attach_to_tech.db'):
    db.create_all()

# ----------- ROUTES ------------


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  

@app.route("/quote", methods=["POST"])
def quote():
    name = request.form.get("name")
    email = request.form.get("email")
    service = request.form.get("service")
    if not name or not email or not service:
        flash("All fields are required for a quote request.", "error")
        return redirect(url_for("index"))
    q = QuoteRequest(name=name, email=email, service=service)
    db.session.add(q)
    db.session.commit()
    flash("Quote request submitted successfully!", "success")
    return redirect(url_for("index"))

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    if not name or not email or not message:
        flash("All fields are required for contact message.", "error")
        return redirect(url_for("index"))
    c = ContactMessage(name=name, email=email, message=message)
    db.session.add(c)
    db.session.commit()
    flash("Message sent successfully!", "success")
    return redirect(url_for("index"))

@app.route("/join", methods=["POST"])
def join_us():
    type_ = request.form.get("type")
    name = request.form.get("name")
    email = request.form.get("email")
    details = request.form.get("details")
    if not type_ or not name or not email:
        flash("All required fields must be filled.", "error")
        return redirect(url_for("index"))
    app_entry = PartnerApplication(type=type_, name=name, email=email, details=details)
    db.session.add(app_entry)
    db.session.commit()
    flash("Application submitted successfully!", "success")
    return redirect(url_for("index"))

# ----------- API for Notes Download/Preview ------------
NOTE_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'notes')
os.makedirs(NOTE_FOLDER, exist_ok=True)

# ---------------- Database Model ----------------
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

db.create_all()

# ---------------- Sample Data ----------------
if not Note.query.first():
    sample_notes = [
        Note(title="HTML & CSS Basics", category="web", filename="promptengg.pdf", description="Step-by-step guide to modern web design."),
        Note(title="InfraDecoded Server Setup", category="infra", filename="infra_server.pdf", description="Linux server setup and networking checklist."),
        Note(title="Content Writing Guide", category="content", filename="content_guide.pdf", description="Tips and tricks to write engaging content."),
        Note(title="Social Media Tips", category="social", filename="social_tips.pdf", description="Boost your social engagement."),
        Note(title="Teaching Methodology", category="teaching", filename="teaching_method.pdf", description="Learn how to teach IT & design effectively.")
    ]
    db.session.bulk_save_objects(sample_notes)
    db.session.commit()
    # Create dummy files
    for note in sample_notes:
        path = os.path.join(NOTE_FOLDER, note.filename)
        with open(path, 'w') as f:
            f.write(f"This is a dummy file for {note.title}")

# ---------------- Routes ----------------
@app.route("/notes")
def get_notes():
    category = request.args.get("category", "all")
    if category == "all":
        notes = Note.query.all()
    else:
        notes = Note.query.filter_by(category=category).all()
    notes_data = [
        {
            "id": note.id,
            "title": note.title,
            "category": note.category,
            "description": note.description,
            "filename": note.filename
        } for note in notes
    ]
    return jsonify(notes_data)

@app.route('/notes/download/<filename>')
def download_note(filename):
    return send_from_directory('notes', filename, as_attachment=True)

@app.route("/note/download/<int:id>")
def note_download(id):
    # In demo, just return JSON, in real app serve file
    return jsonify({"status":"ok","message":f"Download placeholder for note id {id}"})

@app.route("/note/preview/<int:id>")
def note_preview(id):
    # Return demo preview content
    NOTES = [
        {1:'HTML & Accessibility Cheatsheet'},
        {2:'InfraDecoded: Linux server setup'},
        {3:'Content Calendar Template'},
        {4:'Reels Script Formula'},
        {5:'Workshop: Intro to Git'}
    ]
    note = next((n for n in NOTES if id in n), None)
    if note:
        return jsonify({"title": note[id], "preview":"Demo preview content for this note."})
    return jsonify({"error":"Note not found"}), 404



import sqlite3, os

# -------------------- DATABASE SETUP --------------------
def init_db():
    conn = sqlite3.connect('attachtotech.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        service TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()
# --------------------------------------------------------



def init_db():
    conn = sqlite3.connect('attachtotech.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        service TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()
# --------------------------------------------------------


# -------------------- ROUTE FOR FORM --------------------
@app.route('/submit_quote', methods=['POST'])
def submit_quote():
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')

    if not name or not email or not service:
        return jsonify({'status': 'error', 'message': 'All fields required!'}), 400

    conn = sqlite3.connect('attachtotech.db')
    c = conn.cursor()
    c.execute('INSERT INTO quotes (name, email, service) VALUES (?, ?, ?)', (name, email, service))
    conn.commit()
    conn.close()

    # Return JSON success
    return jsonify({'status': 'success', 'message': 'Quote request submitted successfully!'})
# --------------------------------------------------------
import random


@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    import random
    data = request.get_json()
    idea = data.get('idea', '').lower()

    # Define realistic categories
    fields = {
        "website": {
            "project_type": "Website Design & Development",
            "tools": "HTML, CSS, JavaScript, Flask / WordPress",
            "deliverables": "Responsive design, SEO setup, contact form, analytics",
            "cost": "₹5,000 – ₹25,000 (one-time)",
            "maintenance": "₹500 – ₹1,000/month for hosting & updates",
            "timeline": "7–14 days",
            "tip": "Use clean UI and optimize for Google search"
        },
        "social": {
            "project_type": "Social Media Management",
            "tools": "Canva, Meta Suite, Buffer, ChatGPT",
            "deliverables": "15 posts/month, Reels strategy, audience insights",
            "cost": "₹3,000 – ₹7,000/month",
            "maintenance": "Included in monthly retainer",
            "timeline": "2 weeks for setup + ongoing updates",
            "tip": "Focus on engaging Reels and brand tone consistency"
        },
        "content": {
            "project_type": "Content Writing & Blogging",
            "tools": "Grammarly, Notion, ChatGPT, SEO tools",
            "deliverables": "4–8 articles/month, SEO keywords, content calendar",
            "cost": "₹2,000 – ₹6,000/month",
            "maintenance": "₹500/month for edits and re-optimization",
            "timeline": "Weekly content cycle",
            "tip": "Use AI for research but keep human tone authentic"
        },
        "teaching": {
            "project_type": "Online Course / Tutoring Platform",
            "tools": "Google Meet, Notion, Canva, YouTube",
            "deliverables": "Recorded sessions, notes, test materials, website page",
            "cost": "₹4,000 – ₹10,000 setup",
            "maintenance": "₹300/month for hosting & video uploads",
            "timeline": "2–3 weeks",
            "tip": "Make short concept reels to promote your classes"
        },
        "infra": {
            "project_type": "IT Infrastructure Setup",
            "tools": "Cisco Packet Tracer, Linux, AWS Free Tier",
            "deliverables": "Network config, user accounts, monitoring tools",
            "cost": "₹8,000 – ₹15,000 setup",
            "maintenance": "₹1,000–₹2,000/month (security & backups)",
            "timeline": "1–2 weeks",
            "tip": "Automate backups and use SSH for remote management"
        },
        "marketing": {
            "project_type": "Digital Marketing Campaign",
            "tools": "Google Ads, Meta Ads, Canva, Analytics",
            "deliverables": "Ad design, targeting setup, analytics reporting",
            "cost": "₹5,000 – ₹20,000/month (ads + service)",
            "maintenance": "Included in ongoing campaigns",
            "timeline": "1 week setup + monthly review",
            "tip": "Start with organic posts before paid ads"
        },
        "branding": {
            "project_type": "Brand Identity & Logo Design",
            "tools": "Adobe Illustrator, Canva Pro",
            "deliverables": "Logo, color palette, typography, brand guide",
            "cost": "₹3,000 – ₹10,000 one-time",
            "maintenance": "None unless rebranding later",
            "timeline": "5–10 days",
            "tip": "Keep it minimal and aligned with brand story"
        },
        "business": {
            "project_type": "Business Consultancy & Automation",
            "tools": "Google Sheets, Notion, Zapier, ChatGPT",
            "deliverables": "Business plan, process automation, templates",
            "cost": "₹7,000 – ₹25,000 (one-time or project-based)",
            "maintenance": "₹1,000/month for workflow management",
            "timeline": "2–4 weeks",
            "tip": "Focus on automation to save 30% manual effort"
        },
        "ai": {
            "project_type": "AI Chatbot / Automation Project",
            "tools": "Flask, OpenAI API, LangChain (mock setup)",
            "deliverables": "Chatbot UI, FAQ integration, basic NLP",
            "cost": "₹10,000 – ₹25,000",
            "maintenance": "₹1,000–₹2,000/month (hosting & model updates)",
            "timeline": "2–3 weeks",
            "tip": "Train it on your business FAQs for smart responses"
        },
        "default": {
            "project_type": "General Service or Idea Consulting",
            "tools": "ChatGPT, Canva, Google Workspace",
            "deliverables": "Basic strategy, design or implementation plan",
            "cost": "₹3,000 – ₹15,000 (based on scale)",
            "maintenance": "₹500–₹1,000/month (support & updates)",
            "timeline": "5–10 days",
            "tip": "Start small, validate results, then scale"
        }
    }

    # Try to detect best match
    selected = None
    for key in fields.keys():
        if key in idea:
            selected = fields[key]
            break
    if not selected:
        selected = fields["default"]

    # Add a bit of realistic randomness
    ai_message = random.choice([
        "AI Insight: Consider adding automation to make this scalable.",
        "AI Suggestion: Add a content calendar for consistency.",
        "AI Note: Try focusing on long-term branding, not just reach.",
        "Pro Tip: Review every 2 months to optimize performance."
    ])

    response = {
        "project_type": selected["project_type"],
        "tools": selected["tools"],
        "deliverables": selected["deliverables"],
        "estimated_cost": selected["cost"],
        "maintenance_cost": selected["maintenance"],
        "timeline": selected["timeline"],
        "ai_tip": selected["tip"],
        "bonus": ai_message
    }

    return jsonify(response)



# Sample projects data
projects = [
    {
        "title": "Modern Web Platform",
        "description": "A responsive website for a local startup with custom CMS and SEO optimization.",
        "image": "web_platform.jpg"
    },
    {
        "title": "Social Media Campaign",
        "description": "Boosted engagement for a brand using Instagram, Facebook, and Twitter campaigns.",
        "image": "social_media_campaign.jpg"
    },
    {
        "title": "Online Learning Platform",
        "description": "Created an interactive teaching portal with live sessions, quizzes, and analytics.",
        "image": "teaching_platform.jpg"
    }
]

# Sample testimonials data
testimonials = [
    {"quote": "Attach To Tech transformed our online presence. Their team is professional and creative!",
     "author": "Priya Sharma, Entrepreneur"},
    {"quote": "Thanks to their guidance, our social media engagement increased by 300% in 2 months.",
     "author": "Ramesh Patel, Brand Manager"},
    {"quote": "Their teaching sessions are concise and highly practical — perfect for beginners and pros alike.",
     "author": "Neha Desai, Student"}
]

@app.route('/projects')
def projects_page():
    return render_template('projects.html', projects=projects, testimonials=testimonials)

# ----------- RUN APP ------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
