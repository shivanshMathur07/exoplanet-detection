from flask import Flask,render_template
import pandas as pd
from prediction_helper import my_prediction

app = Flask(__name__)

# 127.0.0.1:5000/predict

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route("/predict")
def predict():
    # DUMMY_DATA.to_csv("test data files/test1.csv",mode="a",index=False,header=False)
    data = pd.read_csv("test data files/test2.csv")
    return(my_prediction.get_prediction(data))


if __name__ == "__main__":
    app.run(debug=True)