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
        return {
            "status": "success", 
            "latency": latency, 
            "tps": tokens / latency, 
            "tokens": tokens, 
            "response": completion.choices.message.content
        }
    except Exception as e:
        return {"status": "error", "error_msg": str(e)}

def call_gemini_live(api_key, model_name, user_prompt):
    """Executes live benchmarks against Google AI Studio infrastructure."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name=model_name)
        start_time = time.perf_counter()
        response = model.generate_content(user_prompt)
        latency = time.perf_counter() - start_time
        try:
            tokens = response.usage_metadata.candidates_token_count
        except:
            tokens = len(response.text.split()) * 1.3  # Fallback approximation
        return {
            "status": "success", 
            "latency": latency, 
            "tps": tokens / latency, 
            "tokens": int(tokens), 
            "response": response.text
        }
    except Exception as e:
        return {"status": "error", "error_msg": str(e)}
