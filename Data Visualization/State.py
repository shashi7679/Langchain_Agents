from typing_extensions import TypedDict,NotRequired
from typing import Annotated, Union, Literal, Sequence
from langchain_core.messages import BaseMessage
import operator

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    user_id: str
    base64_string: NotRequired[str]