import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from litellm import completion
from .models import Conversation

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", include_in_schema=False)
@router.post("/")
async def chat(conversation: Conversation):
    try:
        model = conversation.model
        history = conversation.history
        ollama_api_base = "http://localhost:11434"
        api_base = ollama_api_base if "ollama" in model else None

        def generate_responses():
            response = completion(
                model=model,
                messages=history,
                api_base=api_base,
                stream=True,
            )

            answer = ""
            for chunk in response:
                answer += chunk.choices[0].delta.content
                assistant = json.dumps({"role": "assistant", "content": answer})
                yield assistant
            else:
                print(json.dumps({"role": "assistant", "content": answer}))

        return StreamingResponse(generate_responses(), media_type="text/event-stream")
    except Exception as exc:
        raise HTTPException(status=500, detail=exc) from exc
