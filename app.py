import os
from pathlib import Path
import tempfile
from flask import (Flask, request, render_template, send_file, flash)
from forms import DataSelectionForm, DateSelectionForm
from ops.ecris.analysis.venus_data import get_venus_data
from datetime import datetime
from typing import List

from ops.ecris.analysis import VenusDataError

FMT = '%Y-%m-%d %H:%M:%S'
BASE_DIR = Path(__file__).resolve().parent
DATA_LOCATION = BASE_DIR / "data" / "venus"

def _get_secret_key() -> str:
    key = os.getenv("VENUS_SECRET_KEY")
    if key:
        return key
    import secrets
    return secrets.token_hex(32)

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping( SECRET_KEY=_get_secret_key())

    @app.route('/', methods=['GET', 'POST'])
    def index():
        data_form = DataSelectionForm()
        date_form = DateSelectionForm()

        if request.method == 'POST':
            if not (data_form.validate_on_submit() and date_form.validate_on_submit()):
                for field, msgs in {**data_form.errors, **date_form.errors}.items():
                    for msg in msgs:
                        flash(f"{field}: {msg}", "error") 
                    print('Error')
                    return render_template("index.html", date_form=date_form, form=data_form)
            start: datetime = date_form.start_date.data
            end: datetime = date_form.end_date.data
            selected: List[str] = data_form.selected_options.data

            if start > end:
                flash("Start date must be **before** end date.", "error")
                return render_template("index.html", date_form=date_form, form=data_form)
            try:
                output_path = _generate_output_file(selected, start, end)
            except VenusDataError as exc:
                flash(f"Data error: {exc}")
                return render_template('index.html', date_form=date_form, form=data_form)
            except BaseException as exc:
                flash(f"An unexpected error occured: {exc}")
                return render_template('index.html', date_form=date_form, form=data_form)

            return send_file(output_path, mimetype='text/csv', as_attachment=True, 
                             download_name=output_path.name)

        return render_template('index.html', date_form=date_form,
                               error='',
                               form=data_form)

    return app

def _generate_output_file(selected_data: List[str], start_date: datetime, end_date: datetime) -> Path:
    tmp = tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False, dir=BASE_DIR / "tmp")
    tmp_path = Path(tmp.name)
    tmp.close()

    data = get_venus_data(DATA_LOCATION, selected_data, start_date, end_date)
    data.to_csv(tmp_path, index=False)
    return tmp_path

if __name__ == '__main__':
    (BASE_DIR / "tmp").mkdir(exist_ok=True)
    app = create_app()
    app.run()