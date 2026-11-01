# FlowPilot AI — Business Inquiry Workflow Assistant

FlowPilot AI is a Python and Flask-based business inquiry management tool that helps small teams organize customer inquiries, identify priorities, and prepare suitable reply drafts using AI.

The project demonstrates practical workflow automation with rule-based classification, CSV handling, and optional AI-assisted response generation using the Groq API.

## Problem Statement

Small businesses often spend time manually reviewing customer inquiries, deciding which requests need attention, and preparing responses. FlowPilot AI provides a simple work queue to help organize this process and support faster, more consistent responses.

## Features

- **Inquiry Management:** Add and manage business inquiries through a web interface.
- **Automatic Categorization:** Categorize inquiries using keyword-based rules.
- **Priority Detection:** Assign priority levels based on inquiry content.
- **Suggested Next Actions:** Display suggested actions to help users decide what to do next.
- **AI-Assisted Reply Drafting:** Generate polite, relevant response drafts using Groq AI when configured.
- **Fallback Reply Templates:** Use a local template when AI drafting is unavailable.
- **CSV Import:** Import inquiry records from a CSV file.
- **CSV Export:** Export inquiry records for reporting and further analysis.
- **Search and Filtering:** Find inquiries and filter the work queue.
- **Status Management:** Update inquiry statuses to track progress.
- **Duplicate Handling:** Skip empty and duplicate name/message records during CSV import.

## Technology Stack

- **Programming Language:** Python 3
- **Backend Framework:** Flask
- **Frontend:** HTML and CSS
- **AI Integration:** Groq API
- **Environment Configuration:** `python-dotenv`
- **Data Handling:** Python CSV and standard library modules

## Project Structure

```text
FlowPilot-AI/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── sample_inquiries.csv
├── PROMPT_DOCUMENTATION.md
├── TEST_CHECKLIST.md
├── VIDEO_PRESENTATION.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Installation and Setup on Windows

### 1. Install Python

Download Python from:

https://www.python.org/downloads/

During installation, select **Add Python to PATH** if that option is available.

### 2. Download the Project

Clone the repository using Git:

```bat
git clone https://github.com/gitneha17/FlowPilot-AI.git
cd FlowPilot-AI
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

### 3. Create a Virtual Environment

```bat
py -m venv .venv
```

### 4. Install Dependencies

```bat
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 5. Configure the Groq API Key

AI-assisted reply drafting requires a valid Groq API key.

Create a local file named `.env` in the project root, using `.env.example` as a reference. Add your own key:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual key. Never commit your real `.env` file or share your API key publicly.

### 6. Run the Application

```bat
.venv\Scripts\python.exe app.py
```

### 7. Open FlowPilot AI

Visit the following address in your browser:

http://127.0.0.1:5000

Keep the terminal running while using the application.

## How to Use FlowPilot AI

1. Open the application in your browser.
2. Add a business inquiry or import records using the provided CSV format.
3. Review the automatically assigned category, priority, and suggested next action.
4. Search or filter inquiries as needed.
5. Generate a reply draft using the available drafting feature.
6. Review and edit the suggested response before using it.
7. Update the inquiry status as work progresses.
8. Export inquiry records to CSV when required.

## AI Integration and Responsible Use

FlowPilot AI uses the Groq API for optional AI-assisted reply drafting when a valid API key is configured.

The application may use a local template when AI drafting is unavailable or a request fails.

AI-generated content can be inaccurate or incomplete. Users should review all generated responses before using them. The application does not automatically send emails.

Avoid submitting confidential or personally identifiable customer information to an external AI service unless you have appropriate authorization.

## Testing

Use `TEST_CHECKLIST.md` to document the tests performed on the application.

The following areas can be tested:

- Dashboard loading
- Adding inquiries
- Category and priority detection
- Reply drafting and fallback behavior
- CSV import and export
- Search and filtering
- Status updates
- Handling of empty or duplicate CSV records

Use `sample_inquiries.csv` for demonstration and import testing. Report only test results that have actually been verified.

## Limitations

- This is a learning and portfolio prototype, not a production CRM.
- Inquiry records are held in memory and may reset when the Flask server restarts.
- The application does not currently provide persistent database storage or user authentication.
- Categorization and priority detection rely on keyword-based rules rather than a trained machine learning model.
- AI reply drafting depends on API configuration, network access, and provider availability.
- AI-generated responses require human review.
- The application drafts responses but does not send emails automatically.
- The application should be tested further before being used with real customer data.

## Future Improvements

1. Add SQLite or another database for persistent storage.
2. Introduce user authentication and role-based access.
3. Allow users to review and adjust categories and priorities.
4. Evaluate classification accuracy against a manually labeled dataset.
5. Add configurable reminders and workflow integrations.
6. Track measured workflow metrics through an analytics dashboard.
7. Deploy the application to a suitable hosting platform.

## Project Documentation

The repository includes supporting documentation:

- `PROMPT_DOCUMENTATION.md` — documents the prompts and prompt improvements used during development.
- `TEST_CHECKLIST.md` — provides a checklist for testing the application.
- `VIDEO_PRESENTATION.md` — contains the planned demonstration outline.
- `sample_inquiries.csv` — provides fictional sample inquiry data.

## Portfolio and Assessment

**GitHub Repository:** https://github.com/gitneha17/FlowPilot-AI

FlowPilot AI demonstrates a practical application of Python, Flask, workflow automation, rule-based classification, CSV processing, and AI-assisted response drafting.

A demonstration video and its shareable link can be added here after recording and uploading the actual demo.

---

**Author:** Neha Beldar
