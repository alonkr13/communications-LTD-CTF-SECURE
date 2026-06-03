from fastapi import FastAPI
import uvicorn
from auth.routers.router import router
from fastapi.middleware.cors import CORSMiddleware
from database import setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")

def home(): 
    return {"message": "Backend is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)