from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import resume_routes
import uvicorn

app = FastAPI(title="Resume Parser API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(resume_routes.router, prefix="/resumes", tags=["Resumes"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
