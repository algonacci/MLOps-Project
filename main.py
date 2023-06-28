from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {
        "status": {
            "code": 200,
            "message": "Success fetching the API"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
