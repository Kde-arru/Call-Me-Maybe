from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ParameterProperty(BaseModel):

    type: str = Field(description="Parameter type:" \
    "'number', 'string', 'boolean', 'etc'")
    description: Optional[str] = Field(default=None,
                    description="Optional parameter description.")


class FunctionDefinition(BaseModel):

    name: str = Field(description="Unique function name.")
    description: str = Field(description="Description of function behavior.")
    parameter: Dict[str, ParameterProperty] = Field(
        default_factory=dict, description="Mapping of paramenter" \
        "names to their specification."
    )
    returns: Optional[Dict[str, Any]] = Field(default=None, description="Specification" \
    "of the return type.")


class PromptInput(BaseModel):

    prompt: str = Field(description="Natural language request or question.")

class FunctionCallResult(BaseModel):

    prompt: str = Field(description="Original input prompt.")
    name: str = Field(description="Name of the selected function.")
    parameters: Dict[str, Any] = Field(description="Extracted" \
    "function arguments with correct types.")
