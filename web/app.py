from flask import Flask,render_template,url_for,session,redirect,request
import pandas as pd
from prediction_helper import my_prediction
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABC2334@fnf@@/jhg'


@app.route('/',methods = ['GET','POST'])
def index():
    if(request.method == 'POST'):
        uploaded_file = request.files['file_upload']
        uploaded_file.save(f"web/test_files/uploads/{secure_filename(uploaded_file.filename)}")
        session['file_name'] = secure_filename(uploaded_file.filename)
        return redirect("/predict")
    else:
        if 'result' in session:
            if(session['result'] == 'Exoplanet Candidate'):
                candidate=session['result']
                session.pop('result',None)
                return render_template("homepage.html",candidate=candidate)
            else:
                false_positive=session['result']
                session.pop('result',None)
                return render_template("homepage.html",false_positive=false_positive)
        else:
            return render_template("homepage.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/predict")
def predict():
    if 'file_name' in session:
        data_file_path = f"web/test_files/uploads/{session['file_name']}"
        data = pd.read_csv(data_file_path,skiprows=53)
        session['result'] = my_prediction.get_prediction(data)
        return redirect(url_for('index'))
    else:
       return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)