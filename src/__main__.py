import sys
import json
from src.llm_sdk.llm_sdk import Small_LLM_Model
from src.decoder import JSONContrainedDecoder


def main() -> None:

   print("Loading model LLM...")
   model = Small_LLM_Model()
   
   print("Starting JSON Constrained Decoder...")
   decoder = JSONContrainedDecoder(model)
   
   prompt = (
       "Output the result od adding 2 and 3 as a" \
       "valid JSON object with key 'result': \n"
   )
   print(f"\nPrompt seended:\n {prompt}")
   
   print("A gerar resposta com restricao JSON...")
   output_json = decoder.generate_json(prompt)
   
   print("\n--- Resultado Gerado --- ")
   print(output_json)
   print("----------------------")

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
