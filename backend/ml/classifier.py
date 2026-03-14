import joblib
import os


BASE_DIR = os.path.dirname(__file__)
# python way of storing the trained data and loading it back into RAM when app restarts
# usually training data is lost when app closes so like RAM restarts again so to prevent it we use model.pkl
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH=os.path.join(BASE_DIR, "vectorizer.pkl")

model=joblib.load(MODEL_PATH)
vectorizer=joblib.load(VECTORIZER_PATH)

def predict_email(text: str):
    new_text=vectorizer.transform([text])
    # returning the label and the confidence score
    return (model.predict(new_text)[0], max(model.predict_proba(new_text)[0]))