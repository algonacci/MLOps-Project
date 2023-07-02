import os
import pickle
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
    data = [text_input.text]
    vec = cv.transform(data).toarray()
    result = model.predict(vec)
    if result[0] == 0:
        return {"prediction": "This is Not A Spam Email"}
    else:
        return {"prediction": "This is A Spam Email"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,
                host="0.0.0.0",
                port=int(os.environ.get("PORT", 8080)))
