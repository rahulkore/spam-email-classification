#flask modules
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

#fraud determining modules
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

df = pd.read_csv('spam_ham_dataset.csv', encoding="latin-1")
#df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
#df['label'] = df['v1'].map({'ham': 0, 'spam': 1})
X = df['text']
y = df['label_num']
cv = CountVectorizer()
X = cv.fit_transform(X) # Fit the Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
#Naive Bayes Classifier
clf = MultinomialNB()
clf.fit(X_train,y_train)
clf.score(X_test,y_test)
y_pred = clf.predict(X_test)
#print(classification_report(y_test, y_pred))


#from sklearn.externals import joblib
#joblib.dump(clf, 'NB_spam_model.pkl')


#NB_spam_model = open('NB_spam_model.pkl','rb')
#clf = joblib.load(NB_spam_model)
app = Flask(__name__)
@app.route("/")
def home1():
    return "ok"
@app.route('/register/<data>',methods=["GET"])
def home(data):
    #from sklearn.externals import joblib
    #cv = CountVectorizer()
    #NB_spam_model = open('NB_spam_model.pkl','rb')
    #clf = joblib.load(NB_spam_model)
    data = data.split("%20")
    data = str(data).replace("[","").replace("]","")

    #return data
    #data = cv.fit_transform(data)
    data = [data]
    #return data
    print(data)
    data = cv.transform(data).toarray()
    #print(data)
    result = clf.predict(data)
    if result==[0]:
        return "fair"
    else:
        return "fraudulent"
    #return render_template("home.html")

#data = "Are you looking for powerful online marketing that isn't full of crap? Sorry to bug you on your contact form but actually that's exactly where I wanted to make my point. We can send your ad copy to websites via their contact pages just like you're getting this message right now. ... "
#data = "hurrayyyyy, you have won a lottery and if you want your prize money then please enter your credit card details."
#data = [data]
#data = cv.transform(data).toarray()
#print(data)
#result = clf.predict(data)
#print(result)
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
