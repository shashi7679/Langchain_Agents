from langchain.tools import Tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from datetime import datetime, timezone
from langchain_community.tools import DuckDuckGoSearchRun
import functools
from prompts import BASE_GENERAL_PROMPT

class GeneralKnowledgeAgent:
    def __init__(self, llm):
        self.llm = llm
        self.ddg_search = DuckDuckGoSearchRun()
        self._initializer()

    def _initializer(self):
        self.web_search()
        self._initialize_agent()

    def web_search(self):
        def web_serach_func(query:str):
            results = self.ddg_search(query)
            return results
        
        self.web = Tool(
            name="WebSearch",
            func=web_serach_func,
            description="Web Search for updated information"
        )

    def _initialize_agent(self):
        self.agent = create_react_agent(
            model=self.llm,
            tools=[self.web],
            prompt=BASE_GENERAL_PROMPT
        )
        self.node = functools.partial(
            self.agent_node,
            agent=self.agent,
            name="General_Agent"
        )
    
    def agent_node(self, state, agent, name):
        result = agent.invoke(state)
        return {
            "messages": [AIMessage(content=result["messages"][-1].content, name = name)],
            "id": state.get("id"),
        }
