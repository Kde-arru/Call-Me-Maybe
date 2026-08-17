import argparse
import sys

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
        default="data/input/functions_definition.json",
        help="Path to the functions definition JSON"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results"
    )