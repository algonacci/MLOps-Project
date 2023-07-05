import os
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import warnings

app = FastAPI()
warnings.filterwarnings("ignore")


class TextInput(BaseModel):
    text: str


model = pickle.load(open('spam.pkl', 'rb'))
cv = pickle.load(open('vectorizer.pkl', 'rb'))


@app.get("/")
def index():
    return {
        "status": {
            "code": 200,
            "message": "Success fetching the API"
        }
    }


@app.post("/predict")
def predict_spam(text_input: TextInput):
    data = text_input.text.strip()
    if not data:
        raise HTTPException(status_code=400, detail="Empty input text")

    vec = cv.transform([data]).toarray()
    result = model.predict(vec)
    if result[0] == 0:
        return {"prediction": "Ham"}
    else:
        return {"prediction": "Spam"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,
                host="0.0.0.0",
                port=int(os.environ.get("PORT", 8080)))
