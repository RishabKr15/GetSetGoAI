from fastapi import FastAPI
from pydantic import BaseModel
from Agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.on_event("startup")
def startup_event():
    """Create and cache the GraphBuilder (and optionally the compiled graph) on startup.
    This reduces per-request initialization time which can cause client timeouts.
    """
    try:
        logger.info("Initializing GraphBuilder at startup... this may take a while")
        app.state.graph_builder = GraphBuilder(model_provider="deepseek")
        # Optionally pre-build the reactive app (may be heavy). If it causes issues, remove the next line.
        app.state.react_app = app.state.graph_builder()
        logger.info("GraphBuilder initialized and reactive app built")
    except Exception as e:
        logger.exception("Failed to initialize GraphBuilder on startup: %s", e)
        # Do not raise here; keep the app running to allow debug endpoints.


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    start_time = time.time()
    try:
        # Use cached react_app if available; otherwise create on demand
        react_app = getattr(app.state, "react_app", None)
        if react_app is None:
            logger.info("Reactive app not found in state; building on-demand (this may be slow)")
            graph = GraphBuilder(model_provider="deepseek")
            react_app = graph()

        # Save a visualization if possible (non-fatal)
        try:
            png_graph = react_app.get_graph().draw_mermaid_png()
            with open("graph.png", "wb") as f:
                f.write(png_graph)
            logger.info("Graph saved to graph.png in %s", os.getcwd())
        except Exception:
            logger.exception("Failed to draw or save graph.png (continuing)")

        messages = {"messages": [query.query]}
        config = {"configurable": {"thread_id": "default"}}

        logger.info("Invoking reactive app for query: %s", query.query)
        invoke_start = time.time()
        output = react_app.invoke(messages, config=config)
        invoke_duration = time.time() - invoke_start
        logger.info("Reactive app invoke completed in %.2fs", invoke_duration)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        duration = time.time() - start_time
        logger.info("/query handled in %.2fs", duration)
        return {"answer": final_output}

    except Exception as e:
        logger.exception("Error handling /query: %s", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


