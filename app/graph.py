import json
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import OLLAMA_BASE_URL, CHAT_MODEL
from app.retriever import search_docs
from app.tools import search_codebase
from app.schemas import SupportAnswer


class State(TypedDict, total=False):
    issue: str
    docs: list[str]
    code: list[str]
    answer: dict


llm = ChatOllama(
    model=CHAT_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)


def retrieve(state: State):
    return {"docs": search_docs(state["issue"])}


def inspect_code(state: State):
    return {"code": search_codebase(state["issue"])}


def diagnose(state: State):
    docs = "\n\n--- DOCUMENT ---\n".join(state.get("docs", []))
    code = "\n\n--- CODE ---\n".join(state.get("code", []))

    system = """You are an experienced software support engineer.
Use the supplied documentation and code evidence when making specific claims.
If evidence is weak, say so.

Return ONLY valid JSON with exactly:
category, diagnosis, likely_cause, recommended_fix, confidence, evidence, files_checked

category must be one of: bug, configuration, usage, performance, unknown.
confidence must be a number from 0 to 1.
evidence and files_checked must be arrays of strings."""

    prompt = f"""USER ISSUE:
{state["issue"]}

DOCUMENTATION:
{docs or "No documentation retrieved."}

CODE SEARCH RESULTS:
{code or "No matching code found."}"""

    result = llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=prompt),
    ])

    text = result.content
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            parsed = json.loads(text[start:end + 1])
        else:
            parsed = {
                "category": "unknown",
                "diagnosis": text,
                "likely_cause": "Structured output parsing failed.",
                "recommended_fix": "Inspect the supplied evidence manually.",
                "confidence": 0.2,
                "evidence": [],
                "files_checked": [],
            }

    return {"answer": SupportAnswer.model_validate(parsed).model_dump()}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("retrieve", retrieve)
    graph.add_node("inspect_code", inspect_code)
    graph.add_node("diagnose", diagnose)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "inspect_code")
    graph.add_edge("inspect_code", "diagnose")
    graph.add_edge("diagnose", END)
    return graph.compile()


agent = build_graph()
