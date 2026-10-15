# src/engine_clients.py
import time
from groq import Groq
from google import genai  # Modern google-genai client interface import

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
    Handles live API calls to Google AI Studio using the modern google-genai client layer.
    """
    start_time = time.time()
    try:
        # Initialize the modern unified client object
        client = genai.Client(api_key=api_key)
        
        # Modern endpoint structure for content generation
        response = client.models.generate_content(
            model=model_label,
            contents=prompt,
        )
        latency = time.time() - start_time
        
        text_output = response.text
        tokens = len(text_output.split())  # Fast metric estimator for word chunks
        tps = tokens / latency if latency > 0 else 0.0
        
        return {
            "status": "success",
            "latency": latency,
            "tps": tps,
            "tokens": tokens,
            "response": text_output
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
