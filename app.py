import os
from pathlib import Path
from flask import Flask, render_template_string, request, render_template, send_file
from forms import DataSelectionForm, DateSelectionForm
from ops.ecris.analysis.venus_data import get_venus_data
from datetime import datetime
from typing import List

from ops.ecris.analysis import VenusDataError

FMT = '%Y-%m-%d %H:%M:%S'
DATA_LOCATION = Path('./data/venus')

def _get_secret_key() -> str:
    key = os.getenv("VENUS_SECRET_KEY")
    if key:
        return key
    # pragma: no cover – this branch is only hit in dev
    import secrets
    return secrets.token_hex(32)

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping( SECRET_KEY=_get_secret_key())

    @app.route('/', methods=['GET', 'POST'])
    def index():
        data_select = DataSelectionForm()
        date_select = DateSelectionForm()

        if request.method == 'POST':
            start_date = date_select.start_date.data
            end_date = date_select.end_date.data
            selected_data = data_select.selected_options.data

            try:
                validate_and_save_data(selected_data, start_date, end_date)
                return send_file('data.csv', mimetype='text/csv', as_attachment=True)
            except VenusDataError as exc:
                return render_template('index.html', error=f'Data error: {exc}', 
                                        date_form=date_select,
                                        form=data_select)

        return render_template('index.html', date_form=date_select,
                               error='',
                               form=data_select)

    return app

def validate_and_save_data(selected_data: List[str], start_date: datetime, end_date: datetime) -> None | ValueError:
    if start_date >= end_date:
        raise ValueError('End time must be before start time')
    data = get_venus_data(DATA_LOCATION, selected_data, start_date, end_date)
    data.to_csv('data.csv', index=False)



if __name__ == '__main__':
    app = create_app()
    app.run()