from fastapi import FastAPI
from backend.routes import generate, evaluate
from database.models import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Interview Coach API")

# Initialize database
init_db()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(generate.router, prefix="/api", tags=["generation"])
app.include_router(evaluate.router, prefix="/api", tags=["evaluation"])

@app.get("/")
async def root():
    return {"message": "AI Interview Coach Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
