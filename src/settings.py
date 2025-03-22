from src.utility import load_config
from llama_index.llms.groq import Groq

config = load_config()

api_key = config["groq"]["groq_api"]
llm_model = config["groq"]["model"]

llm = Groq(model=llm_model, api_key=api_key)

resp = llm.complete("Hello kesan baaa")
print(resp)

