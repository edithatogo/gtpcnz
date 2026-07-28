import urllib.request
import json
import sys

data = json.dumps({
    "branch": "fix-capitation-budget-lab-refactor",
    "title": "🧹 Refactor render_microeconomics_capitation_budget_lab",
    "description": "Refactored `render_microeconomics_capitation_budget_lab` in `app.py` to break the long function down into four smaller, reusable private helper functions (`_render_capitation_budget_intro`, `_render_capitation_budget_controls`, `_calculate_capitation_budget`, and `_render_capitation_budget_chart`). This improves maintainability and separation of concerns while keeping the exact same functionality."
}).encode("utf-8")

req = urllib.request.Request("http://127.0.0.1:8000/api/v1/submit", data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as f:
        print(f.read().decode('utf-8'))
except urllib.error.URLError as e:
    pass
