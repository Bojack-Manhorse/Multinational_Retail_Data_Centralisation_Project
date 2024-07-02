# Multinational Retail Data Centralisation project

This project creates a STAR-scheme database based on sales data from a retail store consisting of a large number of stores. We create python scripts to extract and clean data from various sources, upload them to a PostgreSQL database and perform various SQL queries.

The sources we extract data from include the following:

- An AWS Database
- A pdf file containing a table
- An AWS API
- A `.csv` file stored in an AWS s3 bucket
- A json file

## Instructions

### Installation

First ensure python is installed on your system, along with java (to run tabula).

To clone the repository, run the following in a terminal:

```
git clone Bojack-Manhorse/Multinational_Retail_Data_Centralisation_Project
``` 

Then move into the porject directory:

```
cd Multinational_Retail_Data_Centralisation_Project
```

Finally install the required python libraries:

```
pip install -r requirements.txt
```

### Setup

Within the project directory, create two files called 

`db_creds.yaml` and `local_db_creds.yaml` in the project folder. Fill them out as done in `credentials_template.yaml`.
- `db_creds.yaml` will contain the authentication for the database you wish to extract rds tables from.
- `local_db_creds.yaml` will contain the authentication for the database you wish to upload all the tables to.

The file structure should look like this:

![image_of_file_structure](image_of_file_structure.png)

### Usage

Run `python3 data_extraction.py` in the terminal.

## Packages used

- `boto3`
- `pandas`
- `requests`
- `tabula`
- `sqlalchemy`
- `yaml`