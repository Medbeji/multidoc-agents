import os, openai, logging, sys

from llama_index import SimpleDirectoryReader
from llama_index import (
    VectorStoreIndex,
    SummaryIndex,
    ServiceContext,
    Response
)
from llama_index.schema import IndexNode
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.llms import OpenAI
from llama_index.retrievers import RecursiveRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.response_synthesizers import get_response_synthesizer
from llama_index.agent import OpenAIAgent
import pandas as pd
import openai
from langdon.config.openai import openai_config

print(openai_config.OPENAI_API_KEY)
openai.api_key = openai_config.OPENAI_API_KEY

#define LLM
llm = OpenAI(temperature=0.1, model_name=openai_config.MODEL)
service_context = ServiceContext.from_defaults(llm=llm)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)




titles = [
    "DevOps_Self-Service_Pipeline_Architecture",
    "DevOps_Self-Service_Terraform_Project_Structure",
    "DevOps_Self-Service_Pipeline_Security_Guardrails"
    ]

documents = {}
for title in titles:
    documents[title] = SimpleDirectoryReader(input_files=[f"./data/{title}.pdf"]).load_data()
print(f"loaded documents with {len(documents)} documents")
print(documents)


# Build agents dictionary
agents = {}

for title in titles:

    # build vector index
    vector_index = VectorStoreIndex.from_documents(documents[title], service_context=service_context)

    # build summary index
    list_index = SummaryIndex.from_documents(documents[title], service_context=service_context)

    # define query engines
    vector_query_engine = vector_index.as_query_engine()
    list_query_engine = list_index.as_query_engine()

    # define tools
    query_engine_tools = [
        QueryEngineTool(
            query_engine=vector_query_engine,
            metadata=ToolMetadata(
                name="vector_tool",
                description=f"Useful for retrieving specific context related to {title}",
            ),
        ),
        QueryEngineTool(
            query_engine=list_query_engine,
            metadata=ToolMetadata(
                name="summary_tool",
                description=f"Useful for summarization questions related to {title}",
            ),
        ),
    ]

    # build agent
    function_llm = OpenAI(model="gpt-3.5-turbo-0613")
    agent = OpenAIAgent.from_tools(
        query_engine_tools,
        llm=function_llm,
        verbose=False,
    )

    agents[title] = agent



# define index nodes that link to the document agents
nodes = []
for title in titles:
    doc_summary = (
        f"This content contains details about {title}. "
        f"Use this index if you need to lookup specific facts about {title}.\n"
        "Do not use this index if you want to query multiple documents."
    )
    node = IndexNode(text=doc_summary, index_id=title)
    nodes.append(node)

# define retriever
vector_index = VectorStoreIndex(nodes)
vector_retriever = vector_index.as_retriever(similarity_top_k=1)