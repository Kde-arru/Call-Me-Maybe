import argparse
import json
import sys
from pathlib import Path
from typing import Any, List, Dict

from src.decoder import JSONConstrainedDecoder
from src.llm_sdk.llm_sdk import Small_LLM_Model
from src.models import FunctionCallResult, FunctionDefinition, PromptInput


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Call me Maybe")
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to the JSON file containing function definitions.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the JSON file containing input prompts."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path to the output JSON file",
    )
    return parser.parse_args()


def load_json_file(file_path: str) -> Any:

    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: file '{file_path}' contains invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

def save_json_file(file_path: str, data: Any) -> None:

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Results successfully saved to '{file_path}'")
    except Exception as e:
        print(f"Error: Failed to save output file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:

    args = parse_args()

    raw_functions = load_json_file(args.functions_definition)
    functions: List[FunctionDefinition] = [FunctionDefinition(**fn) for fn in raw_functions]

    raw_inputs = load_json_file(args.input)
    prompts: List[PromptInput] = [PromptInput(**item) for item in raw_inputs]

    print(f"Loaded {len(functions)} function definitions and {len(prompts)} test prompts.")

    print("Loading Qwen3-0.6B model...")
    model = Small_LLM_Model()
    decoder = JSONConstrainedDecoder(model)

    results: List[Dict[str, Any]] = []
    for item in prompts:
        print(f"\nProcessing prompt: '{item.prompt}'")
        result_dict = decoder.generate_json_response(item.prompt, functions)

        validated_result = FunctionCallResult(**result_dict)
        results.append(validated_result.model_dump())

    save_json_file(args.output, results)

if __name__ == "__main__":
    main()