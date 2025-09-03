from __future__ import annotations

from datetime import date
from typing import List, Tuple

from flask import Flask, redirect, render_template_string, request, url_for

def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index() -> str:
        """
        Render the input form and handle its submission.

        GET
            Returns the HTML form.
        POST
            Reads the submitted values, forwards them to ``process_request``,
            and redirects to the ``/result`` page.
        """
        if request.method == "POST":
            start_date_str: str = request.form.get("start_date", "")
            end_date_str: str = request.form.get("end_date", "")
            selected_items: List[str] = request.form.getlist("items")

            # Convert the date strings to ``datetime.date`` objects.
            # ``date.fromisoformat`` raises ``ValueError`` if the format is wrong.
            try:
                start_date: date = date.fromisoformat(start_date_str)
                end_date: date = date.fromisoformat(end_date_str)
            except ValueError as exc:
                app.logger.error("Invalid date format: %s", exc)
                # Re‑render the form with a simple error message.
                return render_template_string(FORM_TEMPLATE,
                                              error="Please enter valid dates.",
                                              items=AVAILABLE_ITEMS,
                                              selected_items=selected_items,
                                              start_date=start_date_str,
                                              end_date=end_date_str)

            # -----------------------------------------------------------------
            # 2️⃣ Call the placeholder processing function
            # -----------------------------------------------------------------
            process_request(start_date, end_date, selected_items)

            # Store the data in the session or pass via query string.
            # For this minimal example we simply forward them as query args.
            return redirect(
                url_for(
                    "result",
                    start=start_date_str,
                    end=end_date_str,
                    items=",".join(selected_items),
                )
            )

        # --------------------------------------------------------------------- #
        # GET request – render the empty form
        # --------------------------------------------------------------------- #
        return render_template_string(FORM_TEMPLATE,
                                      error=None,
                                      items=AVAILABLE_ITEMS,
                                      selected_items=[],
                                      start_date="",
                                      end_date="")

    @app.route("/result")
    def result() -> str:
        """
        Simple result page that echoes the submitted values.

        In a real application you would display the conversion status,
        download links, logs, etc.
        """
        start = request.args.get("start", "")
        end = request.args.get("end", "")
        items = request.args.get("items", "")
        selected_items = items.split(",") if items else []

        return render_template_string(RESULT_TEMPLATE,
                                      start=start,
                                      end=end,
                                      items=selected_items)

    return app


# --------------------------------------------------------------------------- #
# Placeholder for the real business logic
# --------------------------------------------------------------------------- #
def process_request(start: date, end: date, items: List[str]) -> None:
    """
    **Placeholder** – replace this with the actual conversion routine.

    Parameters
    ----------
    start : datetime.date
        The start date selected by the user.
    end : datetime.date
        The end date selected by the user.
    items : list[str]
        List of values selected from the multi‑select widget.

    Notes
    -----
    The function currently only logs the received arguments.  In a production
    system you would:

    * Validate that ``start <= end``.
    * Translate the selected items into concrete actions (e.g. table names).
    * Call the ``venus_sql_to_parquet`` module for each day in the range.
    * Store the resulting Parquet files and return a status / path.
    """
    logging.info("Processing request – start: %s, end: %s, items: %s",
                 start.isoformat(), end.isoformat(), items)


# --------------------------------------------------------------------------- #
# Static data used by the form (in a real app this could be loaded from a DB)
# --------------------------------------------------------------------------- #
AVAILABLE_ITEMS: Tuple[str, ...] = (
    "ion_current",
    "plasma_params",
    "magnet_power",
    "vacuum_pressure",
    "temperature",
)

# --------------------------------------------------------------------------- #
# HTML templates (kept inline for brevity)
# --------------------------------------------------------------------------- #
FORM_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>VENUS Data Converter</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        .error {{ color: red; }}
        label {{ display: block; margin-top: 1rem; }}
        select {{ width: 100%; height: 8rem; }}
        button {{ margin-top: 1.5rem; padding: 0.5rem 1rem; }}
    </style>
</head>
<body>
    <h1>Convert VENUS SQLite → Parquet</h1>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    <form method="post">
        <label for="start_date">Start date:</label>
        <input type="date" id="start_date" name="start_date"
               value="{{ start_date }}" required>

        <label for="end_date">End date:</label>
        <input type="date" id="end_date" name="end_date"
               value="{{ end_date }}" required>

        <label for="items">Select items to convert:</label>
        <select id="items" name="items" multiple required>
            {% for itm in items %}
                <option value="{{ itm }}"
                    {% if itm in selected_items %}selected{% endif %}>
                    {{ itm.replace('_', ' ').title() }}
                </option>
            {% endfor %}
        </select>

        <button type="submit">Convert</button>
    </form>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Conversion Requested</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem; }}
        ul {{ list-style-type: disc; margin-left: 2rem; }}
    </style>
</head>
<body>
    <h1>Conversion request received</h1>
    <p><strong>Start date:</strong> {{ start }}</p>
    <p><strong>End date:</strong> {{ end }}</p>
    <p><strong>Selected items:</strong></p>
    {% if items %}
        <ul>
        {% for itm in items %}
            <li>{{ itm }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>(none)</p>
    {% endif %}

    <p>🛠️  <em>Placeholder – replace this page with real status / download links.</em></p>

    <p><a href="{{ url_for('index') }}">Back to form</a></p>
</body>
</html>
"""

# --------------------------------------------------------------------------- #
# Entrypoint
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Running ``python app.py`` starts the development server.
    # For production use a WSGI server such as gunicorn or uWSGI.
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)