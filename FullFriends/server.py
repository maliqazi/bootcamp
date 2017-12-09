from flask import Flask, render_template, redirect, request, session, flash
import re
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)
app.secret_key='mykey'

mysql = MySQLConnector(app, 'friendships')

@app.route('/')
def index():
    results = mysql.query_db('SELECT id,first_name, last_name, email from fullfriends')
    emailrecords=[]
    for result in results:
        resTuple = (result['id'],result['first_name'],result['last_name'],result['email'])
        emailrecords.append(resTuple)
    return render_template('index.html', EmailRecords=emailrecords)

@app.route("/friends", methods = ['POST'])
def create():
    if  not EMAIL_REGEX.match(request.form['email']):
        flash(u'Invalid email address','error')
        return redirect('/')
    else:
        flash('The email address you entered (' + request.form['email'] +') is a Valid email address! Thank you!')
        dbqueryString = 'INSERT into \
                        fullfriends(first_name,last_name,email, create_dt, update_dt)\
                        values(\
                        \'' + request.form['first_name'] + '\',\
                        \'' + request.form['last_name'] + '\',\
                        \'' + request.form['email'] + '\'\
                        ,now(),now())'
        res =  mysql.query_db(dbqueryString)
    return redirect('/')

@app.route("/friends/<id>/edit", methods = ['GET'])
def edit(id):
    results = mysql.query_db('SELECT id,first_name, last_name, email from fullfriends where id = ' + id)
    friendRecords=[]
    for result in results:
        friend = (result['id'],result['first_name'],result['last_name'],result['email'])
    return render_template('edit.html', FriendInfo=friend)

@app.route("/friends/<id>", methods = ['POST'])
def update(id):
    dbqueryString = 'Update fullfriends \
                        set first_name = \'' + request.form['first_name'] + '\'\
                        ,last_name = \'' + request.form['last_name'] + '\'\
                        ,email = \'' + request.form['email'] + '\'\
                        ,update_dt = now() \
                     where id =' + id
    res =  mysql.query_db(dbqueryString)
    return redirect('/')

@app.route("/friends/<id>/delete", methods = ['POST'])
def destroy(id):
    dbqueryString = 'Delete from fullfriends where id =' + id
    res =  mysql.query_db(dbqueryString)
    return redirect('/')

app.run(debug=True)
