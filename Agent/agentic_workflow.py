from utils.model_loaders import ModelLoader
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import LocationInfoTool
from tools.currency_converter_tool import CurrencyConverterTool
from tools.arithematic_operations_tool import ArithematicOperationsTool
from langgraph.graph import StateGraph, MessagesState,START,END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from prompt_library.prompt import SYSTEM_PROMPT

class GraphBuilder():
    def __init__(self, model_provider :str ="deepseek"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        self.tools = []
        self.weather_tools = WeatherInfoTool()
        self.currency_tools = CurrencyConverterTool()
        self.location_tools = LocationInfoTool()
        self.arithmetic_tools = ArithematicOperationsTool()
        
        self.tools.extend([
            * self.weather_tools.weather_tools_list,
            * self.location_tools.place_search_tools_list,
            * self.arithmetic_tools.calculater_tools_list,
            * self.currency_tools.currency_tools_list 
        ])
        
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        self.system_prompt = SYSTEM_PROMPT

    
    def agent_function(self, state: MessagesState):
        
        """
        This function will be used to build the agent node in the graph. It
        receives a message and a state as input and returns a new state and
        a message as output. The function will be called by the graph engine
        when the agent node is reached in the graph.
        """
        user_question = state['messages']
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}
    
    def build_graph(self):
        memory = MemorySaver()
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent",self.agent_function)
        graph_builder.add_node("tools",ToolNode(tools=self.tools))
        graph_builder.add_edge(START,"agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        return graph_builder.compile(checkpointer=memory)
        
    
    def __call__(self):
        return self.build_graph()
    
    