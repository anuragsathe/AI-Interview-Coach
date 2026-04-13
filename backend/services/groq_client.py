import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.is_mock = not self.api_key or self.api_key == "your_groq_api_key_here"
        if not self.is_mock:
            self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"

    def chat_completion(self, prompt, system_prompt="You are a professional assistant.", format_json=False):
        if self.is_mock:
            p_lower = prompt.lower()
            if format_json:
                if "generate" in p_lower and "question" in p_lower:
                    return {"questions": [
                        "What are the key components of a Data Science pipeline?",
                        "Explain the difference between supervised and unsupervised learning.",
                        "Describe a challenging technical problem you solved recently.",
                        "How do you handle missing data in a dataset?",
                        "What is overfitting and how can you prevent it?"
                    ]}
                elif "evaluator" in p_lower or "evaluate" in p_lower:
                    return {
                        "score": 85,
                        "strengths": "Clear explanation and good examples.",
                        "weaknesses": "Could be more concise.",
                        "missing_points": "Mentioning specific libraries or tools.",
                        "ideal_answer": "A perfect answer would include both theory and practical application.",
                        "improvement": "Focus on the business impact of your solution."
                    }
                elif "career coach" in p_lower:
                    return {
                        "overall_score_summary": "You demonstrated strong fundamentals in Data Science.",
                        "strengths": "- Strong conceptual understanding\n- Good problem-solving approach",
                        "weak_areas": "- Needs more focus on deployment\n- Could improve on optimization techniques",
                        "suggestions_to_improve": "Work on projects involving cloud deployment.",
                        "recommended_topics_to_study": "Kubernetes, Docker, AWS SageMaker"
                    }
                return {
                    "error": "No mock response configured for this prompt",
                    "prompt_received": prompt[:50] + "..."
                }
            return "This is a mock response because no valid GROQ_API_KEY was found."

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                model=self.model,
                response_format={"type": "json_object"} if format_json else None
            )
            content = response.choices[0].message.content
            if format_json:
                return json.loads(content)
            return content
        except Exception as e:
            print(f"Error calling Groq: {e}")
            return None

groq_service = GroqService()
