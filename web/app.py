from flask import Flask,render_template
import pandas as pd
from prediction_helper import my_prediction

# DUMMY_DATA = pd.DataFrame({"dummy1":[0],"dummy2":[0]})

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("navbar.html")

@app.route("/predict")
def predict():
    # DUMMY_DATA.to_csv("test data files/test1.csv",mode="a",index=False,header=False)
    data = pd.read_csv("test data files/test2.csv")
    return(my_prediction.get_prediction(data))


if __name__ == "__main__":
    app.run(debug=True)