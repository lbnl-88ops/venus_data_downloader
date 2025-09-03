from pathlib import Path
from flask import Flask, render_template_string, request, render_template, send_file
from forms import DataSelectionForm
from ops.ecris.analysis.venus_data import get_venus_data
from datetime import datetime
from typing import List

FMT = '%Y-%m-%d %H:%M:%S'
DATA_LOCATION = Path('./data/venus')

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = DataSelectionForm()
        if request.method == 'POST':
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            selected_data = form.selected_options.data

            try:
                start = datetime.strptime(f'{start_date} 0:0:0', FMT)
                stop = datetime.strptime(f'{end_date} 23:59:00', FMT)
                validate_and_save_data(selected_data, start, stop)
                return send_file('../data.csv', mimetype='text/csv', as_attachment=True)
            except BaseException as exc:
                return render_template('index.html', error=f'Error: {exc}', 
                                        start_date=start_date, end_date=end_date,
                                        form=form)

        start_date = None
        end_date = None
        return render_template('index.html', start_date=start_date, end_date=end_date,
                               form=form)

    return app

def validate_and_save_data(selected_data: List[str], start: datetime, stop: datetime) -> None | ValueError:
    data = get_venus_data(DATA_LOCATION, selected_data, start, stop)
    data.to_csv('data.csv', index=False)



if __name__ == '__main__':
    app = create_app()
    app.run()