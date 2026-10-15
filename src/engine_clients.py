# src/engine_clients.py
import time
from groq import Groq
import google.generativeai as genai

def call_groq_live(api_key, model_label, prompt):
    """
    Handles live API calls to Groq infrastructure with precise metrics collection.
    """
    start_time = time.time()
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model_label,
            messages=[
                {"role": "system", "content": "You are a conservative B2B credit risk compliance framework auditor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        latency = time.time() - start_time
        # Extract metadata safely
        tokens = response.usage.completion_tokens if response.usage else len(response.choices[0].message.content.split())
        tps = tokens / latency if latency > 0 else 0.0
        
        return {
            "status": "success",
            "latency": latency,
            "tps": tps,
            "tokens": tokens,
            "response": response.choices[0].message.content
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def call_gemini_live(api_key, model_label, prompt):
    """
    Handles live API calls to Google AI Studio infrastructure with precise metrics collection.
    """
    start_time = time.time()
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=model_label,
            system_instruction="You are a conservative B2B credit risk compliance framework auditor."
        )
        response = model.generate_content(prompt)
        latency = time.time() - start_time
        
        # Calculate approximate token details if usage metadata is missing
        tokens = response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') and response.usage_metadata else len(response.text.split())
        tps = tokens / latency if latency > 0 else 0.0
        
        return {
            "status": "success",
            "latency": latency,
            "tps": tps,
            "tokens": tokens,
            "response": response.text
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
