import uvicorn
from os.path import join, abspath
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router
from core.config import settings

favicon_path = abspath(join(settings.BASE_DIR, "static", "favicon.ico"))
# print(favicon_path)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
