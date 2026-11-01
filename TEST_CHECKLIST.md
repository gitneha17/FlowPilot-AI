# Manual Test Checklist

Run these tests yourself. Mark each item only after you have observed the result.

- [ ] App starts and dashboard opens at `http://127.0.0.1:5000`.
- [ ] Add an inquiry with name and message; confirm it appears in the queue.
- [ ] Try submitting a blank name or message; confirm a helpful validation message appears.
- [ ] Enter a malformed email address; confirm it is rejected.
- [ ] Add a message mentioning "website is down urgently"; inspect the assigned category and priority.
- [ ] Import `sample_inquiries.csv`; count imported rows and verify the resulting records.
- [ ] Import the same CSV again; verify matching name/message duplicates are skipped.
- [ ] Try a CSV with no header or without a required column; verify a helpful error.
- [ ] Search for a contact name and reset the search.
- [ ] Filter by priority and category.
- [ ] Change a record's status and verify the selected value.
- [ ] Generate a reply draft with no Gemini key; verify template fallback.
- [ ] If you configure Gemini, test it with non-sensitive fictional content and verify fallback behavior if the API is unavailable.
- [ ] Export CSV and open it in a spreadsheet or text editor.
- [ ] Restart the app and observe that in-memory changes reset; document this limitation.
- [ ] Check layout at a narrow/mobile browser width.

## Results log
Date tested: __________

Python version: __________

Operating system: __________

Passed: ____ / attempted: ____

Issues found and fixes: __________________________________________

Known issues remaining: _________________________________________
