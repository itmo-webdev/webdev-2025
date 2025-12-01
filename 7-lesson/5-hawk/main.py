from hawk_python_sdk.modules.fastapi import HawkFastapi

from fastapi import FastAPI, Request

app = FastAPI()

def set_user(request: Request):
    request.header.token
    return {'user_id': 1}

hawk = HawkFastapi({
    'app_instance': app,
    'token': 'eyJpbnRlZ3JhdGlvbklkIjoiNWM2YWY0NzAtN2MyZS00ZDU2LTk3OTMtYjU1OWMxMjQ5NjA4Iiwic2VjcmV0IjoiMDdmODFiNDMtMWFiZC00YzVmLTk0MmYtMTA0YzE4M2IyMDNjIn0='
    'set_user': 
})

@app.get("/")
def index():
    hawk.send(ValueError("error description"), {"params": "value"})

@app.get("/compute")
def compute():
    x = x / 0
    return {"result": x}