#!/usr/bin/env python
from operator import itemgetter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv
from app.github_api import get_pr_diff
from langchain_core.runnables import RunnableLambda

load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "https://www.code-review-assistant.app/",
    "https://code-review-assistant.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_template(
    "Give me feedback on this pull request. The changes are between the <diff> tags. Format the feedback as html paragraphs."
    "<diff>"
    "{diff}"
    "<diff>")
output_parser = StrOutputParser()

chain = {
    "diff": itemgetter("pr_url") | RunnableLambda(get_pr_diff)
        } | prompt | model | output_parser

add_routes(
    app,
    chain,
    path="/feedback",
    enabled_endpoints=["stream"],
    include_callback_events=True,
)


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="localhost", port=port)
