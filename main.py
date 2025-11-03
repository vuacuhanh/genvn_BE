# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import generate, upload, export

app = FastAPI(
    title="Tạo sinh đề Tiểu học (TV)",
    version="0.1.0",
)

# CORS cho FE Next.js
# Lưu ý: nếu dùng allow_credentials=True thì KHÔNG dùng "*" cho origins theo spec.
# Hãy liệt kê rõ origin dev của bạn.
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://genvn-eoimxuvwe-qqs-projects-d8bf152f.vercel.app",
    "https://genvn-nytj104wd-qqs-projects-d8bf152f.vercel.app",
    "https://genvn-fe.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(upload.router,   prefix="/api", tags=["upload"])
app.include_router(export.router,   prefix="/api", tags=["export"])

@app.get("/")
def root():
    return {"message": "Backend chạy ok!"}

