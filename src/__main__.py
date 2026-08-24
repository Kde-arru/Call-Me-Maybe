import sys
import json
from src.llm_sdk.llm_sdk import Small_LLM_Model


def main() -> None:

    print("Loading model LLM...")
    model = Small_LLM_Model()
    
    test_text = "What is the sum of 2 and 3?"
    
    tensor_ids = model.encode(test_text)
    input_ids: list[int] = tensor_ids[0].tolist()
    
    print(f"\nPrompt: '{test_text}'")
    print(f"Token IDs generate: {input_ids}")
    
    logits = model.get_logits_from_input_ids(input_ids)
    print(f"Tamanho do vocabulario (vetor de logits): {len(logits)}")

    vocab_path = model.get_path_to_vocab_file()
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab: dict[str, int] = json.load(f)
        
    id_to_token = {v: k for k, v in vocab.items()}
    
    top_5_ids = sorted(range(len(logits)), key=lambda i: logits[i], reverse=True)[:5]
    
    print("\nTop 5 proximos tokens que o modelo preve por padrao:")
    for rank, token_id in enumerate(top_5_ids, 1):
        token_str = id_to_token.get(token_id, "<desconhecido>")
        print(f" {rank}. ID: {token_id:<6} | Token: '{token_str}' | Logit: {logits[token_id]:.4f}")
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error ocurred: {e}", file=sys.stderr)
        sys.exit(1)
