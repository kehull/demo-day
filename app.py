#import dependencies
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect)
import datetime as dt
import uuid
from schema import create_classes
import json
import pprint
import joblib
import pickle
import os
from schema import create_classes
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from flask_sqlalchemy import SQLAlchemy



#set up app
app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') or "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#set up routes
db = SQLAlchemy(app)

Customer = create_classes(db)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")

@app.route("/model", methods=["GET","POST"])
def send():
    #create empty list to transfer to html
    global table_data
    table_data=[]
    
    
    
    
    #postgres form setup and table vars
    if request.method == "POST":
        
        #get info from forms
        gender = request.form["gender"].upper() 
        income=request.form["income"]
        customer_id=uuid.uuid4().hex
        date=dt.datetime.today().strftime('%Y%m%d')
        
        #create and store sql session
        customer=Customer(customer_id=customer_id,gender=gender,income=income,membership_date=date)
        db.session.add(customer)
        db.session.commit() 
        
        #translate gender values to number for json dictionaries
        if gender== "M":
            gender=0
        elif gender=="O":
            gender=1
        else: 
            gender=2
        
        # Opening JSON file
        f = open('Resources/models_kelly/encoding_keys/offers_encoded.json')
        g = gender
        i = int(income) 
  
        # load in knn model and json
        complete_knn= joblib.load('Resources/models_kelly/complete_offer.pkl')
        data = json.load(f)
        
        # returns JSON object as a dictionaries
        for dictionary in data:
            
            #update dictionary with form values
            dictionary.update(gender = g, income = i,)
            
            #create variable for X values used in model
            model_data=[[dictionary['offer_id'],dictionary['gender'],dictionary['income'],dictionary['reward'],dictionary['channels'],dictionary['difficulty'],dictionary['duration'],dictionary['offer_type']]]
            complete_score = int(complete_knn.predict(model_data))
            
            #create key value for prediction
            dictionary['offer_completed_y_n']=complete_score
            
            #translate numbers into offer names
            if dictionary['offer_id'] ==8:
                dictionary['offer_id']='Offer 7: The Americano'
            elif dictionary['offer_id']==2:
                dictionary['offer_id']='Offer 2: The Cold Brew'
            elif dictionary['offer_id']==1:
                dictionary['offer_id']='Offer 8: The Espresso'
            elif dictionary['offer_id']==3:
                dictionary['offer_id']='Offer 6: The Pourover'
            elif dictionary['offer_id']==0:
                dictionary['offer_id']='Offer 9: The Macchiato'
            elif dictionary['offer_id']==5:
                dictionary['offer_id']='Offer 5: The French Press'
            elif dictionary['offer_id']==4:
                dictionary['offer_id']='Offer 4: The Mocha'
            elif dictionary['offer_id']==9:
                dictionary['offer_id']='Offer 3: The Latte'
            elif dictionary['offer_id']==7:
                dictionary['offer_id']='Offer 10: The Cappuccino'
            else:
                dictionary['offer_id']='Offer 1: The Doppio'
                             
            #translate gender back into abbreviations
            if dictionary['gender'] ==0:
                dictionary['gender']='M'
            elif dictionary['gender']==1:
                dictionary['gender']='O'
            else:
                 dictionary['gender']='F'
            
            #translate channels to respective strings
            if dictionary['channels'] ==1: 
                dictionary["channels"]="email, mobile, social"
            elif dictionary['channels']==3: 
                dictionary['channels']="web, email, mobile"
            elif dictionary['channels']==0: 
                dictionary['channels']="web, email, mobile, social"
            else:
                dictionary["channels"]="web, email"
            
            #translate offer types to respective strings
            if dictionary['offer_type'] ==1: 
                dictionary['offer_type']="informational"
            elif dictionary['offer_type']==2: 
                dictionary['offer_type']="bogo"
            else:
                dictionary['offer_type']="discount"
            
            if dictionary['offer_completed_y_n'] ==0:
                dictionary['offer_completed_y_n']="Yes"
            else:
                dictionary['offer_completed_y_n']="No"
            
            #append dictionary to table data
            table_data.append(dictionary)
        f.close()
        
         
        
    return render_template("model.html",table_data=table_data)

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

@app.route('/customer/api')
def customer():
    #set up api
    
    #query from db
    results = db.session.query(Customer.customer_id, Customer.gender,Customer.income,Customer.membership_date).all()
    
    #set up list of dictonaries to store end result
    customer_data = {"customer_data":[]}
    
    #loop through results and create dictionary
    for customer_id,gender,income,membership_date in results:
        test_data = {
            "customer_id": customer_id,
            "gender": gender,
            "income": income,
            "membership_date": membership_date
        }
        
        #append dictionary to customer_data
        customer_data["customer_data"].append(test_data)
    return jsonify(customer_data)
@app.route('/customer/api/gender/<gender>')
def gender(gender):
    #create a list for checking if the gender variable is valid
    gender_list=['M','F','O']
    
    # convert any entry to uppercase
    canonicalization=gender.upper()
    
    #check if in gender list
    if canonicalization in gender_list:
        
        #set up list of dictonaries to store end result
        json_dict={"customer_data":[]}
        
        #query from db
        results=db.session.query(Customer.customer_id, Customer.gender,Customer.income,Customer.membership_date).filter(Customer.gender==canonicalization)
         
         #loop through results and create dictionary
        for customer_id,gender,income,membership_date in results:
            test_dict={}
            test_dict["customer_id"]=customer_id
            test_dict["gender"]=gender
            test_dict["income"]=income
            test_dict["membership_date"]=membership_date
            
            #append to json_dict
            json_dict["customer_data"].append(test_dict)
    else:
        return f'Error! Gender not found. Try "M","F", or "O".',404
    return jsonify(json_dict)
   

@app.route('/customer/api/income/<income>')
def income(income):
    # convert any entry to uppercase
    canonicalization=int(income)
    
    #query db for income values
    income_results=db.session.query(Customer.income).all()
    
    #store income values to list
    income_list=[i[0] for i in income_results]
    
    #check if form is valid
    if canonicalization >= min(income_list):
        
        #query db
        results= db.session.query(Customer.customer_id,Customer.gender,Customer.income,Customer.membership_date).filter(Customer.income <= canonicalization)
        
        #set up list of dictonaries to store end result
        json_dict={"customer_data":[]}    
        
        #loop through results and create dictionary
        for customer_id,gender,income,membership_date in results:
            test_dict={}
            test_dict["customer_id"]=customer_id
            test_dict["gender"]=gender
            test_dict["income"]=income
            test_dict["membership_date"]=membership_date
            json_dict["customer_data"].append(test_dict)
        return jsonify(json_dict)
    else:
        return f"{income} is beyond the lower limit of the income range. Try entering a higher income value.",404
    

    


if __name__ == "__main__":
    app.run()