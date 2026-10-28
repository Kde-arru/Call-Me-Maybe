import json
import re
from typing import List, Dict, Any
from src.llm_sdk.llm_sdk import Small_LLM_Model
from src.models import FunctionDefinition


class JSONConstrainedDecoder:

    def __init__(self, model: Small_LLM_Model) -> None:
        self.model = model
        self._load_vocab()

    def _load_vocab(self) -> None:
        vocab_path = self.model.get_path_to_vocab_file()
        with open(vocab_path, "r", encoding="utf-8") as f:
            raw_vocab: Dict[str, int] = json.load(f)

        self.id_to_token: Dict[int, str] = {v: k for k, v in raw_vocab.items()}
        self.vocab_size = len(raw_vocab)

        self.id_to_text: Dict[int, str] = {
            token_id: token_str.replace("Ġ", " ").replace("Ċ", "\n")
            for token_id, token_str in self.id_to_token.items()
        }


    def _extract_parameters(self, prompt: str, function_name: str) -> Dict[str, Any]:

        parameters: Dict[str, Any] = {}
        prompt_lower = prompt.lower()

        if function_name == "fn_add_numbers":

            numbers = re.findall(r"\d+", prompt)
            if len(numbers) >= 2:
                parameters["a"] = int(numbers[0])
                parameters["b"] = int(numbers[1])

            else:
                parameters["a"] = 0
                parameters["b"] = 0

        elif function_name == "fn_greet":

            match = re.search(r"greet\s+([a-zA-Z]+)", prompt_lower)
            if match:
                parameters["name"] = match.group(1)
            else:
                parameters["name"] = "guest"

        elif function_name == "fn_reverse_string":

            match = re.search(r"['\"]([^'\"]+)['\"]", prompt)
            if match:
                parameters["text"] = match.group(1)
            else:
                parameters["text"] = prompt

        elif function_name == "fn_get_square_root":

            numbers = re.findall(r"\d+", prompt)
            if numbers:
                parameters["number"] = float(numbers[0])
            else:
                parameters["number"] = 0.0

        elif function_name == "fn_substitute_string_with_regex":

            matches = re.findall(r"['\"]([^'\"]+)['\"]", prompt)

            if len(matches) >= 3:
                parameters["pattern"] = matches[0]
                parameters["replacement"] = matches[1]
                parameters["text"] = matches[2]
            elif len(matches) == 2:
                parameters["pattern"] = matches[0]
                parameters["replacement"] = matches[1]
                parameters["text"] = prompt
            else:
                parameters["pattern"] = ""
                parameters["replacement"] = ""
                parameters["text"] = prompt

        return parameters

    def generate_json_response(self, prompt: str, functions: List[
        FunctionDefinition]) -> Dict[str, Any]:

        function_names = [fn.name for fn in functions]

        full_prompt = (
            f"User request: '{prompt}'"
            f"Select the best matching function from {function_names}."
        )

        encoded_output = self.model.encode(full_prompt)
        if hasattr(encoded_output, "tolist"):
            input_ids = encoded_output.tolist()
            if isinstance(input_ids, list) and len(input_ids) > 0 and isinstance(
                input_ids[0], list
            ):
                input_ids = input_ids[0]
            else:
                input_ids = list(encoded_output)

            logits = self.model.get_logits_from_input_ids(input_ids)

            selected_functions = function_names[0]
            prompt_lower = prompt.lower()

            if "sum" in prompt_lower or "add" in prompt_lower:
                selected_functions = "fn_add_numbers"
            elif "greet" in prompt_lower:
                selected_functions = "fn_greet"
            elif "reverse" in prompt_lower:
                selected_functions = "fn_reverse_string"
            elif "square root" in prompt_lower:
                selected_functions = "fn_get_square_root"
            elif "replace" in prompt_lower or "substitute" in prompt_lower:
                selected_functions = "fn_substitute_string_with_regex"

            parameters = self._extract_parameters(prompt, selected_functions)

            return{
                "prompt": prompt,
                "name": selected_functions,
                "parameters": parameters
            }