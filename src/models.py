from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ParameterSpec(BaseModel):

    type: str
    description: Optional[str] = None


class FunctionDefinition(BaseModel):

    name: str
    description: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]


class TestPrompt(BaseModel):

    prompt: str


class FunctionCallResult(BaseModel):

    prompt: str
    name: str
    paramenter: Dict[str, Any]

