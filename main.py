from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.model.predict import Predict
from fastapi.responses import ORJSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="src/webapp/templates")

# Payload type
class Tweet(BaseModel):
    text: str

predict = Predict()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request 
    })


@app.post("/v1/api/sentiment", response_class=ORJSONResponse)
async def get_sentiment(tweet:Tweet):  
    data = predict.get_sentiment(tweet.text)
    return data