# Prompt Documentation — FlowPilot AI

**Important:** These are example prompts to guide development. Do not claim you used a prompt, accepted its output, or got a particular result unless that is what actually happened. Update the outcome column after you try each step.

## Project goal
Build a beginner-friendly business inquiry workflow assistant that imports sample inquiries, assigns transparent baseline categories and priorities, drafts response suggestions, and exports results.

## Example prompt log
| Stage | Example prompt | What to verify / record |
|---|---|---|
| 1. Problem definition | "Help me scope a beginner Python project that solves a real business workflow problem. It should import CSV inquiries, categorize and prioritize them, suggest next actions, and export results. Keep it safe for fictional data." | Did the scope stay achievable? Note changes. |
| 2. App structure | "Create a small Flask app with one dashboard, an add-inquiry form, CSV import, search/filter, status updates, and CSV export. Explain each file for a beginner." | Did the file structure match the plan? |
| 3. Classification logic | "Write a transparent Python baseline that maps sample inquiry text to categories and High/Medium/Low priority. Make clear this is rules-based, not a trained model." | Test edge cases and record misclassifications. |
| 4. Data validation | "Review CSV import logic for missing required columns, blank rows, duplicate records, malformed email addresses, and helpful error messages." | Test each case; record bugs found and fixes. |
| 5. Reply drafting | "Draft a concise and polite business response without inventing prices, guarantees, or facts. Mark it as a draft that a person must review." | Compare output to the original inquiry; flag unsupported claims. |
| 6. UI review | "Review the dashboard for beginner usability, responsive layout, clear empty states, and accessible labels. Suggest only improvements that can be verified." | Capture screenshots before/after only if you really made the changes. |
| 7. Final review | "Act as a cautious code reviewer. Identify security, privacy, correctness, and deployment limitations in this small Flask portfolio app. Do not assume tests passed." | Record the real fixes and known limitations. |

## Iteration log — complete this yourself
| Date | Prompt/change | Observed result | What I changed next |
|---|---|---|---|
| YYYY-MM-DD | [fill in] | [actual result] | [actual next change] |
| YYYY-MM-DD | [fill in] | [actual result] | [actual next change] |

## AI-use statement for the project
Suggested wording to adapt truthfully:

"AI tools assisted me with planning, code review, and response-draft design. I reviewed the generated code, tested the workflow, and documented limitations. Inquiry classification and priority assignment in the baseline version use explicit keyword rules; optional Gemini integration can generate reply drafts when configured. No real customer data is included."

Edit this statement to accurately reflect your actual process and tool usage.
