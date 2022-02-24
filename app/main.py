from fastapi import FastAPI, Request, Depends
from fastapi_responses import custom_openapi
from app.dependencies import auth_hook, auth_web
from os import getenv
import subprocess
from fastapi.exceptions import HTTPException

app = FastAPI()

app.openapi = custom_openapi(app)

@app.get("/", dependencies=[Depends(auth_web)])
@app.post("/", dependencies=[Depends(auth_hook)])
async def hook(req: Request):
    #json = await req.json()
    #print(json)
    service = getenv('SERVICE')
    print(service)
    resp = subprocess.run(["docker-compose", "-f", "docker-compose.yaml", "pull", service])
    if resp.returncode != 0:
        raise HTTPException(status_code=500, detail="Failed to pull Docker image")
    print(resp.returncode)
    resp = subprocess.run([f"docker-compose -f docker-compose.yaml up -d {service}"])
    if resp.returncode != 0:
        raise HTTPException(status_code=500, detail="Failed to relaunch container")
    return "Update"


