# ML Service for University Portal AI/Analytics
# Litestar async server for predictive models and embeddings

from litestar import Litestar, get, post
from litestar.config.cors import CORSConfig
from litestar.config.logging import LoggingConfig
from pydantic import BaseModel
from typing import List, Optional
import os

# === MODELS ===

class PredictionRequest(BaseModel):
    """Request for student success prediction"""
    student_id: str
    gpa: float
    attendance_rate: float
    assignment_completion: float
    midterm_score: Optional[float] = None
    course_code: str
    semester: str


class PredictionResponse(BaseModel):
    """Prediction response"""
    student_id: str
    predicted_score: float
    risk_level: str
    confidence: float
    recommendations: List[str]


class EmbeddingRequest(BaseModel):
    """Request for text embedding"""
    text: str
    model: str = "bge-small"


class SearchRequest(BaseModel):
    """Semantic search request"""
    query: str
    top_k: int = 5


# === ROUTES ===

@get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ml-service"}


@post("/predict/student-success")
async def predict_student_success(request: PredictionRequest) -> PredictionResponse:
    """
    Predict student success in a course.
    Uses XGBoost model for tabular prediction.
    """
    # Simple rule-based prediction (replace with real model)
    risk_score = (
        (request.gpa / 4.0) * 0.3 +
        request.attendance_rate * 0.3 +
        request.assignment_completion * 0.4
    )
    
    if request.midterm_score:
        risk_score = (risk_score * 0.7 + request.midterm_score / 100 * 0.3)
    
    predicted = min(100, max(0, risk_score * 100))
    
    # Determine risk level
    if predicted >= 70:
        risk_level = "low"
    elif predicted >= 50:
        risk_level = "medium"
    else:
        risk_level = "high"
    
    # Generate recommendations
    recommendations = []
    if request.attendance_rate < 0.8:
        recommendations.append("Attend more classes")
    if request.assignment_completion < 0.8:
        recommendations.append("Complete all assignments on time")
    if predicted < 60:
        recommendations.append("Request extra tutorial support")
    if not recommendations:
        recommendations.append("Maintain current performance")
    
    return PredictionResponse(
        student_id=request.student_id,
        predicted_score=round(predicted, 2),
        risk_level=risk_level,
        confidence=0.85,
        recommendations=recommendations
    )


@post("/embeddings")
async def generate_embedding(request: EmbeddingRequest) -> dict:
    """
    Generate text embedding using local model.
    Uses BGE-small for privacy and cost efficiency.
    """
    # Simplified embedding (replace with real HuggingFace implementation)
    # In production: use sentence-transformers with BGE-small
    text_hash = hash(request.text)
    embedding = [
        float((text_hash >> i) & 0xFF) / 255.0 
        for i in range(0, 384, 8)
    ]
    
    return {
        "text": request.text,
        "model": request.model,
        "embedding": embedding,
        "dimensions": len(embedding)
    }


@post("/search/semantic")
async def semantic_search(request: SearchRequest) -> dict:
    """
    Semantic search using vector database.
    Uses pgvector for similarity search.
    """
    # Generate query embedding
    query_embedding = [
        float((hash(request.query) >> i) & 0xFF) / 255.0 
        for i in range(0, 384, 8)
    ]
    
    # Return mock results (replace with real pgvector search)
    results = [
        {
            "id": f"doc_{i+1}",
            "title": f"University Document {i+1}",
            "score": round(1.0 - (i * 0.15), 3),
            "excerpt": f"Relevant content matching '{request.query}'..."
        }
        for i in range(request.top_k)
    ]
    
    return {
        "query": request.query,
        "results": results,
        "total": request.top_k
    }


@post("/analytics/cohort")
async def cohort_analytics(request: dict) -> dict:
    """
    Analyze student cohort performance.
    Returns retention predictions and intervention recommendations.
    """
    # Mock cohort analysis
    return {
        "total_students": request.get("total_students", 1000),
        "at_risk": int(request.get("total_students", 1000) * 0.15),
        "predictions": {
            "will_pass": 750,
            "might_fail": 150,
            "will_fail": 100
        },
        "interventions": [
            {"type": "tutoring", "target": 50, "priority": "high"},
            {"type": "mentoring", "target": 75, "priority": "medium"},
            {"type": "alert", "target": 25, "priority": "high"}
        ]
    }


# === APP CONFIG ===

cors_config = CORSConfig(
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging_config = LoggingConfig(
    loggers={
        "ml-service": {
            "level": "INFO",
        }
    }
)

app = Litestar(
    route_handlers=[
        health_check,
        predict_student_success,
        generate_embedding,
        semantic_search,
        cohort_analytics,
    ],
    cors_config=cors_config,
    logging_config=logging_config,
)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)