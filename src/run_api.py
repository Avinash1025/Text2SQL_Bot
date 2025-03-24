from src.pipeline import sql_query_pipeline
from llama_index.core.base.llms.types import ChatResponse


def run_api(query_str: str) -> ChatResponse:
    """Run the API using the provided query string."""
    response = sql_query_pipeline.run(query_str=query_str)
    return response

