
import csv
import io
import json
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from groq import Groq
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "change-this-for-local-demo"
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Fictional demo records. Data is held in memory and resets on restart.
INQUIRIES = [
    {
        "id": 1,
        "name": "Aarav Shah",
        "email": "aarav@example.com",
        "message": "Please share pricing for your website development service.",
        "category": "Pricing",
        "priority": "Medium",
        "status": "New",
        "next_action": "Prepare relevant pricing information",
        "reply": "",
        "created_at": "Demo record",
    },
    {
        "id": 2,
        "name": "Mira Patel",
        "email": "mira@example.com",
        "message": "Our website is down and we need help urgently today.",
        "category": "Technical Support",
        "priority": "High",
        "status": "New",
        "next_action": "Investigate the technical issue and respond promptly",
        "reply": "",
        "created_at": "Demo record",
    },
    {
        "id": 3,
        "name": "Rohan Mehta",
        "email": "rohan@example.com",
        "message": "I would like to know more about your automation solutions.",
        "category": "Product / Service Inquiry",
        "priority": "Medium",
        "status": "New",
        "next_action": "Share relevant service information",
        "reply": "",
        "created_at": "Demo record",
    },
]

CATEGORIES = [
    "Pricing",
    "Technical Support",
    "Product / Service Inquiry",
    "Partnership",
    "Complaint",
    "Other",
]

PRIORITIES = ["High", "Medium", "Low"]


def classify_inquiry(message):
    """Classify an inquiry and recommend its next action."""
    text = (message or "").lower()

    support_keywords = [
        "down", "broken", "bug", "error", "not working",
        "unable to fetch", "cannot fetch", "can't fetch",
        "unable to access", "can't access", "cannot access",
        "not loading", "won't load", "website unavailable",
        "site unavailable", "failed to load", "technical",
        "crash", "crashing", "outage", "login issue",
        "unable to login", "unable to log in",
    ]

    pricing_keywords = [
        "price", "pricing", "cost", "quote", "quotation",
        "invoice", "payment", "billing", "how much",
    ]

    complaint_keywords = [
        "complaint", "unhappy", "disappointed",
        "refund", "poor service", "bad experience",
    ]

    partnership_keywords = [
        "partner", "partnership", "collaborat",
    ]

    product_keywords = [
        "service", "solution", "feature", "automation",
        "website", "app", "application", "launch",
        "new version", "upgrade", "development",
        "shopping app",
    ]

    if any(word in text for word in support_keywords):
        category = "Technical Support"
        action = "Investigate the technical issue and respond promptly"

    elif any(word in text for word in complaint_keywords):
        category = "Complaint"
        action = "Review the complaint and prepare a careful response"

    elif any(word in text for word in pricing_keywords):
        category = "Pricing"
        action = "Prepare relevant pricing information"

    elif any(word in text for word in partnership_keywords):
        category = "Partnership"
        action = "Review partnership opportunity"

    elif any(word in text for word in product_keywords):
        category = "Product / Service Inquiry"
        action = "Share relevant service information"

    else:
        category = "Other"
        action = "Review inquiry and decide next step"

    urgent_keywords = [
        "urgent", "urgently", "asap", "immediately",
        "critical", "emergency", "website down",
        "site down", "outage",
    ]

    high_priority_support = [
        "down", "outage", "crash", "crashing",
        "website unavailable", "site unavailable",
    ]

    medium_keywords = [
        "price", "pricing", "cost", "quote",
        "quotation", "invoice", "payment", "billing",
    ]

    if (
        any(word in text for word in urgent_keywords)
        or (
            category == "Technical Support"
            and any(word in text for word in high_priority_support)
        )
        or category == "Complaint"
    ):
        priority = "High"

    elif category == "Technical Support":
        priority = "Medium"

    elif any(word in text for word in medium_keywords):
        priority = "Medium"

    elif category == "Product / Service Inquiry" and any(
        word in text for word in ["launch", "new version", "upgrade"]
    ):
        priority = "Medium"

    else:
        priority = "Low"

    return category, priority, action


def make_template_reply(name, category):
    """Provide a safe fallback when AI drafting is unavailable."""
    greeting = (name or "there").strip()

    if category == "Pricing":
        body = (
            "Thank you for your interest. We can share relevant pricing "
            "details once we understand your requirements."
        )
    elif category == "Technical Support":
        body = (
            "Thank you for letting us know. We understand this may be "
            "disruptive. Please share the affected page and any error "
            "message so the issue can be reviewed."
        )
    elif category == "Partnership":
        body = (
            "Thank you for reaching out about a possible partnership. "
            "Please share more about your proposal and goals."
        )
    elif category == "Complaint":
        body = (
            "Thank you for bringing this to our attention. We take your "
            "concern seriously and would appreciate any relevant details "
            "so it can be reviewed."
        )
    else:
        body = (
            "Thank you for contacting us. We would be happy to learn more "
            "about your requirements and suggest suitable next steps."
        )

    return (
        f"Hi {greeting},\n\n"
        f"{body}\n\n"
        "Best regards,\n"
        "FlowPilot AI\n"
        "Customer Support Team"
    )


def gemini_reply(name, category, message):
    """Generate a customer reply using Groq, with safe fallback on failure."""
    if not GROQ_API_KEY:
        print("Groq API key is missing. Check your .env file.")
        return None

    customer_name = (name or "there").strip()
    customer_message = (message or "").strip()

    try:
        client = Groq(
            api_key=GROQ_API_KEY,
            timeout=45.0,
            max_retries=1,
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional customer support assistant. "
                        "Write one specific, helpful, ready-to-review email "
                        "body responding directly to the customer's message. "
                        "Use a warm, professional and concise tone. "
                        "Acknowledge the actual issue or request. Suggest "
                        "practical next steps and ask up to three relevant "
                        "questions when useful. For technical problems, "
                        "ask for diagnostic details such as the affected "
                        "page and exact error message. For pricing requests, "
                        "ask about requirements instead of inventing prices. " 
                        "Never invent company policies, prices, phone numbers, "
                        "email addresses, discounts, support hours, guarantees, "
                        "investigations, or completed fixes. If information is "
                        "unavailable, ask the customer for clarification or say "
                        "the team will confirm it. Use only facts provided in "
                        "the inquiry or explicitly supplied in the prompt. "
                        "Never ask for passwords, OTPs, "
                        "or full payment card details. Do not include a "
                        "greeting or signature. Return only the email body."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Customer name: {customer_name}\n"
                        f"Inquiry category: {category}\n"
                        f"Customer message: {customer_message}\n\n"
                        "Draft a personalized response that addresses this "
                        "specific message. Avoid vague, generic filler."
                    ),
                },
            ],
            temperature=0.4,
            max_completion_tokens=700,
        )

        if not response.choices:
            print("Groq returned no response choices.")
            return None

        choice = response.choices[0]
        message_obj = choice.message
        reply = (message_obj.content or "").strip()
        finish_reason = getattr(choice, "finish_reason", None)

        # Diagnostic output helps identify empty or incomplete responses.
        print("Groq finish reason:", finish_reason)
        print("Groq message content:", repr(reply[:500]))
        print(
            "Groq reasoning present:",
            bool(getattr(message_obj, "reasoning", None)),
        )

        if not reply:
            print("Groq returned an empty reply.")
            return None

        if finish_reason == "length":
            print("Groq reply reached its token limit.")
            return None

        # Remove common Markdown formatting and excess blank lines.
        reply = re.sub(r"[*`#]", "", reply)
        reply = re.sub(r"\n{3,}", "\n\n", reply).strip()

        # Remove a greeting if the model unexpectedly includes one.
        greeting_pattern = (
            r"^(?:hi|hello|dear)\s+"
            + re.escape(customer_name)
            + r"\s*[,!:.]?\s*"
        )
        reply = re.sub(
            greeting_pattern,
            "",
            reply,
            count=1,
            flags=re.IGNORECASE,
        ).strip()

        # Remove a model-generated signature to avoid duplication.
        reply = re.sub(
            r"\n*\s*(?:best regards|kind regards|regards|sincerely|"
            r"thank you),?\s*[\s\S]*$",
            "",
            reply,
            flags=re.IGNORECASE,
        ).strip()

        # Reject clearly incomplete responses.
        if len(reply.split()) < 12:
            print("Groq reply is too short; using template fallback.")
            return None

        if reply[-1] not in ".!?\"')":
            print("Groq reply may be incomplete; using template fallback.")
            return None

        if re.search(
            r"\b(?:and|or|but|with|for|to|the|a|an|of|in|such as)$",
            reply.rstrip().split()[-1],
            re.IGNORECASE,
        ):
            print("Groq reply ends with an unfinished phrase.")
            return None

        # Add a single consistent greeting and signature.
        final_reply = (
            f"Hi {customer_name},\n\n"
            f"{reply}\n\n"
            "Best regards,\n"
            "FlowPilot AI\n"
            "Customer Support Team"
        )

        return final_reply

    except Exception as error:
        # Do not print API keys or other secret configuration.
        print(f"Groq API error ({type(error).__name__}): {error}")
        return None


def build_inquiry(name, email, message, record_id):
    category, priority, action = classify_inquiry(message)

    return {
        "id": record_id,
        "name": name.strip(),
        "email": email.strip(),
        "message": message.strip(),
        "category": category,
        "priority": priority,
        "status": "New",
        "next_action": action,
        "reply": "",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


@app.route("/")
def index():
    search = request.args.get("q", "").strip().lower()
    priority_filter = request.args.get("priority", "")
    category_filter = request.args.get("category", "")

    rows = INQUIRIES

    if search:
        rows = [
            r for r in rows
            if search in (
                r["name"] + " " + r["email"] + " " + r["message"]
            ).lower()
        ]

    if priority_filter:
        rows = [
            r for r in rows
            if r["priority"] == priority_filter
        ]

    if category_filter:
        rows = [
            r for r in rows
            if r["category"] == category_filter
        ]

    stats = {
        "total": len(INQUIRIES),
        "high": sum(1 for r in INQUIRIES if r["priority"] == "High"),
        "new": sum(1 for r in INQUIRIES if r["status"] == "New"),
        "categories": len(set(r["category"] for r in INQUIRIES)),
    }

    return render_template(
        "index.html",
        inquiries=rows,
        stats=stats,
        categories=CATEGORIES,
        priorities=PRIORITIES,
        q=request.args.get("q", ""),
        selected_priority=priority_filter,
        selected_category=category_filter,
    )


@app.post("/add")
def add():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not message:
        flash("Name and inquiry message are required.", "error")
        return redirect(url_for("index"))

    if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        flash(
            "Please enter a valid email address or leave it blank.",
            "error",
        )
        return redirect(url_for("index"))

    new_id = max((r["id"] for r in INQUIRIES), default=0) + 1
    INQUIRIES.insert(0, build_inquiry(name, email, message, new_id))

    flash(
        "Inquiry added and categorized. Review its priority and next action.",
        "success",
    )
    return redirect(url_for("index"))


@app.post("/draft/<int:inquiry_id>")
def draft(inquiry_id):
    inquiry = next(
        (r for r in INQUIRIES if r["id"] == inquiry_id),
        None,
    )

    if not inquiry:
        flash("Inquiry not found.", "error")
        return redirect(url_for("index"))

    ai_text = gemini_reply(
        inquiry["name"],
        inquiry["category"],
        inquiry["message"],
    )

    if ai_text:
        inquiry["reply"] = ai_text
        flash(
            "AI reply draft created. Please review it before use.",
            "success",
        )
    else:
        inquiry["reply"] = make_template_reply(
            inquiry["name"],
            inquiry["category"],
        )
        flash(
            "Template draft created because AI was unavailable or "
            "returned an unusable response. Review before use.",
            "warning",
        )

    return redirect(url_for("index"))


@app.post("/status/<int:inquiry_id>")
def update_status(inquiry_id):
    inquiry = next(
        (r for r in INQUIRIES if r["id"] == inquiry_id),
        None,
    )
    new_status = request.form.get("status", "")

    if inquiry and new_status in ["New", "In Progress", "Resolved"]:
        inquiry["status"] = new_status
        flash("Inquiry status updated.", "success")

    return redirect(url_for("index"))


@app.post("/upload")
def upload():
    file = request.files.get("file")

    if not file or not file.filename.lower().endswith(".csv"):
        flash("Please choose a CSV file.", "error")
        return redirect(url_for("index"))

    try:
        content = file.stream.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(content))

        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")

        fields = {
            field.strip().lower(): field
            for field in reader.fieldnames
            if field
        }

        name_col = next(
            (
                fields[key]
                for key in ["name", "contact_name", "customer_name"]
                if key in fields
            ),
            None,
        )
        email_col = next(
            (
                fields[key]
                for key in ["email", "email_address"]
                if key in fields
            ),
            None,
        )
        message_col = next(
            (
                fields[key]
                for key in ["message", "inquiry", "query", "description"]
                if key in fields
            ),
            None,
        )

        if not name_col or not message_col:
            raise ValueError(
                "CSV needs a name/contact_name column and a "
                "message/inquiry/query column."
            )

        imported = 0
        seen = {
            (r["name"].lower(), r["message"].lower())
            for r in INQUIRIES
        }

        for row in reader:
            name = (row.get(name_col) or "").strip()
            email = (
                (row.get(email_col) or "").strip()
                if email_col else ""
            )
            message = (row.get(message_col) or "").strip()

            if (
                not name
                or not message
                or (name.lower(), message.lower()) in seen
            ):
                continue

            new_id = max(
                (r["id"] for r in INQUIRIES),
                default=0,
            ) + 1

            INQUIRIES.append(
                build_inquiry(name, email, message, new_id)
            )
            seen.add((name.lower(), message.lower()))
            imported += 1

        flash(
            f"Imported {imported} new inquiry/inquiries. "
            "Empty and duplicate rows were skipped.",
            "success",
        )

    except (UnicodeDecodeError, csv.Error, ValueError) as exc:
        flash(f"Could not import CSV: {exc}", "error")

    return redirect(url_for("index"))


@app.get("/export")
def export():
    output = io.StringIO()

    columns = [
        "id", "name", "email", "message", "category",
        "priority", "status", "next_action", "reply", "created_at",
    ]

    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(INQUIRIES)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = (
        "attachment; filename=flowpilot_inquiries.csv"
    )
    response.headers["Content-Type"] = "text/csv; charset=utf-8"

    return response


if __name__ == "__main__":
    app.run(debug=True)
