import argparse
import sys
from src.models import FunctionDefinition, TestPrompt
from src.utils import load_json_models


def main() -> None:

    parser = argparse.ArgumentParser(description="Function Calling CLI")

    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path no the functions definition JSON"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the functions definition JSON"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json"
    )

    args = parser.parse_args()

    functions = load_json_models(args.functions_definition, FunctionDefinition)
    prompts = load_json_models(args.input, TestPrompt)

    print(f"Loaded {len(functions)} function definitions")
    print(f"Loaded {len(prompts)} test prompts")

    print(f"Functions file: {args.functions_definition}")
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error ocurred: {e}", file=sys.stderr)
        sys.exit(1)
