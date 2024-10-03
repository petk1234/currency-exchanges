from __main__ import app
from flask import render_template, request
from data_handler import DataHandler

@app.route('/', methods=['GET'])
def template():
    handler_instance = DataHandler()
    if(request.args.get('clear')):
        handler_instance.clear_sheet()

    if(request.args.get('start_date') and request.args.get('end_date')):
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        data = handler_instance.fetch_exchange_rates(start_date_str, end_date_str)
        handler_instance.transform_json_to_df(data)

    return render_template('form.html')