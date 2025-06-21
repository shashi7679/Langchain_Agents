from langchain_groq import ChatGroq
from sqlalchemy import create_engine
from langchain.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from datetime import datetime, timezone
import functools
from prompts import BASE_SQL_PROMPT


class SQLAgent:
    def __init__(self, connection, llm):
        self.llm = llm
        self.connection = connection
        self.db = SQLDatabase.from_uri(self.connection)
        self._initialize_tools()
        self._initialize_agent()

    def initialize_tools(self):
        def get_current_timestamp(*args, **kwargs):
            return datetime.now(timezone.utc())
        
        self.get_time = Tool(
            name="CurrentTimestamp",
            func=get_current_timestamp,
            description="Get Current timestamp"
        )

    def _initialize_agent(self):
        sql_toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        tools = [sql_toolkit.get_tools(),
                 self.get_time
                 ]
        self.agent = create_react_agent(
            model=self.llm,
            tools=tools,
            prompt=BASE_SQL_PROMPT
        )
        self.node = functools.partial(
            self.agent_node,
            agent=self.agent,
            name="SQL_Agent"
        )

    def agent_node(self, state, agent, name):
        result = agent.invoke(state)
        return {
            "messages": [AIMessage(content=result["messages"][-1].content, name = name)],
            "id": state.get("id")
        }


