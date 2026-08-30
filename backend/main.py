from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import connect_to_mongodb, close_mongodb_connection
from routes import auth, user, bank, i4c

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()

app = FastAPI(
    title="Durgam API",
    description="Mule Account Detection & I4C Cyber Crime Coordination System",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(bank.router, prefix="/api/bank", tags=["Bank"])
app.include_router(i4c.router, prefix="/api/i4c", tags=["I4C"])

@app.get("/")
async def root():
    return {"message": "Durgam API is running 🚀", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
