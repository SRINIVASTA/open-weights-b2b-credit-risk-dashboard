# src/engine_clients.py
import time

def call_groq_live(api_key, model_name, user_prompt):
    """Executes live benchmarks against open-weights models hosted on Groq."""
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        start_time = time.perf_counter()
        
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": f"Analyze strictly using clear markdown headers:\n{user_prompt}"}],
            temperature=0.1
        )
        latency = time.perf_counter() - start_time
        tokens = completion.usage.completion_tokens
        
        # ✅ FIX: Array index added to resolve 'list' object error
        response_text = completion.choices[0].message.content
        
        return {
            "status": "success", 
            "latency": latency, 
            "tps": tokens / latency, 
            "tokens": tokens, 
            "response": response_text
        }
    except Exception as e:
        return {"status": "error", "error_msg": str(e)}


def call_gemini_live(api_key, model_name, user_prompt):
    """Executes live benchmarks against Google AI Studio via the modern google-genai SDK."""
    try:
        # ✅ FIX: Upgraded to modern 2026 Google GenAI SDK interface
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        start_time = time.perf_counter()
        
        # Clean model string naming mapping helper
        clean_model_name = model_name.replace("google/", "")
        
        response = client.models.generate_content(
            model=clean_model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                temperature=0.1
            )
        )
        latency = time.perf_counter() - start_time
        
        # Safely extract generated token statistics
        try:
            tokens = response.usage_metadata.candidates_token_count
        except:
            tokens = len(response.text.split()) * 1.3  # Safe mathematical fallback
            
        return {
            "status": "success", 
            "latency": latency, 
            "tps": tokens / latency, 
            "tokens": int(tokens), 
            "response": response.text
        }
    except Exception as e:
        return {"status": "error", "error_msg": str(e)}
