from fastapi import FastAPI, Request, Depends

from fastapi.testclient import TestClient
import hmac
from app.main import app
from app.dependencies import auth_hook, auth_web
from os import environ, getenv
import json

environ['WEBHOOK_SECRET'] = "dfsgdsjghhgdaehlsdfjhjkdh"
environ["BRANCH"] = "master"
environ["TOKEN"] = "assdcvfgvh"
secret_key = getenv('WEBHOOK_SECRET')

client = TestClient(app)

@app.post("/test_auth", dependencies=[Depends(auth_hook)])
async def auth_test_handler(request: Request):
    return 200

@app.get("/test_web", dependencies=[Depends(auth_web)])
async def web_test_hnadler(request: Request):
    return 200

def test_auth():  
    payload = {"Hello":"World"}
    msg = json.dumps(payload).encode()
    mac = hmac.new(secret_key.encode(), msg=msg, digestmod='sha1').hexdigest()

    response = client.post("/test_auth", json= payload, headers={"X-Hub-Signature": "sha1="+mac}) 
    assert response.status_code == 200

    response = client.post("/test_auth", headers={"X-Hub-Signature": "sha1="+mac})  
    assert response.status_code == 204
    assert response.text == '{"detail":"Missing or bad content"}'

    response = client.post("/test_auth", json= payload, headers={"X-Hub-Signature": "sha="+mac}) 
    assert response.status_code == 400
    assert response.text == '{"detail":"Invalid signature"}'

    response = client.post("/test_auth", json=payload)  
    assert response.status_code == 400
    assert response.text == '{"detail":"Missing signature"}'

    response = client.post("/test_auth", json= payload, headers={"X-Hub-Signature": "sha1="+mac+"a"}) 
    assert response.status_code == 403
    assert response.text == '{"detail":"Unauthorized"}'
   

# def test_branch():
#     payload = {"ref": "refs/heads/master"}
#     response = client.post("/test_ref", json= payload)
#     assert response.status_code == 202

#     payload = {"ref": "refs/heads/test"}
#     response = client.post("/test_ref", json= payload)
#     assert response.status_code == 403

def test_web():
    response = client.get('/test_web?token={}'.format(getenv("TOKEN")))
    assert response.status_code == 200

    response = client.get('/test_web')
    assert response.status_code == 400

    response = client.get('/test_web?token=a')
    assert response.status_code == 403
