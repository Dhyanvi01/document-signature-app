from fastapi import FastAPI

app = FastAPI(title="Document Signature API")

@app.get("/health")
def health():
    return {"status": "ok"}
