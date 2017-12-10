from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key='mykey'
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'TheWall')

@app.route('/', methods=['GET'])
def index():
    if len(session.keys()) > 2:
        return redirect('/messageboard')
    else:
        return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    pw_hash = bcrypt.generate_password_hash(password)

    insert_query = "INSERT INTO users(first_name, last_name,  email, password, created_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW())"
    query_data = { 'first_name': first_name, 'last_name': last_name, 'email': email, 'pw_hash': pw_hash}
    mysql.query_db(insert_query, query_data)

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    query_data = { 'email': email }
    user = mysql.query_db(user_query, query_data)

    if bcrypt.check_password_hash(user[0]['password'], password):
        session['id']=user[0]['id']
        session['first_name']=user[0]['first_name']
        session['last_name']=user[0]['last_name']
        session['email']=user[0]['email']
        session['password']=user[0]['password']
        return redirect('/messageboard')
    else:
        flash(u'Wrong password used, please try again','error')
        return redirect('/')

@app.route('/messageboard', methods=['GET'])
def messageboard():
    if len(session.keys()) < 3:
        flash(u'Please login to access The Wall','error')
        return redirect('/')
    user_query_msgs = "SELECT u.first_name, u.last_name, DATE_FORMAT(u.created_at, \'%M %d %Y %h:%i%p\' ) as created_at, m.message, m.id FROM users as u join messages m on u.id=m.user_id order by m.created_at desc"
    messagerecords = []
    commentrecords = []
    resultsmsgs = mysql.query_db(user_query_msgs)
    for resultsmsg in resultsmsgs:
        resTuple = (resultsmsg['id'], resultsmsg['first_name'],resultsmsg['last_name'],resultsmsg['created_at'],resultsmsg['message'])
        messagerecords.append(resTuple)
        message_id = resultsmsg['id']
        user_query_cmts = "SELECT u.first_name, u.last_name, DATE_FORMAT(u.created_at, \'%M %d %Y %h:%i%p\' ) as created_at, c.comment, c.message_id, c.id FROM users as u join comments c on u.id=c.user_id where c.message_id=:message_id order by c.created_at desc"
        query_data = { 'message_id': message_id }
        resultscmts = mysql.query_db(user_query_cmts,query_data)
        for resultscmt in resultscmts:
            print 'Results: ' + str(resultsmsg['id']) + ' ' + str(resultscmt['id'])
            resTup = (resultscmt['first_name'],resultscmt['last_name'],resultscmt['created_at'],resultscmt['comment'],resultscmt['message_id'])
            commentrecords.append(resTup)
    print commentrecords
    return render_template("wall.html", MessageRecords = messagerecords, CommentRecords = commentrecords, FirstName=session['first_name'], LastName=session['last_name'])

@app.route('/post_message', methods=['POST'])
def post_message():
    user_id = session['id']
    message = request.form['message']

    insert_query = "INSERT INTO messages(user_id,  message, created_at) VALUES (:user_id, :message, NOW())"
    query_data = { 'user_id': user_id, 'message': message }
    mysql.query_db(insert_query, query_data)

    return redirect('/messageboard')

@app.route('/post_comment/<messageid>', methods=['POST'])
def post_comment(messageid):
    user_id = session['id']
    m_id = messageid
    comment = request.form['comment']

    insert_query = "INSERT INTO comments(message_id, user_id,  comment, created_at) VALUES (:message_id, :user_id, :comment, NOW())"
    query_data = { 'message_id': m_id, 'user_id': user_id, 'comment': comment }
    mysql.query_db(insert_query, query_data)

    return redirect('/messageboard')

@app.route('/logout')
def logout():
    for key in session.keys():
        session.pop(key)
    return redirect('/')
app.run(debug=True)
