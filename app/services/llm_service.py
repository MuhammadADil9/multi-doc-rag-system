from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List, Dict, Any


class LLMServiceError(Exception):
    pass


class LLMService:
    """
    Loads and runs tokenizer & LLM
    Given text it would handle answers and generations

    """

    def __init__(self, model_name: str = "BTLM-3B-8k-base"):
        print(f"Loading Tokenizer")
        self.tokenizer = AutoTokenizer.from_pretrained("cerebras/btlm-3b-8k-base")
        self.model = AutoModelForCausalLM.from_pretrained(
            "cerebras/btlm-3b-8k-base", trust_remote_code=True, torch_dtype="auto"
        )

        self.model.eval()

    def generate_answer(
        self, prompt: str, context_chunks: List[str], max_length: int = 300
    ) -> str:
        """
        Generate an answer using the LLM.
        """
        try:
            if not prompt.strip(""):
                raise LLMServiceError("Prompt is empty")
            if len(prompt) > 1000:
                raise LLMServiceError("User prompt exceeds 1000 words")
            if len(context_chunks) == 0:
                raise LLMServiceError("Given context is empty")

            context_text = "\n\n".join(context_chunks)
            formatted_prompt = f"Answer the question based on the context.\n\nContext:\n{context_text}\n\nQuestion: {prompt}\n\nAnswer:"
        
        
            inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        
        
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=4,
                    early_stopping=True
                )
        
        
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)        
        
        