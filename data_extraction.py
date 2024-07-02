import boto3
import pandas as pd
import requests
import tabula

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
        number_of_stores = self.list_number_of_stores(link_1, header).json()['number_stores']
        list_of_stores = []
        for i in range(0,number_of_stores):
            list_of_stores.append(self.list_number_of_stores(link_2 + str(i), header).json())
        output = pd.DataFrame(list_of_stores)
        return output
    
    def extract_from_s3(self, s3_address):
        """
            Extracts a dataframe from a csv in an s3 Bucket from s3_address
        """
        s3 = boto3.client('s3')
        list = s3_address.split('/')
        s3.download_file(list[2], list[3], list[3])
        return pd.read_csv(list[3])
    
    def read_json(self, link):
        return pd.read_json(link) #Should this be in a context manager?
