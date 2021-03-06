from os import getenv
import hmac
from fastapi import Request
from fastapi.exceptions import HTTPException

async def auth_hook(request: Request):
    try:
        text = await request.body()
        json = await request.json()

    except:
        raise HTTPException(status_code=204, detail="Missing or bad content")
    
    header_signature = request.headers.get('X-Hub-Signature')
    if not header_signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    # separate the signature from the sha1 indication
    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        raise HTTPException(status_code=400, detail="Invalid signature")

    secret_key = getenv('WEBHOOK_SECRET')
    if secret_key is None:
        raise HTTPException(status_code=503, detail="Missing WEBHOOK_SECRET")

    # create a new hmac with the secret key and the request data
    mac = hmac.new(secret_key.encode(), msg=text, digestmod='sha1')

    # verify the digest matches the signature
    if not hmac.compare_digest(mac.hexdigest(), signature):
        raise HTTPException(status_code=403, detail="Unauthorized")

async def auth_web(request: Request):
    token = request._query_params.get("token")
    if token == None or token == "":
        raise HTTPException(status_code=400, detail="Missing token")
    if token == getenv("TOKEN"):
        return
    raise HTTPException(status_code=403, detail="Invalid token")