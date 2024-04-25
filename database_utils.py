from sqlalchemy import create_engine
from sqlalchemy import inspect
import yaml

class DatabaseConnector:
    """
        Connect and upload data to the database.
    """
    def read_db_creds(self, file_path):
        """
            Open a YAML file, then print and return the contents.
        """
        with open(file_path, 'r') as imported_file:
            #print(yaml.safe_load(imported_file))
            return yaml.safe_load(imported_file)
        
    def init_db_engine(self, file_path):
        """
            Uses read_db_creds to create an sqlalchemy engine from a file path containing a list of credentials
        """
        dictionary_of_credentials = self.read_db_creds(file_path)
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = dictionary_of_credentials['RDS_HOST']
        USER = dictionary_of_credentials['RDS_USER']
        PASSWORD = dictionary_of_credentials['RDS_PASSWORD']
        DATABASE = dictionary_of_credentials['RDS_DATABASE']
        PORT = dictionary_of_credentials['RDS_PORT']
        #print(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        return create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    
    def list_db_tables(self, file_path):
        """
            Passes init_db_engine and list the tables in the connected database
        """
        engine = self.init_db_engine(file_path)
        engine.execution_options(isolation_level='AUTOCOMMIT').connect()
        inspector = inspect(engine)
        print(inspector.get_table_names())

    def upload_to_db(self, data_frame, table_name, file_path):
        """
            Uploads 'data_frame' as 'table_name' to a database whose credentials are stored as a yaml file in 'file_path'
        """
        data_frame.to_sql(table_name, self.init_db_engine(file_path), if_exists='replace')
