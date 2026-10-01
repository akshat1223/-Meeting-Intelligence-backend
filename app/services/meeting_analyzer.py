
import json
from groq import Groq

from app.config import settings
from app.models.meeting import MeetingAnalysis


client = Groq(api_key=settings.GROQ_API_KEY)


async def analyze_meeting(transcript: str) -> MeetingAnalysis:

    prompt = """
Analyze the following meeting transcript.

Return ONLY valid JSON.

Use EXACTLY this structure:

{
    "summary": "string",
    "decisions": [
        {
            "decision": "string"
        }
    ],
    "action_items": [
        {
            "task": "string",
            "assignee": null,
            "deadline": null,
            "priority": null,
            "status": null
        }
    ],
    "risks": [
        {
            "description": "string"
        }
    ],
    "blockers": [
        {
            "description": "string"
        }
    ],
    "unresolved_items": [
        {
            "item": "string"
        }
    ],
    "participants": []
}

Important:
- blockers MUST be objects with "description".
- unresolved_items MUST be objects with "item".
- action_items MUST be objects.
- Do not return strings directly inside these arrays.
- Do not invent information.

Transcript:
""" + transcript

    response = client.chat.completions.create(
        model=settings.GROQ_LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        response_format={
            "type": "json_object"
        }
    )

    print("GROQ RESPONSE:", response)

    result = json.loads(response.choices[0].message.content)

    return MeetingAnalysis.model_validate(result)