from fastapi import FastAPI
from words.router import router, routerGet


app = FastAPI()

app.include_router(router)
app.include_router(routerGet)
