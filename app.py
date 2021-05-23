#import dependencies
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect)
import json
import pprint
import joblib
import pickle
import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

#set up app
app = Flask(__name__)

#set up routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/model", methods=["GET", "POST"])
def send():
    
    #postgres form setup and table vars
    if request.method == "POST":
        #get info from forms
        gender = request.form["gender"]
        income=request.form["income"]
        
# Opening JSON file
f = open('Resources\models_kelly\encoding_keys\offers_encoded.json')
  
# returns JSON object as a dictionary
data = json.load(f)
def decode(dictionary):
    dictionary['offer_id'] = dictionary['offer_id'].map({8:'Offer 7: The Americano',
                             2:'Offer 2: The Cold Brew',
                            1:'Offer 8: The Espresso',
                            3:'Offer 6: The Pourover',
                            0:'Offer 9: The Macchiato',
                            5:'Offer 5: The French Press',
                            4:'Offer 4: The Mocha',
                            9:'Offer 3: The Latte',
                            7:'Offer 10: The Cappuccino',
                            6:'Offer 1: The Doppio'},
                             na_action=None)
    dictionary['gender'] = dictionary['gender'].map({0:'M',
                                                    1: 'O',
                                                    2: 'F'})
    dictionary['channels'] = dictionary['channels'].map({1: "email, mobile, social",
                                                         3: "web, email, mobile",
                                                         0: "web, email, mobile, social",
                                                         2: "web, email"})
    dictionary['offer_type'] = dictionary['offer_type'].map({1: "informational",
                                                            2: "bogo",
                                                            0: "discount"})
    dictionary['offer_completed_y_n'] = dictionary['offer_completed_y_n'].map({0:"Yes",
                                                                        1: "No"})
    global decoded_predictions
    decoded_predictions = decoded_predictions.append(dictionary)
    final_df = decoded_predictions.sort_values('offer_completed_y_n', ascending = False).drop(['gender', 'income'], axis=1)
    return final_df.to_html(header="true", table_di = table)

g = gender
i = int(income)

def predictions():
    for dictionary in data:
        dictionary.update(gender = g, income = i,)
        complete_df = pd.DataFrame(dictionary, index=[0])[["offer_id", "gender", "income", "reward", "channels", "difficulty", "duration", "offer_type"]]
        complete_score = int(complete_knn.predict(complete_df))
        dictionary['offer_completed_y_n'] = complete_score
        new_dict = pd.DataFrame(dictionary, index=[0])
        decode(new_dict)

predictions()
f.close()
         
        
    # return render_template("model.html",table_data=table_data)

@app.route('/interviews/benfierce')
def ben():
    return render_template("ben.html")

@app.route('/interviews/jenkaslowon')
def jen():
    return render_template("jen.html")

@app.route('/disclaimer')
def disclaimer():
    return render_template("disclaimer.html")

@app.route('/casestudy/delmar')
def delmar():
    return render_template("delmar.html")

@app.route('/casestudy/showme')
def showme():
    return render_template('showme.html')

if __name__ == "__main__":
    app.run()