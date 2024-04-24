import pandas as pd
import data_cleaning
import database_utils
import boto3
import tabula
import requests

local_database_creds = "local_db_creds.yaml"
external_database_creds = "db_creds.yaml"

class DataExtractor:
    """
        Used to extract data from different data sources
    """
    def read_rds_table(self, database_connector, table_name):
        """
            Returns a pandas dataframe of 'table_name' in 'database_connector'
        """
        return pd.read_sql_table(table_name, database_connector.init_db_engine(external_database_creds),index_col='index')
    
    def retrieve_pdf_data(self, link):
        """
            Returns a list of pandas dataframes from a pdf file
        """
        return pd.concat(tabula.read_pdf(link, pages='all'), ignore_index=True)
    
    def list_number_of_stores(self, link_1, header):
        """
            Retrieves data from 'end_point' with authentication from 'header'.
        """
        return requests.get(link_1, headers=header)

    def retrieve_stores_data(self, link_1, link_2, header):
        """
            Uses 'list_number_of_stores' to retrieve data from all stores.
        """
        print(link_1)
        number_of_stores = self.list_number_of_stores(link_1, header).json()['number_stores']
        list_of_stores = []
        for i in range(0,number_of_stores):
            list_of_stores.append(self.list_number_of_stores(link_2 + str(i), header).json())
        output = pd.DataFrame(list_of_stores)
        return output
    
    def extract_from_s3(self, s3_address):
        s3 = boto3.client('s3')
        list = s3_address.split('/')
        s3.download_file(list[2], list[3], list[3])
        return pd.read_csv(list[3])
    
    def read_json(self, link):
        return pd.read_json(link) #Should this be in a context manager?
    
my_connection = database_utils.DatabaseConnector()
my_extractor = DataExtractor()
my_hoover = data_cleaning.DataCleaning()
    
def upload_user_data():
    df_raw = my_extractor.read_rds_table(my_connection, 'legacy_users')
    df_cleaned = my_hoover.clean_user_data(df_raw)
    my_connection.upload_to_db(df_cleaned, 'dim_users', local_database_creds)

upload_user_data()

def upload_card_data():
    pdf_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'
    df_raw = my_extractor.retrieve_pdf_data(pdf_link)
    df_cleaned = my_hoover.clean_card_data(df_raw)
    my_connection.upload_to_db(df_cleaned, 'dim_card_details', local_database_creds)

#upload_card_data()
    
def upload_store_data():
    number_of_stores_link = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
    store_data_link = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
    authentication_header = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
    print(my_extractor.list_number_of_stores(number_of_stores_link, authentication_header))
    df_raw = my_extractor.retrieve_stores_data(number_of_stores_link, store_data_link, authentication_header)
    df_cleaned = my_hoover.clean_store_data(df_raw)
    my_connection.upload_to_db(df_cleaned, 'dim_store_details', local_database_creds)

#upload_store_data()

def upload_product_data():
    bucket_address = 's3://data-handling-public/products.csv'
    df_raw = my_extractor.extract_from_s3(bucket_address)
    df_weights_fixed = my_hoover.convert_product_weights(df_raw)
    df_cleaned = my_hoover.clean_products_data(df_weights_fixed)
    my_connection.upload_to_db(df_cleaned, 'dim_products', local_database_creds)

#upload_product_data()

def upload_order_data():
    df_raw = my_extractor.read_rds_table(my_connection, 'orders_table')
    df_cleaned = my_hoover.clean_orders_data(df_raw)
    my_connection.upload_to_db(df_cleaned, 'orders_table', local_database_creds)

#upload_order_data()

def upload_events_data():
    events_link = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
    df_raw = my_extractor.read_json(events_link)
    df_cleaned = my_hoover.clean_event_data(df_raw)
    my_connection.upload_to_db(df_cleaned, 'dim_date_times', local_database_creds)

#upload_events_data()

def all_function():
    upload_user_data()
    upload_card_data()
    upload_store_data()
    upload_product_data()
    upload_order_data()
    upload_events_data()

#all_function()
    