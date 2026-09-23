🎯 **What:** Extracted static markdown, mathematical calculations, and chart/metric rendering into distinct helper functions for microeconomics lab scenarios (scheduled payment, capitation budget, activity response, and access mix).
💡 **Why:** Reduces the length and complexity of these Streamlit functions, clearly separating presentation logic, UI context, and core mathematics. Enhances readability and maintainability.
✅ **Verification:** Ran `black` formatting, syntax checks, and `scripts/check_repo_health.py` to confirm all validation and health checks pass.
✨ **Result:** A significant improvement in maintainability for the lab app, with smaller, well-scoped functions that adhere to separation of concerns.
