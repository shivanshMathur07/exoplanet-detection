import pickle
import pandas as pd

import warnings
warnings.filterwarnings(action='ignore')

model_path = "web\prediction_helper\my_model.pickle"

pickle_in = open(model_path,"rb")
trained_model = pickle.load(pickle_in)

def get_prediction(data):
    # print(data.shape)
    data = data.drop(['kepid','kepoi_name','kepler_name','koi_pdisposition','koi_disposition','koi_score','koi_teq_err1','koi_teq_err2'],axis=1)
    data['koi_tce_delivname'] = data['koi_tce_delivname'].fillna(data['koi_tce_delivname'].mode()[0])
    #for filling numerical empty values
    for col in data.columns[data.isna().sum() > 0] :
        data[col] = data[col].fillna(data[col].mean())
    #since we have a categorical column, encoding it to numerical form
    delivname_dummies = pd.get_dummies(data['koi_tce_delivname'], prefix='delivname')
    data = pd.concat([data, delivname_dummies], axis=1)
    data = data.drop('koi_tce_delivname', axis=1)
    #since we have to add two new features in data we are using dummies
    if('delivname_q1_q16_tce' in data.columns):
        data['delivname_q1_q17_dr25_tce'] = 0
        data['delivname_q1_q17_dr24_tce'] = 0
    elif('delivname_q1_q17_dr24_tce' in data.columns):
        data['delivname_q1_q16_tce'] = 0
        data['delivname_q1_q17_dr25_tce'] = 0
    elif('delivname_q1_q17_dr25_tce' in data.columns):
        data['delivname_q1_q16_tce'] = 0
        data['delivname_q1_q17_dr24_tce'] = 0
    results = trained_model.predict(data)
    if(results[0] == 1):
        return("Exoplanet Candidate")
    else:
        return("False Positive Candidate")


