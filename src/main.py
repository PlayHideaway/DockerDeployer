from os import environ
import os
from fastapi import FastAPI, Body, Request, Depends
import json
from fastapi.exceptions import HTTPException

from fastapi.param_functions import Header
from fastapi_responses import custom_openapi
from auth import auth_hook, auth_web, check_ref


if not os.environ.get("DOCKER"):
    from dotenv import load_dotenv
    load_dotenv
    
app = FastAPI()

app.openapi = custom_openapi(app)

@app.get("/", dependencies=[Depends(auth_web)])
@app.post("/", dependencies=[Depends(auth_hook), Depends(check_ref)])
async def hook(req: Request):
    return "Update"


