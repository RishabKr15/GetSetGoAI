from fastapi import FastAPI
from pydantic import BaseModel
from Agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
app = FastAPI()
import os

class QueryRequest(BaseModel):
    query: str
    
@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        graph = GraphBuilder(model_provider="deepseek")
        react_app = graph()
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png_graph)
        print(f"Graph saved to graph.png in {os.getcwd()}")
        messages = {"messages": [query.query]}
        config = {"configurable": {"thread_id": "default"}}
        output = react_app.invoke(messages, config=config)

        if isinstance(output,dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)
            
        return {"answer": final_output}
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    
    