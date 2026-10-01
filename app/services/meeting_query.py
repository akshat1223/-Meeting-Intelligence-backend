from groq import Groq

from app.config import settings

client = Groq(api_key = settings.GROQ_API_KEY)

async def answer_metting_question(question:str, transript:str, analysis: dict):
    prompt = """
    Answer the users question using only the meeting info provided below.

    meeting transript: {transript}
    meeting analysis: {analysis}
    user question: {question}

    do not hellucinate info if the answer is not avilable, say: "The information is not avilable"

"""
    prompt = prompt.format(transript=transript, analysis=analysis, question=question)
    response = client.chat.completions.create(model=settings.GROQ_LLM_MODEL, messages=[{"role": "user", "content": prompt}], temperature=0)

    return response.choices[0].message.content