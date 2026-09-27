from __future__ import annotations

import logging
import re

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

logger = logging.getLogger(__name__)


class ChatHFClient:
    def __init__(self, model_name: str, temperature: float = 0.7, max_tokens: int = 1024):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        logger.info("Loading model %s ...", model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )
        logger.info("Model %s loaded", model_name)

    def _clean_response(self, text: str) -> str:
        text = re.sub(r'<\|im_end\|>.*$', '', text)
        text = re.sub(r'<\|end\|>.*$', '', text)
        text = re.sub(r'assistant\s*', '', text, flags=re.IGNORECASE)
        text = text.strip().strip('"').strip("'")
        return text

    def generate(self, messages: list[dict], max_tokens: int | None = None) -> str:
        prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        result = self.pipe(
            prompt,
            max_new_tokens=max_tokens or self.max_tokens,
            temperature=self.temperature,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        generated = result[0]["generated_text"]
        response = generated[len(prompt):]
        return self._clean_response(response)
