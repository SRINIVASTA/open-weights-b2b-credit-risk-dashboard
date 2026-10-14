# src/engine_clients.py
import time

def call_groq_live(api_key, model_name, user_prompt):
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        start_time = time.perf_counter()
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": f"Provide an immediate B2B risk analysis under a highly conservative credit framework:\n{user_prompt}"}],
            temperature=0.1
        )
        latency = time.perf_counter() - start_time
        tokens = completion.usage.completion_tokens
        response_text = completion.choices.message.content
        return {"status": "success", "latency": latency, "tps": tokens / latency, "tokens": tokens, "response": response_text}
    except Exception as e:
        return {"status": "error", "error_msg": str(e)}

def call_gemini_live(api_key, model_name, user_prompt):
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        start_time = time.perf_counter()
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        latency = time.perf_counter() - start_time
        try:
            tokens = response.usage_metadata.candidates_token_count
        except:
            tokens = len(response.text.split()) * 1.3
        return {"status": "success", "latency": latency, "tps": tokens / latency, "tokens": int(tokens), "response": response.text}
    except Exception as e:
        return {"status": "error", "error_msg": str(e)}
