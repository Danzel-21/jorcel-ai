from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "response": ""}
    )

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": message}
        ]
    )

    answer = completion.choices[0].message.content

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "response": answer,
            "message": message
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
