import pandas as pd
import numpy as np
import re

class DataCleaning:
    """
       Used to clean data
    """
    def clean_user_data(self, df_input):
        df = df_input
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce', format="%Y-%m-%d")
        df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce', format="%Y-%m-%d")
        df['phone_number'] = df['phone_number'].map(lambda string: re.sub('[+][0-9]{2}', '0', string)) #Replaces country code from phone number with 0
        df['phone_number'] = df['phone_number'].map(lambda string: re.sub('[+][0-9]{1}', '0', string))
        df['phone_number'] = df['phone_number'].map(lambda string: string.replace('(', '').replace(')', '').replace(' ', '').replace('-', '').replace('.', '')) #Removes brackets and spaces
        df['phone_number'] = df['phone_number'].map(lambda string: re.sub('^00', '0', string)) #Removes double zeroes at start of phone number
        for index, row in df.iterrows():
            if '@' not in str(df.iloc[index, 5]): #If email address doesn't have an '@', set it to null
                #print('Hi!', df.iloc[index, 5])
                df.iloc[index, 5] = np.NaN
            if 'x' in df.iloc[index, 9]:
                df.iloc[index, 9] = np.NaN
        df = df.dropna()
        return df

    def clean_card_data(self, dataframe_input):
        """
            Cleans a database of the format in 'card details.pdf'. We make the 'expiry_date' and 'date_payment_confirmed' colums into dates, make the 'card_number
            column into a integer, and remove all rows with null values.
        """
        dataframe_output = dataframe_input
        dataframe_output['expiry_date'] = pd.to_datetime(dataframe_output['expiry_date'], errors='coerce', format="%m/%y")
        dataframe_output['card_number'] = pd.to_numeric(dataframe_output['card_number'],errors='coerce')
        dataframe_output['date_payment_confirmed'] = pd.to_datetime(dataframe_output['date_payment_confirmed'], errors='coerce', format="%Y-%m-%d")
        dataframe_output = dataframe_output.dropna(axis='index')
        return dataframe_output
    
    def clean_store_data(self, dataframe_input):
        dataframe_output = dataframe_input
        #dataframe_output.set_index('index')
        #dataframe_output = dataframe_output.drop('level_0', axis = 1)
        dataframe_output = dataframe_output.drop('lat', axis = 1)
        for i in ['longitude', 'staff_numbers', 'latitude']:
            dataframe_output[i] = pd.to_numeric(dataframe_output[i], errors='coerce')

        dataframe_output['opening_date'] = pd.to_datetime(dataframe_output['opening_date'], errors='coerce', format="%Y-%m-%d")
        dataframe_output['continent'].replace({'eeEurope':'Europe'}, inplace=True)
        dataframe_output['continent'].replace({'eeAmerica':'America'}, inplace=True)
        dataframe_output = dataframe_output.dropna(subset=['staff_numbers'])
        return dataframe_output
    
    def convert_product_weights(self, dataframe_input):
        dataframe_output = dataframe_input
        for index, row in dataframe_output.iterrows():
            try:
                raw_string = dataframe_output.iloc[index, 3]
                #print(raw_string)
                individual_weight = 0
                quantity = 1
                total_weight = 0
                if 'x' in raw_string:
                    individual_weight = raw_string.split('x')[1]
                    quantity = int(raw_string.split('x')[0])
                    #print(quantity, individual_weight)
                else:
                    individual_weight = raw_string
                if individual_weight[-2:] == 'kg':
                    #print(individual_weight, individual_weight[:-2], 'Unit is KG!')
                    total_weight = round(float(individual_weight[:-2]) * quantity, 3)
                elif individual_weight[-1:] == 'g':
                    #print(individual_weight, 'Unit is G!')
                    total_weight = round((float(individual_weight[:-1]) * quantity) / 1000 ,3)
                elif individual_weight[-2:] == 'ml':
                    #print(individual_weight, 'Unit is ML!')
                    total_weight = round((float(individual_weight[:-2]) * quantity) / 1000, 3)
                elif individual_weight[-1:] == 'l':
                    #print(individual_weight, 'Unit is L!')
                    total_weight = round(float(individual_weight[:-1]) * quantity, 3)
                elif individual_weight[-2:] == 'oz':
                    total_weight = round((float(individual_weight[:-2]) * quantity) / 35, 3)
                if quantity > 1:
                    #print(f'Quanitity is {quantity}, individual_weight is {individual_weight} and total_weight is {total_weight}')
                    pass
                dataframe_output.iloc[index, 3] = total_weight
            except TypeError:
                #print('We have a null value!', index, dataframe_output.iloc[[index]])
                dataframe_output.iloc[index, 3] = np.NaN
        print(dataframe_output['weight'])
        dataframe_output['weight'] = pd.to_numeric(dataframe_output['weight'], errors='ignore')
        return dataframe_output
    
    def clean_products_data(self, dataframe_input):
        dataframe_output = dataframe_input
        dataframe_output['date_added'] = pd.to_datetime(dataframe_output['date_added'], errors='coerce', format="%Y-%m-%d")
        dataframe_output['product_price'] = pd.to_numeric(dataframe_output['product_price'].str.replace('[^-.0-9]', ''))
        dataframe_output['EAN'] = pd.to_numeric(dataframe_output['EAN'], errors='coerce')
        dataframe_output = dataframe_output.dropna()
        return dataframe_output
    
    def clean_orders_data(self, df_input):
        df = df_input
        df = df.drop('first_name', axis = 1)
        df = df.drop('last_name', axis = 1)
        df = df.drop('1', axis = 1)

        return df
    
    def clean_event_data(self, df_input):
        df = df_input
        df['month'] = pd.to_numeric(df['month'], errors='coerce')
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['day'] = pd.to_numeric(df['day'], errors='coerce')
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', format="%H:%M:%S")
        df['timestamp'] = df['timestamp'].dt.time
        df.dropna()
        return df
