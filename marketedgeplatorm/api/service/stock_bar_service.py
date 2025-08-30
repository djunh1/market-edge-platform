'''
Created on August 25, 2025

@author: douglasjacobson
'''

import enum
import json
import logging

import pandas as pd
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeekDayEnum(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4


class StockBarService(object):
    def __init__(self, start_date, end_date, ticker):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker

        # string constants
        self.PRICE_CHANGE_TODAY = 'c-o'
        self.PRICE_CHANGE_FROM_YESTERDAY = 'c-pc'
        self.PRICE_CHANGE_OPEN_FROM_PREVIOUS_CLOSE = 'o-pc'


    def generate_weekday_hit_matrix_response(self, price_data):
        logging.info('Generating weekday hit matrix for ticker={}'.format(self.ticker))
        cleaned_stock_data = self.clean_price_data(price_data)
        df_price_changes = self.update_dataframe_with_daily_price_change(cleaned_stock_data)
        df_date_range = self.update_dataframe_with_date_range(df_price_changes)
        df_hit_matrix = self.generate_daily_hit_matrix_for_stock_price(df_date_range)

        json_response = self.convert_hit_matrix_to_json(df_hit_matrix)

        return json_response

    # Primary edge methods

    def generate_daily_hit_matrix_for_stock_price(self, df) -> pd.DataFrame:
        '''
        Generates a new hit matrix for each day of the week.

        :param pd.Dataframe df: a dataframe within a specific date range with the ohlc price data for the ticker.
        '''
        logging.info('Cleaning hit matrix from {} to {} for the ticker={}'.format(self.start_date, self.end_date, self.ticker))
        prices = [self.PRICE_CHANGE_TODAY, self.PRICE_CHANGE_FROM_YESTERDAY, self.PRICE_CHANGE_OPEN_FROM_PREVIOUS_CLOSE]
        df_hit_matrix = pd.DataFrame()
        for priceType in prices:
            for day in WeekDayEnum:
                hit_matrix = {'up': 0, 'down': 0}
                for idx, row in df.iterrows():
                    if idx.dayofweek == day.value and df.loc[idx][priceType] > 0:
                        hit_matrix['up'] = hit_matrix.get('up', 0) + 1
                    elif idx.dayofweek == day.value:
                        hit_matrix['down'] = hit_matrix.get('down', 0) + 1
                new_row = {
                    "price_type": priceType,
                    "day": day.name,
                    "up": hit_matrix['up'],
                    "down": hit_matrix['down'],
                    "total": round((hit_matrix['up'] + hit_matrix['down']), 1),
                    "odds": round((hit_matrix['up'] / (hit_matrix['up'] + hit_matrix['down'])) * 100, 1)
                }
                df_hit_matrix = df_hit_matrix._append(new_row, ignore_index=True)
        return df_hit_matrix

    # Helper Methods

    def clean_price_data(self, price_data) -> pd.DataFrame:
        '''
        Consumes JSON response and converts it into a data frame
        '''
        logging.info('Cleaning stock data for the ticker={}'.format(self.ticker))
        df = pd.json_normalize(price_data['historical'])
        df['datetime'] = pd.to_datetime(df['date'])
        df = df.set_index('datetime')
        df.round(2)

        # reverse order of rows
        df = df[::-1]

        return df

    def update_dataframe_with_daily_price_change(self, df) -> pd.DataFrame:
        '''
        Adds the columns for the price changes (differences) for the following
        todays open - close, todays close - yesterdays close, and todays open - yesterdays close

        :param pd.Dataframe df: a dataframe with the ohlc price data for the ticker.
        '''
        logging.info('Calculating price changes ticker={}'.format(self.ticker))
        df[self.PRICE_CHANGE_TODAY] = df.apply(lambda row: round(row['close'] - row['open'], 2), axis=1)
        df['close_yesterday'] = df['close'].shift()
        df.dropna(inplace=True)
        df[self.PRICE_CHANGE_FROM_YESTERDAY] = df.apply(lambda row: round(row['close'] - row['close_yesterday'], 2),
                                                        axis=1)
        df[self.PRICE_CHANGE_OPEN_FROM_PREVIOUS_CLOSE] = df.apply(lambda row: round(row['open'] - row['close_yesterday'], 2),
                                                        axis=1)
        return df

    def update_dataframe_with_date_range(self, df) -> pd.DataFrame:
        '''
        :param pd.Dataframe df: a dataframe with the ohlc price data for the ticker.
        '''

        filtered_df_indexed = df.loc[self.start_date:self.end_date]
        return filtered_df_indexed

    def convert_hit_matrix_to_json(self, df) -> str:
        '''
        Converts the hit matrix into a JSON to be consumed by the API
        :param pd.Dataframe
        '''

        logging.info('Generating odds matrix JSON response for ticker={}'.format(self.ticker))
        weekday_dict = {}
        for day in WeekDayEnum:
            all_odds = []
            entry = {}
            for index, row in df.iterrows():
                if row['day'] == day.name:
                    entry = {
                        'scenario': row['price_type'],
                        'number_up': row['up'],
                        'number_down': row['down'],
                        'tots': row['total'],
                        'odds': row['odds'],
                    }
                    all_odds.append(entry)
            weekday_dict[day.name] = all_odds

        json_response = {'ticker': self.ticker,
                          'weekday': weekday_dict
                         }

        return json_response

