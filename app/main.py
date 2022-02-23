from fastapi import FastAPI, Request, Depends
from fastapi_responses import custom_openapi
from app.dependencies import auth_hook, auth_web

app = FastAPI()

app.openapi = custom_openapi(app)

@app.get("/", dependencies=[Depends(auth_web)])
@app.post("/", dependencies=[Depends(auth_hook)])
async def hook(req: Request):
    json = await req.json()
    print(json)
    return "Update"


