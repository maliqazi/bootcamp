from flask import Flask, render_template, redirect, request, session, flash
import re
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)
app.secret_key='mykey'

mysql = MySQLConnector(app, 'books')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/emailvalidation", methods = ['POST','GET'])
def emailValidation():
    if  not EMAIL_REGEX.match(request.form['email']):
        flash(u'Invalid email address','error')
        return redirect('/')
    else:
        flash('The email address you entered (' + request.form['email'] +') is a Valid email address! Thank you!')
        dbqueryString = 'INSERT into emails(EmailAddress, create_dt, update_dt)values(\'' + request.form['email'] + '\',now(),now())'
        print dbqueryString
        res =  mysql.query_db(dbqueryString)
        return redirect('/success')

@app.route("/success", methods = ['POST','GET'])
def success():
    results = mysql.query_db('SELECT EmailAddress, DATE_FORMAT(create_dt, \'%m/%d/%y %h:%i%p\'  ) from emails')
    EmailRecord=[]
    for result in results:
        EmailRecord.append(str(result['EmailAddress']) + '   ' + str(result['DATE_FORMAT(create_dt, \'%m/%d/%y %h:%i%p\'  )']))
    print EmailRecord
    print results
    return render_template('emails.html', records=EmailRecord)

app.run(debug=True)
