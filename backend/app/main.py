#!/usr/bin/env python
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatAnthropic, ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv
from github_api import get_pr_diff

load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
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
    "Give me feedback on this pull request. The changes are between the <diff> tags."
    "<diff>"
    "{diff}"
    "<diff>")
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()
chain = prompt | model | output_parser

@app.get("/")
async def root(pr_url: Optional[str] = None):
    if not pr_url:
        raise HTTPException(status_code=400, detail="Parameter 'pr_url' is required")

    try:
        diff = get_pr_diff(pr_url)
        result = chain.invoke({"diff": diff})
        print(result)
        return {"llm_out": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#
# add_routes(
#     app,
#     prompt | model,
#     path="/feedback",
# )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
