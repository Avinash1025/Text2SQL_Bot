import os
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings, SQLDatabase
from sqlalchemy import inspect

from src.utility import load_config

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

config = load_config()
llm_model = config["groq"]["model"]

llm = Groq(model=llm_model, api_key=api_key)

resp = llm.complete("Hello kesan baaa")
print(resp)

# Access the Ollama settings from the config.yaml
ollama_config = config['ollama']
base_url = f"http://{ollama_config['host']}:{ollama_config['port']}"

# Initialize the embedding model
embedding_model = OllamaEmbedding(
    model_name=ollama_config['embedding_model'],  # Model for generating embeddings (can be 'text-embedding-ada-002' or 'nomic-embed-text:latest')
    base_url=base_url,                        # Base URL for the embedding model
)

Settings.llm = llm
Settings.embed_model = embedding_model


from src.utility import create_sqldb_and_tables
data_dir_path = f"{os.getcwd()}/resources/data"
sqldb_path = f"{os.getcwd()}/resources/Database.db"

engine = create_sqldb_and_tables(dir_path=data_dir_path, db_path=sqldb_path)

inspector = inspect(engine)
tables = inspector.get_table_names()

print(f"Tables Present in db: {tables}")



from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core import SQLDatabase, VectorStoreIndex
from src.prompt import CONTEXT

# Create an SQLDatabase instance using the provided SQLAlchemy engine and list of table names
# This represents the connection to your Sqlite database with the specified tables
sql_database = SQLDatabase(engine, include_tables=tables)

# Create a mapping between SQL tables and nodes in the index
# This will help in linking SQL tables to the objects in the index
table_node_mapping = SQLTableNodeMapping(sql_database)

# Create a list of SQLTableSchema objects, each representing the schema of a table
# with its associated context string (description of the table)
table_schema_objs = [SQLTableSchema(table_name=t, context_str=c) for t, c in zip(tables, CONTEXT)]

# This will index the objects (tables) using a vector store for efficient retrieval based on similarity
obj_index = ObjectIndex.from_objects(
    table_schema_objs,    # List of table schemas with context descriptions
    table_node_mapping,   # Mapping between SQL tables and index nodes
    VectorStoreIndex,     # Index type used for storing and retrieving vectors
)

# This retriever will fetch the most similar objects (tables) based on the query
obj_retriever = obj_index.as_retriever(similarity_top_k=3)

print(table_schema_objs)

