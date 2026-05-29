import os
import pandas as pd

from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LogisticRegression as LR

import joblib 
from sklearn.metrics import classification_report

from sklearn.feature_extraction.text import TfidfVectorizer

# df=pd.read_csv("training_data.csv")

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "training_data.csv")
# python way of storing the trained data and loading it back into RAM when app restarts
# usually training data is lost when app closes so like RAM restarts again so to prevent it we use model.pkl
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")  

df=pd.read_csv(DATA_PATH)
df = df.dropna(subset=["text", "label"])
print(df.head())

# loading the model
X =df["text"]
y = df["label"]

X_train, X_test, y_train, y_test=tts(X,y,test_size=0.2,random_state=42)

#converting the data into numerical values
vectorizer=TfidfVectorizer()
X_train_tfidf=vectorizer.fit_transform(X_train)
X_test_vec=vectorizer.transform(X_test)

model=LR()
model.fit(X_train_tfidf,y_train)

# prediction
prediction=model.predict(X_test_vec)

# evaluating
print(classification_report(y_test, prediction))

# storing the training result in model.pkl
joblib.dump(model, os.path.join(BASE_DIR, "model.pkl"))
joblib.dump(vectorizer, os.path.join(BASE_DIR, "vectorizer.pkl"))
print("Training has been successfully stored in model.pkl") 