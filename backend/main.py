from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import random
from .app.schemas import IdeaRequest, QuestionRequest, AgentResponse
from .app.agents.informational import InformationalAgent
from .app.agents.interpersonal import InterpersonalAgent
from .app.agents.decision_making import DecisionMakingAgent
from .app.database import get_db, IdeaModel

app = FastAPI(title="Rasha Multi-Agent Backend")

info_agent = InformationalAgent()
inter_agent = InterpersonalAgent()
dm_agent = DecisionMakingAgent()

@app.post("/api/user/create")
async def create_user(db: Session = Depends(get_db)):
    user = IdeaModel()
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.id}

@app.post("/api/idea/update/{user_id}")
async def update_idea(user_id: int, req: dict, db: Session = Depends(get_db)):
    user = db.query(IdeaModel).filter(IdeaModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if "main_idea" in req: user.main_idea = req["main_idea"]
    if "resubmitted_idea" in req: user.resubmitted_idea = req["resubmitted_idea"]
    if "agent_name" in req: user.agent_name = req["agent_name"]
    if "generative_num" in req: user.generative_num = req["generative_num"]
    
    db.commit()
    return {"status": "success"}

@app.post("/api/utils/generate-number")
async def generate_number():
    # Simple random for now, could be more robust
    return {"number": random.randint(100, 999)}

@app.post("/api/agents/informational", response_model=AgentResponse)
async def informational_agent_endpoint(req: QuestionRequest):
    try:
        res = await info_agent.process(req.question)
        return AgentResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/interpersonal", response_model=AgentResponse)
async def interpersonal_agent_endpoint(req: IdeaRequest):
    try:
        res = await inter_agent.process(req.idea)
        return AgentResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/decision-making", response_model=AgentResponse)
async def decision_making_agent_endpoint(req: IdeaRequest):
    try:
        res = await dm_agent.process(req.idea)
        return AgentResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
