import warnings
warnings.filterwarnings("ignore", category=UserWarning, message='Field name "output_schema" in "TavilyResearch" shadows an attribute in parent "BaseTool"')
warnings.filterwarnings("ignore", category=UserWarning, message='Field name "stream" in "TavilyResearch" shadows an attribute in parent "BaseTool"')

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import re
import os
import time
import logging
import json
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, Response

from tools.place_search_tool import LocationInfoTool
from Agent.agentic_workflow import GraphBuilder

load_dotenv()

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    num_travelers: Optional[int] = None
    travel_month: Optional[str] = None
    allow_web: Optional[bool] = False
    auto_convert: Optional[bool] = False
    target_currency: Optional[str] = None
    include_web_results: Optional[bool] = False
    thread_id: Optional[str] = "default"

@app.on_event("startup")
def startup_event():
    try:
        provider = os.getenv("MODEL_PROVIDER", "google")
        app.state.graph_builder = GraphBuilder(model_provider=provider)
        app.state.react_app = app.state.graph_builder()
        logger.info(f"GraphBuilder initialized with provider: {provider}")
    except Exception as e:
        logger.exception("Failed to initialize on startup")

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        react_app = getattr(app.state, "react_app", None)
        if react_app is None:
            provider = os.getenv("MODEL_PROVIDER", "google")
            app.state.graph_builder = GraphBuilder(model_provider=provider)
            react_app = app.state.graph_builder()

        metadata = (
            f"Trip Context: Travelers: {query.num_travelers}, "
            f"Month: {query.travel_month if query.travel_month else 'any month'}, "
            f"Preferred Currency: {query.target_currency if query.target_currency else 'USD'}."
        )
        if query.auto_convert:
            metadata += " IMPORTANT: Please proactively convert all costs and budgets to the Preferred Currency using your tools."
        messages = {"messages": [("user", metadata), ("user", query.query)]}
        
        # Persistence check
        config = {"configurable": {"thread_id": query.thread_id}}
        
        # Invoke the graph
        output = react_app.invoke(messages, config=config)
        
        # --- ROBUST OUTPUT PARSING ---
        final_output = ""
        
        # Handle dictionary responses (prevents the 'markdown' key error)
        if isinstance(output, dict):
            if "markdown" in output:
                final_output = output["markdown"]
            elif "structured" in output and isinstance(output["structured"], dict):
                start_fin = output["structured"].get("markdown", str(output))
                if "... full markdown ..." in start_fin or "full markdown" in start_fin:
                     # Fallback to message content if LLM used the placeholder
                     if "messages" in output and len(output["messages"]) > 0:
                        final_output = output["messages"][-1].content
                     else:
                        final_output = str(output)
                else:
                    final_output = start_fin
            elif "messages" in output and len(output["messages"]) > 0:
                final_output = output["messages"][-1].content
            else:
                final_output = str(output)
        else:
            final_output = str(output)
            
        # Ensure final_output is a string (handle case where content became a list)
        if isinstance(final_output, list):
             final_output = " ".join([str(item) for item in final_output])
        elif not isinstance(final_output, str):
             final_output = str(final_output)

        # Remove any lingering machine-readable JSON blocks
        final_output = re.sub(r"```json\s*[\s\S]*?```", "", final_output, flags=re.DOTALL).strip()
        
        # Provide both a cleaned `answer` for UI and a `raw` field for debugging
        return {"answer": final_output}

    except Exception as e:
        logger.exception("Error in /query")
        # Handle OpenRouter Credit Issues (402)
        # Handle OpenRouter Credit Issues (402)
        if "402" in str(e):
             # return JSONResponse(status_code=402, content={"error": "Insufficient Credits on OpenRouter."})
             return JSONResponse(status_code=402, content={"error": f"Provider API Error: {str(e)}"})
        return JSONResponse(status_code=500, content={"error": str(e)})

# PDF and Test endpoints
@app.get("/test")
def test_endpoint():
    return {"status": "ok"}

@app.post("/export_pdf")
def export_pdf(req: dict):
    from utils.save_to_document import markdown_to_pdf_bytes
    pdf_bytes = markdown_to_pdf_bytes(req['content'], title=req.get('title', "Travel Plan"))
    return Response(content=pdf_bytes, media_type="application/pdf")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)