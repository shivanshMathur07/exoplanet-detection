from flask import Flask,render_template,url_for
import pandas as pd
from prediction_helper import my_prediction

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("homepage.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/predict")
def predict():
    data = pd.read_csv("test data files/test_10.csv",skiprows=53)
    return(my_prediction.get_prediction(data))


if __name__ == "__main__":
    app.run(debug=True)