
import base64
import re

from langchain.tools import Tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from datetime import datetime, timezone
import functools
from prompts import BASE_PLOTTER_PROMPT

def is_valid_base64(s: str) -> bool:
    if not isinstance(s, str):
        print(f"Error: Input must be a string, but got {type(s)}")
        return False
    if not s:
        # An empty string is often considered valid Base64 (decodes to empty bytes)
        return True
    base64_chars_regex = r"^[A-Za-z0-9+/=_*-]*$"
    if not re.fullmatch(base64_chars_regex, s):
        print(f"Debug: String '{s}' contains invalid Base64 characters.")
        return False

    # Standard Base64 decoding attempt
    try:
        if len(s) % 4 == 0:
            base64.b64decode(s, validate=True)
        else:
            pass # We'll rely on the exception for invalid format directly.
        return True
    except base64.binascii.Error:
        # Debugging: print(f"Debug: Failed standard Base64 decode for '{s}'")
        pass # Not a valid standard Base64 string

    # URL-safe Base64 decoding attempt (handles '-' and '_' instead of '+' and '/')
    try:
        base64.urlsafe_b64decode(s, validate=True)
        return True
    except base64.binascii.Error:
        # Debugging: print(f"Debug: Failed URL-safe Base64 decode for '{s}'")
        pass # Not a valid URL-safe Base64 string

    # If neither decoding method succeeded, it's not a valid Base64 string
    return False


class PlotterAgent:
    def __init__(self, llm):
        self.llm = llm
        self.base64Image = None
        self._initializer()

    def _initializer(self):
        self.generate_plot()
        self._initialize_agent()

    def generate_plot(self):
        def generate_plot_func(code:str):
            """
            Executes code to generate plot in base64 string format.
            """
            local_namespace = {}
            exec(code, local_namespace)
            plot_data = local_namespace['plot_data']
            base64_image = plot_data()
            if is_valid_base64(base64_image):
                return {
                    "status": "success",
                    "message": (
                        "Generated base64 image Successfully!"
                    )
                }
            return {
                "status": "error",
                "message": (
                    "Unable to generate a valid base64 string consisting the plot"
                    "Please fix your code and take neccessary measure to genrate a plot and returning it after converting it into a valid base64 string"
                )
            }
        self.gen_plot = Tool(
            name="Generate_Plot",
            func=generate_plot_func,
            description="""
            executes the code having 'plot_data' and retuns the status of the base64 string
            """
        )

    def _initialize_agent(self):
        self.agent = create_react_agent(
            model=self.llm,
            tools=[self.gen_plot],
            prompt=BASE_PLOTTER_PROMPT
        )
        self.node = functools.partial(
            self.agent_node,
            agent=self.agent,
            name="Plotter_Agent"
        )
    
    def agent_node(self, state, agent, name):
        result = agent.invoke(state)
        state["base64_string"] = self.base64Image
        return {
            "messages": [AIMessage(content=result["messages"][-1].content, name = name)],
            "id": state.get("id"),
            "base64_string": state["base64_string"]
        }