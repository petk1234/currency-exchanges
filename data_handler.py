import requests
import pandas as pd
from datetime import datetime
import gspread
from gspread_dataframe import set_with_dataframe

class DataHandler:
    base_url = 'https://bank.gov.ua/NBU_Exchange/exchange_site?'
    gc = gspread.service_account()
    sh = gc.open("My power bi project")

    def transformDate(self, date_string):
        print(date_string)
        return datetime.strptime(date_string, "%Y-%m-%d").strftime("%Y%m%d")
    
    def format_to_two_digits(self, number):
        integer_part = int(number)
        integer_digits = len(str(abs(integer_part)))
        if integer_digits > 2:
            factor = 10 ** (integer_digits - 2)
            return number / factor
        else:
            return number 

    def fetch_exchange_rates(self, startDate, endDate):
        response = requests.get(f"{self.base_url}start={self.transformDate(startDate)}&end={self.transformDate(endDate)}&valcode=usd&sort=exchangedate&order=desc&json")
        return response.json()

    def transform_json_to_df(self, jsonData):
        transformed_data = pd.json_normalize(jsonData)
        transformed_data['rate'] = transformed_data['rate'].apply(lambda x: self.format_to_two_digits(x))
        df = pd.DataFrame()
        df[['date','currency']] = transformed_data[[ 'exchangedate', 'rate']]
        set_with_dataframe(self.sh.sheet1, df)

    def clear_sheet(self):
        self.sh.sheet1.clear()
        