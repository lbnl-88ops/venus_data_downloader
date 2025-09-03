from pathlib import Path
from flask import Flask, render_template_string, request, render_template, send_file
from .forms import DataSelectionForm
from ops.ecris.analysis.venus_data import get_venus_data
import datetime as dt

FMT = '%Y-%m-%d %H:%M:%S'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = DataSelectionForm()
        if request.method == 'POST':
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            selected_data = form.selected_options.data

            if start_date and end_date and selected_data:
                try:
                    start = dt.datetime.strptime(f'{start_date} 0:0:0', FMT)
                    stop = dt.datetime.strptime(f'{end_date} 23:59:00', FMT)
                    # You can now process the start_date and end_date
                    # For example, print them to the console:
                    data_location = Path('../ecris.analysis/data/venus')
                    data = get_venus_data(data_location, selected_data, start, stop)
                    data.to_csv('data.csv', index=False)
                    return send_file('../data.csv', mimetype='text/csv', as_attachment=True)
                except BaseException as exc:
                    return render_template('index.html', error=f'Please enter valid dates: {exc}', 
                                            start_date=start_date, end_date=end_date,
                                            form=form)

        start_date = None
        end_date = None
        return render_template('index.html', start_date=start_date, end_date=end_date,
                               form=form)

    return app