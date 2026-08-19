import json
import sys
from typing import Any, List, Type, TypeVar
from pydantic import BaseModel, ValidationError


T = TypeVar("T", bound=BaseModel)

def load_json_models(file_path: str, model_cls: Type[T]) -> List[T]:

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(
                f"Error: Expected a JSON array in {file_path}", file=sys.stderr
            )
            sys.exit(1)

        return [model_cls.model_validate(item) for item in data]

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(
            f"Error: Invalid JSON format in '{file_path}': {e}", file=sys.stderr
        )
        sys.exit(1)
    except ValidationError as e:
        print(
            f"Errord: Schema validation failed for '{file_path}': {e}",
            file=sys.stderr
        )
        sys.exit(1)
    