from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from api.v1 import auth, criteria, evidence, user

def get_application() -> FastAPI:
    application = FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    application.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    application.include_router(criteria.router, prefix="/api/v1", tags=["criteria"])
    application.include_router(evidence.router, prefix="/api/v1", tags=["evidence"])
    application.include_router(user.router, prefix="/api/v1", tags=["User"])

    return application

app = get_application()
# if __name__ == '__main__':
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)