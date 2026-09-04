from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Engineering Workbench API",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }

