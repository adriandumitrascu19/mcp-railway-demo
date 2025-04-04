from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

class AskRequest(BaseModel):
    message: str

@app.post("/ask")
async def ask_ai(req: AskRequest):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = req.message

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Esti un asistent prietenos si clar."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    answer = response.choices[0].message["content"]
    return {"question": prompt, "answer": answer}


@app.get("/", response_class=HTMLResponse)
def serve_form():
    return FileResponse("form.html", media_type="text/html")
