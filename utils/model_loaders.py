import os
from dotenv import load_dotenv
from typing import Literal,Optional,Any
from pydantic import BaseModel, Field
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from utils.config_loader import load_config

load_dotenv()
class ConfigLoader:
    def __init__(self):
        print("loading config....")
        self.config = load_config()
        
    def __getitem__(self, key):
        return self.config[key]
    

class ModelLoader(BaseModel):
    model_provider: Literal["mistralai", "deepseek",] = "deepseek"
    config : Optional[ConfigLoader] = Field(default=None,exclude=True)
    
    def model_post_init (self, __context: Any) -> None:
        self.config = ConfigLoader()
        
    model_config = {"arbitrary_types_allowed": True}
        
    def load_llm(self):
        """
        Load the llm model
        """
        print("Loading LLM model")
        print("Model provider:", self.model_provider)
        if self.model_provider == "mistralai":
            mistral_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config['llm']["mistral"]["model_name"]
            llm = ChatMistralAI(model_name=model_name, mistral_api_key=mistral_api_key)
        elif self.model_provider == "deepseek":
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config['llm']["deepseek"]["model_name"]
            # Using OpenRouter for DeepSeek
            llm = ChatOpenAI(
                model=model_name, 
                api_key=openai_api_key,
                base_url="https://openrouter.ai/api/v1",
                max_tokens=2000  # Stay within credit limits
            )
        
        return llm
            
        