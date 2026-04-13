from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.services.groq_client import groq_service
from database.models import get_db, Question, Evaluation, InterviewSession
from sqlalchemy.orm import Session
import json

router = APIRouter()

class EvaluationRequest(BaseModel):
    session_id: int
    question_index: int # 0-based index of the question in the session
    answer: str

class EvaluationResponse(BaseModel):
    score: int
    strengths: str
    weaknesses: str
    missing_points: str
    ideal_answer: str
    improvement: str

class FinalReportRequest(BaseModel):
    session_id: int

@router.post("/evaluate-answer", response_model=EvaluationResponse)
async def evaluate_answer(request: EvaluationRequest, db: Session = Depends(get_db)):
    # Get the specific question
    session = db.query(InterviewSession).filter(InterviewSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if request.question_index >= len(session.questions):
        raise HTTPException(status_code=400, detail="Invalid question index")
    
    question = session.questions[request.question_index]
    
    prompt = f"""You are a strict and professional interview evaluator.

Question: {question.text}
User Answer: {request.answer}

Evaluate the answer and return ONLY in JSON format with these exact keys:
"score": (0-100),
"strengths": "...",
"weaknesses": "...",
"missing_points": "...",
"ideal_answer": "...",
"improvement": "..."

Rules:
- Be strict but fair
- Do not give full marks easily
- Identify missing technical points
- Ideal answer should be concise and correct
- Improvement must be actionable"""

    system_prompt = "You are a professional technical recruiter. Return ONLY valid JSON."
    
    result = groq_service.chat_completion(prompt, system_prompt=system_prompt, format_json=True)
    
    if not result:
        raise HTTPException(status_code=500, detail="AI Evaluation failed")

    # Store evaluation in DB
    existing_eval = db.query(Evaluation).filter(Evaluation.question_id == question.id).first()
    if existing_eval:
        db.delete(existing_eval) # Overwrite if exists
    
    evaluation = Evaluation(
        question_id=question.id,
        user_answer=request.answer,
        score=result.get("score", 0),
        strengths=result.get("strengths", ""),
        weaknesses=result.get("weaknesses", ""),
        missing_points=result.get("missing_points", ""),
        ideal_answer=result.get("ideal_answer", ""),
        improvement=result.get("improvement", "")
    )
    db.add(evaluation)
    db.commit()
    
    return EvaluationResponse(**result)

@router.post("/get-final-report")
async def get_final_report(request: FinalReportRequest, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter(InterviewSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    all_results = []
    total_score = 0
    evaluated_count = 0
    
    for q in session.questions:
        if q.evaluation:
            all_results.append({
                "question": q.text,
                "user_answer": q.evaluation.user_answer,
                "score": q.evaluation.score,
                "feedback": f"Strengths: {q.evaluation.strengths}\nWeaknesses: {q.evaluation.weaknesses}",
                "ideal_answer": q.evaluation.ideal_answer
            })
            total_score += q.evaluation.score
            evaluated_count += 1
            
    avg_score = total_score / evaluated_count if evaluated_count > 0 else 0
    
    prompt = f"""You are a career coach.

Given the following interview performance data:
{json.dumps(all_results)}

Generate:
1. Overall score summary
2. Strengths
3. Weak areas
4. Suggestions to improve
5. Recommended topics to study

Return the response in a structured JSON format with these matching keys."""

    system_prompt = "You are a professional career coach. return ONLY valid JSON."
    
    overall_feedback = groq_service.chat_completion(prompt, system_prompt=system_prompt, format_json=True)
    
    # Update session with overall results
    session.overall_score = avg_score
    session.overall_feedback = json.dumps(overall_feedback)
    db.commit()
    
    return {
        "avg_score": avg_score,
        "per_question": all_results,
        "overall_feedback": overall_feedback
    }
