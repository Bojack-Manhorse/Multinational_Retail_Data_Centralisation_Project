import pandas as pd
import numpy as np
import re

class DataCleaning:
    """
       Used to clean data
    """
    def clean_user_data(self, df_input):
        """
            Cleans the 'dim_users; table. Set dob and 'join_date' to the correct dateime format, puts the phone number into a standard format, makes sure
            e-mail addresses are valid and fixes country codes.
        """
        df = df_input
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce', format="%Y-%m-%d")
        df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce', format="%Y-%m-%d")
        df['phone_number'] = df['phone_number'].map(lambda string: re.sub('[+][0-9]{2}', '0', string)) #Replaces country code from phone number with 0
        df['phone_number'] = df['phone_number'].map(lambda string: re.sub('[+][0-9]{1}', '0', string))
        df['phone_number'] = df['phone_number'].map(lambda string: string.replace('(', '').replace(')', '').replace(' ', '').replace('-', '').replace('.', '')) #Removes brackets and spaces
        df['phone_number'] = df['phone_number'].map(lambda string: re.sub('^00', '0', string)) #Removes double zeroes at start of phone number

        def check_if_at_exists(string:str):
            if '@' not in str(string): #If email address doesn't have an '@', set it to null
                return np.NaN
            else:
                return string
        df['email_address'] = df['email_address'].map(check_if_at_exists)

        def check_phone_number(string:str):
            if 'x' in string: #If there's an x in the phone number, discard it
                return np.NaN
            else:
                return string
        df['phone_number'] = df['phone_number'].map(check_phone_number)

        def fix_country_code(string:str): #Replaces country codes of 'GGB' with 'GB'
            if str(string) == 'GGB':
                return 'GB'
            else:
                return string
        df['country_code'] = df['country_code'].map(fix_country_code)
        
        df = df.dropna(subset=['user_uuid', 'address', 'email_address'], how='any') #Drops entires with null values in any of those columns
        return df

    def clean_card_data(self, dataframe_input):
        """
            Cleans the "dim_card_details" table. We make the 'expiry_date' and 'date_payment_confirmed' colums into dates, make the 'card_number
            column into a integer, and remove all rows with null values.
        """
        df = dataframe_input
        df['expiry_date'] = pd.to_datetime(df['expiry_date'], errors='coerce', format="%m/%y")
        df['card_number'] = df['card_number'].map(lambda string: re.sub("[^0-9]", '', str(string)))
        df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], errors='coerce', format="%Y-%m-%d")
        def remove_short_strings(string): #Removes card_numbers which are too short
            if len(str(string)) < 8:
                return np.NaN
            else:
                return string
        df['card_number'] = df['card_number'].map(remove_short_strings)
        df = df.dropna(subset=['card_number']) #Drops entires with null card_numbers
        return df
    
    def clean_store_data(self, dataframe_input):
        """
            Cleans the "dim_store_details" table. Drops the 'lat' column, makes certain columns into numeric values
        """
        df = dataframe_input
        df = df.drop('lat', axis = 1) #Seems to be null for all values so dropped
        for i in ['longitude', 'staff_numbers', 'latitude']:
            df[i] = pd.to_numeric(df[i], errors='coerce')
        df['opening_date'] = pd.to_datetime(df['opening_date'], errors='coerce', format="%Y-%m-%d")
        df['continent'].replace({'eeEurope':'Europe'}, inplace=True)
        df['continent'].replace({'eeAmerica':'America'}, inplace=True)
        for index_num, row in df.iterrows():
            if len(str(df.iloc[index_num, 9])) > 2:
                #print(df.iloc[index_num, 9], df.iloc[index_num,4])
                df.iloc[index_num, 4] = np.NaN
        df = df.dropna(subset=['store_code'])
        return df
    
    def convert_product_weights(self, dataframe_input):
        """
            Converts the weight column of the "dim_products" table to kilograms
        """
        df = dataframe_input
        def check_format_and_convert(raw_string:str):
            try:
                individual_weight = 0
                quantity = 1
                total_weight = 0
                if 'x' in raw_string:
                    individual_weight = raw_string.split('x')[1]
                    quantity = int(raw_string.split('x')[0])
                else:
                    individual_weight = raw_string
                if individual_weight[-2:] == 'kg':
                    total_weight = round(float(individual_weight[:-2]) * quantity, 3)
                elif individual_weight[-1:] == 'g':
                    total_weight = round((float(individual_weight[:-1]) * quantity) / 1000 ,3)
                elif individual_weight[-2:] == 'ml':
                    total_weight = round((float(individual_weight[:-2]) * quantity) / 1000, 3)
                elif individual_weight[-1:] == 'l':
                    total_weight = round(float(individual_weight[:-1]) * quantity, 3)
                elif individual_weight[-2:] == 'oz':
                    total_weight = round((float(individual_weight[:-2]) * quantity) / 35, 3)
                if quantity > 1:
                    pass
                return total_weight
            except TypeError:
                return np.NaN
        df['weight'] = df['weight'].map(check_format_and_convert)
        df['weight'] = pd.to_numeric(df['weight'], errors='ignore')
        return df
    
    def clean_products_data(self, dataframe_input):
        """
            Cleans the 'dim_products' table. Sets 'date_added' to datetime, 'product_price' to numeric, 'removed' to 1 minus boolean, and dropps entires with null
            product_code
        """
        df = dataframe_input
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce', format="%Y-%m-%d")
        df['product_price'] = pd.to_numeric(df['product_price'].str.replace('[^-.0-9]', '')) #Makes product price to a string just containing numerics, then applies to_numeric
        df = df.dropna(subset=['product_code'])
        def map_still_available_to_boolean(string): #If still_available, reutrns true, else returns false
            if string == 'still_available':
                return True
            else:
                return False
        df['removed'] = df['removed'].map(lambda string: map_still_available_to_boolean(string))
        def check_if_length_is_36(string):
            if len(string) >= 36:
                return string
            else:
                return np.NaN
        df['uuid'] = df['uuid'].map(check_if_length_is_36)
        df = df.dropna(subset=['product_code', 'uuid'], how='any')
        return df
    
    def clean_orders_data(self, df_input):
        """
            Cleans the 'orders_table' table.
        """
        df = df_input
        df['card_number'] = df['card_number'].astype(str) #For some reason card_number is supposed to be a string
        df = df.drop('first_name', axis = 1)
        df = df.drop('last_name', axis = 1)
        df = df.drop('1', axis = 1)
        return df
    
    def clean_event_data(self, df_input):
        """
            Cleans the 'dim_date_times' table. 
        """
        df = df_input
        def pad_with_zeroes(string:str):# Pads a string with one character with a zero in front
            try:
                if len(string) == 1:
                    return "0" + string
                else:
                    return string
            except TypeError:
                pass
        for i in ['month', 'day']:
            df[i] = df[i].map(pad_with_zeroes) #Ensures month and days are of the form '01' instead on '1'
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', format="%H:%M:%S")
        df['timestamp'] = df['timestamp'].dt.time
        def check_if_length_is_36(string):
            if len(string) >= 36:
                return string
            else:
                return np.NaN
        df['date_uuid'] = df['date_uuid'].map(check_if_length_is_36)
        df = df.dropna()
        return df
