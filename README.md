# FlowPilot AI — Business Inquiry Workflow Assistant

A beginner-friendly portfolio project that demonstrates a practical business workflow: capture inquiries, categorize them, prioritize them, prepare reply drafts, update status, and export a report.

## Problem statement
Small teams can lose time manually sorting incoming business inquiries and deciding what to do next. FlowPilot AI creates a simple, reviewable work queue.

## Features
- Add an inquiry through a form.
- Import CSV records (`name` and `message` are required; `email` is optional).
- Categorize inquiries and assign a priority using transparent baseline rules.
- Suggest a next action for each inquiry.
- Draft a polite response using a local template; optionally use Gemini when a valid `GEMINI_API_KEY` is configured.
- Search/filter the queue, update status, and export all records to CSV.
- Skip empty and duplicate name/message records during import.

## Tech stack
- Python 3
- Flask
- HTML and CSS
- Python standard library (`csv`, `urllib`, `json`, `re`)
- Optional Gemini API integration; the project works without an API key.

## Run on Windows
1. Install Python 3 from https://www.python.org/downloads/ and select **Add Python to PATH** during setup.
2. Extract this folder from the ZIP.
3. Open Command Prompt in the `FlowPilot_AI_Project` folder.
4. Create a virtual environment:
   ```bat
   py -m venv .venv
   ```
5. Install dependencies:
   ```bat
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
6. Start the app:
   ```bat
   .venv\Scripts\python.exe app.py
   ```
7. Open http://127.0.0.1:5000 in your browser.

If `py` is not recognized, try `python --version`. If neither works, install Python first.

## Optional Gemini integration
1. Obtain an API key from Google's Gemini developer platform, subject to current eligibility and quotas.
2. Set it only in your local terminal/session, never in source code or GitHub.
   In Windows Command Prompt:
   ```bat
   set GEMINI_API_KEY=YOUR_KEY_HERE
   .venv\Scripts\python.exe app.py
   ```
3. Click **Draft reply**. If the API key is absent or the request fails, the app falls back to a local template.
4. Review every generated message before using it. Never send confidential customer information to an AI service without permission.

The API's model name, availability, pricing, and quotas can change. The app uses `gemini-3.8-flash` as an example model identifier; if unavailable to your account, check current provider documentation and update `app.py`.

## Test plan
Use `TEST_CHECKLIST.md` and record actual outcomes before claiming a test passed. Use `sample_inquiries.csv` for import testing.

## Important limitations
- This is a learning prototype, not a production CRM.
- Records are held in memory and reset when the server restarts. It has no database or user authentication.
- Baseline category and priority decisions are keyword rules, not a trained ML model.
- Gemini reply drafting is optional. Do not claim the app is fully AI-powered when running without the API key.
- The app drafts messages only; it does not send emails.
- Use fictional or authorized sample data only.

## Portfolio presentation
In your repository, include:
- This README
- Screenshots of the app you actually ran
- Your completed prompt iteration log in `PROMPT_DOCUMENTATION.md`
- A short demo video or a link to it
- A summary of tests you actually completed
- A short section describing what you would improve next (database, authentication, reliable evaluation, and integrations)

## Suggested future improvements
1. Store records in SQLite.
2. Add a review screen to edit AI-generated categories before saving.
3. Compare rules-based categorization against a manually labeled test set.
4. Add scheduled reminders without automatically contacting customers.
5. Add a dashboard showing real measured workflow metrics.
