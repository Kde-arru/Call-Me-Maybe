import json
import math
from typing import Any, List, Dict
from llm_sdk import Small_LLM_Model


class JSONContrainedDecoder:
    
    def __init__(self, model: Small_LLM_Model) -> None:
        self.model = model
        self._load_vocab()
        
    def _load_vocab(self) -> None:
        vocab_path = self.model.get_path_to_vocab_file()
        with open(vocab_path, "r", encoding="utf-8") as f:
            raw_vocab: Dict[str, int] = json.load(f)
            
        self.id_to_token: Dict[int, str] = {v: k for k, v in raw_vocab.items()}
        self.vocab_size = len(raw_vocab)
        
        self.id_to_token: Dict[int, str] = {
            token_id: token_str.replace("Ġ", " ").replace("Ċ", "\n")
            for token_id, token_str in self.id_to_token.items()
        }
        
    def _is_valid_json_prefix(self, candidate_text: str) -> bool:
        candidate_text = candidate_text.strip()
        if not candidate_text:
            return True
    
        if not candidate_text.startswith(("{", "[")):
            return False
        
        try:
            json.loads(candidate_text)
            return True
        except json.JSONDecodeError as e:
            valid_prefix_errors = [
                "Unterminated string starting at",
                "Expecting value",
                "Expecting property name enclosed in double quotes",
                "Expecting ':' delimiter",
                "Expecting ',' delimiter",
            ]
            msg = str(e)
            return any(err in msg for err in valid_prefix_errors)
        
    def generate_json(self, prompt: str, max_new_tokens: int = 128) -> str:
        
        tensor_ids = self.model.encode(prompt)
        input_ids: List[int] = tensor_ids[0].tolist()
        
        prompt_length = len(input_ids)
        
        for step in range(max_new_tokens):
            
            logits = self.model.get_logits_from_input_ids(input_ids)
            
            generated_ids = input_ids[prompt_length:]
            current_generated_text = self.model.decode(generated_ids)
            
            masked_logits = list(logits)
            valid_candidates_count = 0
            
            for token_id in range(len(logits)):
                token_text = self.id_to_text.get(token_id, "")
                candidate_text = current_generated_text + token_text
                
                if not self._is_valid_json_prefix(candidate_text):
                    masked_logits[token_id] = -float("inf")
                else:
                    valid_candidates_count += 1
                    
            if valid_candidates_count == 0:
                masked_logits = logits
                
            best_token_id = max(range(len(masked_logits)), key=lambda i: masked_logits[i])
            input_ids.append(best_token_id)
            
            new_generated_text = self.model.decode(input_ids[prompt_length:]).strip()
            try:
                json.loads(new_generated_text)
                return new_generated_text
            except json.JSONDecodeError:
                pass
        
        return self.model.decode(input_ids[prompt_length:])