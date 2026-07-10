from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from agent import agent
from database import get_db
from models import Interaction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = agent.invoke({"messages": [{"role": "user", "content": req.message}]})
    last_message = response["messages"][-1].content
    return {"reply": last_message}

class InteractionCreate(BaseModel):
    hcp_name: str = ""
    interaction_type: str = ""
    attendees: str = ""
    topics_discussed: str = ""
    sentiment: str = ""
    outcomes: str = ""
    follow_up_actions: str = ""

@app.post("/interactions/manual")
def create_manual(data: InteractionCreate, db: Session = Depends(get_db)):
    new_interaction = Interaction(**data.dict())
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
    return {"id": new_interaction.id, "status": "saved"}

@app.get("/")
def root():
    return {"message": "HCP CRM backend is running"}

@app.get("/interactions")
def get_interactions(db: Session = Depends(get_db)):
    return db.query(Interaction).all()