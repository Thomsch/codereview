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
    "https://www.code-review-assistant.app",
    "https://code-review-assistant.app"
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
    "Do a code review on this pull request by providing actionable feedback on the changes."
    "Be positive and constructive in your feedback."
    "Start by a very brief summary of the changes in the pull request."
    "Then, provide feedback on the changes in the pull request."
    "Provide at least one security suggestion, one performance suggestion, one readability suggestion relevant to the changes in the pull request. "
    "If you find other concerns, provide feedback on those as well."
    "Make sure the feedback is always actionable and relevant to the changes in the pull request."
    "End with a positive note."
    "The changes in the pull request are between the <diff> tags."
    "<diff>"
    "{diff}"
    "<diff>"
    "Format the feedback in html paragraphs. "
    "Use h3 tags for headings and p tags for paragraphs to organize the feedback.")
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
