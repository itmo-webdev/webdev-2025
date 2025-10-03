# main.py
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_sso.sso.google import GoogleSSO

app = FastAPI()

GOOGLE_CLIENT_ID = "437883604921-nlvhkt9go7pjch4a1e4ggc32mff5hd8u.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"

google_sso = GoogleSSO(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    redirect_uri=GOOGLE_REDIRECT_URI,
)

@app.get("/auth-google")
async def auth_login():
    return await google_sso.get_login_redirect()

@app.get("/auth/google/callback")
async def auth_callback(request: Request):
    async with google_sso:
        sso_user = await google_sso.verify_and_process(request)

    return JSONResponse(
        {
            "provider": sso_user.provider,
            "id": sso_user.id,
            "email": sso_user.email,
            "name": sso_user.display_name,
            "picture": getattr(sso_user, "picture", None),
        }
    )

