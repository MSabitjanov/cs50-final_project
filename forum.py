from flask import Flask, render_template, session, request, redirect
import datetime
import sys

# sys.path.append('C:\\Users\\ACER\\Documents\\UzInfocom\\FORUM')

from database import ForumDB
import sqlite3
from functionality import *
import os
from werkzeug.utils import secure_filename
from cs50 import SQL
from PIL import Image
# from .filters import *


app = Flask(__name__)
app.secret_key = 'verysecret'
xy = datetime.datetime.now()


# creating instance to forum db
DB = ForumDB()

@app.route('/')
def home():
    # selecting top 5 questions according like
    topQues = DB.select_top_ques()
    leng = len(topQues)
    
    if session and session['status'] == 'admin':
        return render_template('forum.html', t = topQues, leng = leng, status = session['status'])
    else:        
        return render_template('forum.html', t = topQues, leng = leng)

@app.route('/login', methods=['POST', 'GET'])
def login():  

    if request.method == 'POST':

        uname = request.form['uname']
        password = request.form['password']

        password = hash_pass(password)

        data = DB.select_login_data(uname, password)

        topQues = DB.select_top_ques()
        leng = len(topQues)
        
        try:
            if data[0]['username'] == uname and data[0]['password'] == password:
                session['uname'] = uname
                session['password'] = password
                # selecting the status of user
                status = DB.selectStatus(uname)        
                session['status'] = status[0]['status']
                # selecting the ban status from database
                ban = DB.select_ban_status(uname)
                session['ban'] = ban[0]['ban']
                
                if session['status'] == 'admin':
                    return render_template('forum.html', t = topQues, leng = leng, status = session['status'])
                else:
                    return render_template('forum.html', t = topQues, leng = leng)
        except:
            return "Check your username or password. May be you should <a href=http://localhost:55/register>register yourself</a>"
    else:
        return render_template('login.html')

@app.route('/edit_profile', methods=["POST", "GET"])
def edit_profile():

    # user can edit profile if he already registered
    if "uname" in session and "password" in session:        
        r = session['uname']
        u = session['password']

        if request.method == "POST":
            x = request.form

            if x['action'] == "Submit":
                fname = request.form['name']  
                lname = request.form['lname']
                uname = request.form['uname']
                email = request.form['email']                

                DB.update_user_info(fname, lname, uname, email, r, u)

            elif x['action'] == "Confirm":
                try:
                    curr = request.form['current'] 
                    new_pass = request.form['new']
                    new_pass = hash_pass(new_pass)

                    DB.update_user_password(new_pass, r, u)
                except:
                    return "Password not matching"                

            elif x['action'] == "Upload":
                # getting photo and filter from user
                photo = request.files['user_photo']            
                filters = request.form['filter']
                
                # checking for uploaded image, if empty insert default user image
                image = upload_user_photo(photo, filters, session['uname']) 
                print        
                try:
                    DB.upload_user_photo(image, r, u)
                except:
                    print('Something went wrong!!!')
            return redirect('/');
        else:
            return redirect('/preedit');
    else:
        return render_template('login.html')

@app.route('/cabinet', methods=['POST', 'GET'])
def cabinet():
    # entering to cabinet    
    if "uname" in session and "password" in session:
        uname = session['uname']

        if request.method == 'POST':           
            mof =  request.form.get('moderate')
            ban =  request.form.get('ban')

            if mof == 'moderate':
                # selecting questions with hidden status
                hiddenQues = DB.select_hidden_ques()
                leng = len(hiddenQues)

                return render_template('hidden.html', q = hiddenQues, leng = leng)

            elif ban == 'ban':
                # selecting all banned users
                bannedUsers = DB.select_all_banned()
                leng = len(bannedUsers)

                return render_template('ban.html', b = bannedUsers, leng = leng)

        else:
            #selecting all user questions 
            userQuestions = DB.select_user_questions(uname)
            leng = len(userQuestions)

            return render_template('cabinet.html', q = userQuestions, leng = leng, status = session['status'])

    else:
        return render_template("login.html")

    # return render_template("login.html")

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == "POST":
        x = request.form

        if x['action'] == "Confirm":

            # getting personal info from user
            fname = request.form['name']  
            lname = request.form['lname']
            uname = request.form['uname']
            email = request.form['email']

            # protecting the system from entering whitespaces, if True(Ok, good)
            if checkME(fname, lname, uname) == False:
                return "No, no! Not allowed, Bro, Sorry :-("

            # checking username for uniqueness, true(exist), false(not exists)
            if DB.CheckUname(uname) == True:
                return "Bro, username already exists. Try to choose another one, Ok Bro?"

            # getting password from user
            new_pass = request.form['current'] 
            confirm = request.form['new']
            if new_pass != confirm:
                return "Oh, dude, your passwords not matching!"

            password = hash_pass(confirm)

            
            # checking if user exists
            if DB.user_exist(email) == True:
                return "Hmm, seems your account with this email already exists!"        

            # getting photo and filter from user
            photo = request.files['photo']           
            filters = request.form['filter']

            # checking for uploaded image, if empty insert default user image
            image = upload_user_photo(photo, filters, uname) 

            DB.insert_personal_info(fname, lname, uname, email, password, image)   

        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/preedit')
def preedit():
    try:
        namee = session['uname']
        password = session['password']

        a = DB.get_user_info(namee, password)

        return render_template('edit_profile.html', fname = a[0]['fname'], lname = a[0]['lname'], username = a[0]['username'], email = a[0]['email'])
    except:
        return render_template('login.html') 

@app.route('/ask', methods=['POST', 'GET'])
def ask():
    if request.method == 'POST':
        if "uname" in session and "password" in session:
            title = request.form['header'].strip()
            body = request.form['explanation'].strip()
            category  = request.form['category']
            time = xy.strftime('%d-%m-%Y')
            uname = session['uname']            
            questionid = uname + str(xy).replace(" ", "")            

            if title == "" or body == "":
                return "No, no! Not allowed, Bro, Sorry :-("

            # inserting question info into questions db
            DB.InsertQuestion(uname, questionid, time, title, body, category)

            return redirect('/');
    elif "uname" in session and "password" in session:
        if session['ban'] != 'ok':            
            return "<h2>Oh, Bro seems you are banned</h2>"

        # selecting all category from categories db
        category = DB.selectCategory()        
        len_of = len(category)
        
        return render_template('ask.html', lenf = len_of, ctgry = category)
    else:
        return "<h2><a href=http://localhost:55/login>Log In first!</a></h2>"

@app.route('/questions', methods=['POST', 'GET'])
def questions():
    # implementing like and comment counters
    if request.method == 'POST':      
        if "uname" in session and "password" in session:           
            button = request.form['ques'].split('$')
            uname = session['uname']
            # page = request.form['page']
            # print(page)
          
            if button[0] == 'hiden' or button[0] == 'show':
                DB.update_ques_status(button)
            
            elif button[0] == 'banned' or button[0] == 'ok':
                DB.ban_user(button[0], button[1])
                session['ban'] = button[0]

            if button[0] == 'like':
                # checking the like table if user already liked the message true means liked
                data = DB.checkLike(uname, button[1])
                if data == False:
                    DB.updateLike('increase', uname, button[1])
                elif data == True:
                    DB.updateLike('decrease', uname, button[1])
            elif button[0] == 'comment':
                # selecting question with specific id
                questions = DB.select_ques(button[1])    

                # selecting all comments which belongs to paticular questionid
                comments = DB.select_comments(button[1])
                lend = len(comments) 

                photo = DB.select_photo(session['uname'])   

                return render_template('comment.html', q = questions, c = comments, lend = lend)

            questions = DB.selectAllQuestions()
            leng = len(questions)    

            # selecting all comments which belongs to paticular questionid
            comments = DB.select_comments(button[1])
            lend = len(comments)            

            paginate = DB.get_page()

            if session['status'] == 'admin':
                return render_template('admin_question.html', q = questions, leng = leng, com = lend, p = paginate)
            else:            
                return render_template('questions.html', q = questions, leng = leng, com = lend, p = paginate)

        else:
            return "<h2><a href=http://localhost:55/login?>Log In first!</a></h2>"

    else:
        # selecting all questions from questions db(limit=10)
        questions = DB.selectAllQuestions()
        leng = len(questions)
        
        paginate = DB.get_page()
        
        if not session:
            return render_template('questions.html', q = questions, leng = leng, p = paginate)
        elif session['status'] == 'user':
            return render_template('questions.html', q = questions, leng = leng, p = paginate)
        elif session['status'] == 'admin':
            return render_template('admin_question.html', q = questions, leng = leng, p = paginate)
        else:
            return "Sorry man, something went wrong! I will tell about this to my creator. Thank you for your understanding!"
        
       

@app.route('/category', methods=['POST', 'GET'])
def category():
    if request.method == 'POST':
        category = request.form['category']

        # selecting all existing categories from database
        categories = DB.selectCategory()
        lex = len(categories)

        # selecting all messages with specific category
        messages = DB.select_messages(category)
        len_of_messages = len(messages)

        if not messages:
            return "<h2><a href=http://localhost:55/ask?>NO messages on this category, You can be the first!</a></h2>"

        return render_template('category.html', categ = categories, lex = lex, messages = messages, lengz = len_of_messages)
        
    else:
        # selecting all existing categories from database
        categories = DB.selectCategory()
        lex = len(categories)

        # selecting all messages with specific category
        messages = DB.select_messages('Other')
        len_of_messages = len(messages)

        return render_template('category.html', categ = categories, lex = lex, messages = messages, lengz = len_of_messages)

@app.route('/comment', methods=['POST', 'GET'])
def comment():
    if request.method == 'POST':
        if "uname" in session and "password" in session:
            quesid = request.form['comment']
            uname = session['uname']
            date = xy.strftime('%d-%m-%Y')
            avatar = uname + '.png'
            comment = request.form['input'].strip()

            if not comment or len(comment) > 100:
                return "<h2>Invalid input, Please check!</h2>"

            #wring new comments to comments table
            DB.add_comment(quesid, uname, date, comment, avatar)
            DB.update_comment_count(quesid)

            questions = DB.select_ques(quesid)    

            # selecting all comments which belongs to paticular questionid
            comments = DB.select_comments(quesid)
            lend = len(comments) 
            
            photo = DB.select_photo(session['uname'])    
            
            return render_template('comment.html', q = questions, c = comments, lend = lend, photo = photo)

        else:
            return render_template('login.html')

@app.route('/paginate', methods=['POST', 'GET'])
def paginate():
    
    page = request.form['page']
    
    questions = DB.get_questions(int(page))
    leng = len(questions)
    paginate = DB.get_page()

    if session['status'] == 'admin':
        return render_template('admin_question.html', q = questions, leng = leng, p = paginate)

    return render_template('questions.html', q = questions, leng = leng, p = paginate)

@app.route('/search', methods=['POST', 'GET'])
def search():

    search = request.form['search']
    data =  DB.search(search)
    leng = len(data)

    paginate = DB.get_page()

    if session['status'] == 'admin':
        return render_template('admin_question.html', q = data, leng = leng, p = paginate)

    return render_template('questions.html', q = data, leng = leng, p = paginate)

app.run(host='localhost', port=55)