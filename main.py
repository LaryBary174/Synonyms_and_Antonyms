from fastapi import FastAPI
from api.words import router as words_router


app = FastAPI()

app.include_router(words_router)