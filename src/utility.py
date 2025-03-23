import yaml
import os
import pandas as pd
from sqlalchemy import create_engine, inspect, text

def load_config():
    with open(f"{os.getcwd()}/config/config.yml") as file:
        config = yaml.safe_load(file)
    return config


def create_sqldb_and_tables(dir_path, db_path):
    # List all CSV files in the directory
    csv_files = [file for file in os.listdir(dir_path) if file.endswith('.csv')]

    # Create a SQLAlchemy engine
    engine = create_engine(f"sqlite:///{db_path}")
    print(f"successfully connected to the sql db {engine}")

    # Load all table
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    for file in csv_files:
        table_name = os.path.splitext(file)[0]  # Table name is the filename without extension
        df = pd.read_csv(os.path.join(dir_path, file))

        if table_name not in existing_tables:
            df.to_sql(table_name, engine, index=False)
            print(f"Table '{table_name}' has been created and data has been added.")
        else:
            print(f"Table '{table_name}' already exists in the database.")

    return engine
