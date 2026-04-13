from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from backend.services.groq_client import groq_service
from database.models import get_db, InterviewSession, Question
from sqlalchemy.orm import Session

router = APIRouter()

class GenerateRequest(BaseModel):
    roles: List[str]
    session_id: int = None

class GenerateResponse(BaseModel):
    questions: List[str]
    session_id: int

@router.post("/generate-questions", response_model=GenerateResponse)
async def generate_questions(request: GenerateRequest, db: Session = Depends(get_db)):
    roles_str = ", ".join(request.roles)
    
    # Create a new session if not provided
    if not request.session_id:
        new_session = InterviewSession(roles=roles_str)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        session_id = new_session.id
    else:
        session_id = request.session_id

    prompt = f"""You are an expert interviewer. Generate 5 to 10 realistic interview questions for the following roles: {roles_str}.
Difficulty: beginner to intermediate.
Rules:
- Questions must be practical and commonly asked
- Avoid generic HR questions
- Keep them short and clear
- Mix concepts if multiple roles selected"""

    system_prompt = "You are a professional technical interviewer. Return the results in a JSON object with a key 'questions' which is a list of strings."
    
    result = groq_service.chat_completion(prompt, system_prompt=system_prompt, format_json=True)
    
    if not result or 'questions' not in result:
        raise HTTPException(status_code=500, detail="Failed to generate questions")

    questions_list = result['questions']
    
    # Save questions to DB
    for q_text in questions_list:
        db_question = Question(session_id=session_id, text=q_text)
        db.add(db_question)
    
    db.commit()
    
    return GenerateResponse(questions=questions_list, session_id=session_id)
