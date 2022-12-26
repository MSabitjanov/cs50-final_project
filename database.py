import sqlite3
from cs50 import SQL

# db = SQL("sqlite:///../sqlite-tools-win32-x86-3390000/forumdb")

# db.execute('''CREATE TABLE questions (
#                                         id integer PRIMARY KEY,
#                                         uname text NOT NULL,
#                                         questionid text NOT NULL,
#                                         time text NOT NULL,                              
#                                         title text NOT NULL,
#                                         body text NOT NULL,
#                                         likes integer NOT NULL,
#                                         );''')

# db.execute(''' ALTER TABLE questions ADD category TEXT NOT NULL DEFAULT 'Other'; ''')

class ForumDB:
    def __init__(self):
        self.db = SQL("sqlite:///forumdb")

    # query for selecting user(with email) in order to check if user already exists
    def user_exist(self, email):
        x = self.db.execute(''' SELECT email FROM registration WHERE email = ?; ''', email)
        if not x:
            return False
        else: 
            return True


    # selecting top 5 questions according like
    def select_top_ques(self):
        topQues = self.db.execute(''' SELECT * FROM questions ORDER BY likes DESC LIMIT 5; ''')
        return topQues

    # inserting registered user data to db
    def insert_personal_info(self, fname, lname, uname, email, password, photo):
        self.db.execute(''' INSERT INTO registration (fname, lname, username, email, password, photo, status) VALUES (?, ?, ?, ?, ?, ?, ?);''', fname, lname, uname, email, password, photo, 'user')

    # checkin if user already registered or not 
    def select_login_data(self, uname, password):
        x = self.db.execute(''' SELECT username, password FROM registration WHERE username = ? AND password = ?; ''', uname, password)
        return x

    # getting user info for edit page value
    def get_user_info(self, namee, password):
        x = self.db.execute(''' SELECT fname, lname, username, email FROM registration WHERE username = ? AND password = ?; ''', namee, password)
        return x

    # updating user personal info
    def update_user_info(self, fname, lname, uname, email, r, u):
        self.db.execute(''' UPDATE registration SET fname = ?, lname = ?, username = ?, email = ? WHERE username = ? AND password = ?; ''', fname, lname, uname, email, r, u)

    # updating user password
    def update_user_password(self, password, r, u):
        self.db.execute(''' UPDATE registration SET password = ? WHERE username = ? AND password = ?; ''', password, r, u)

    # updating user photo
    def upload_user_photo(self, image, r, u):
        self.db.execute(''' UPDATE registration SET photo = ? WHERE username = ? AND password = ?; ''', image, r, u)

    # checking username for uniqueness, true(exist), false(not exists)
    def CheckUname(self, uname):
        x = self.db.execute(''' SELECT username FROM registration WHERE username = ?; ''', uname)
        if not x:
            return False
        else: 
            return True

    # inserting question info into questions db
    def InsertQuestion(self, uname, questionid, time, title, body, category):
        self.db.execute(''' INSERT INTO questions (uname, questionid, time, title, body, likes, comment, category) VALUES (?,?,?,?,?,?,?,?); ''', uname, questionid, time, title, body, 0, 0, category)

    # selecting all questions from questions db(limit=10)
    def selectAllQuestions(self):
        q = self.db.execute(''' SELECT * FROM questions WHERE status = ? ORDER BY id DESC LIMIT ?, ?; ''', 'show', 0, 2)
        return q

    # selecting all category from categories db
    def selectCategory(self):
        category = self.db.execute(''' SELECT * FROM categories; ''' )
        return category

    #selecting photo name of user
    def select_photo(self, uname):
        photo = self.db.execute(''' SELECT photo FROM registration WHERE username = ?; ''', uname)        
        return photo[0]['photo']

    # checking the like table if user already liked the message true means liked
    def checkLike(self, uname, quesId):
        data = self.db.execute(''' SELECT uname, quesId FROM like WHERE uname = ? AND quesId = ?; ''', uname, quesId)
        
        if not data: 
            return False
        else:
            return True

    def search(self, search):
        # search1 = '%' + search + '%'
        # search2 = '%' + search + '%'
        # print(search1)
        data = self.db.execute(''' SELECT * FROM questions WHERE title LIKE ? or body LIKE ?; ''', '%' + search + '%', '%' + search + '%')
        return data

    # updating the like counter of question
    def updateLike(self, val, uname, quesid):
        if val == 'increase':
            likes = self.db.execute(''' SELECT likes FROM questions WHERE questionid = ?; ''', quesid )
            likes = likes[0]['likes'] + 1
            self.db.execute(''' UPDATE questions SET likes = ? WHERE questionid = ?; ''', likes, quesid )
            self.db.execute(''' INSERT INTO like (uname, quesId) VALUES (?, ?); ''', uname, quesid)
        elif val == 'decrease':
            likes = self.db.execute(''' SELECT likes FROM questions WHERE questionid = ?; ''', quesid )
            likes = likes[0]['likes'] - 1
            self.db.execute(''' UPDATE questions SET likes = ? WHERE questionid = ?; ''', likes , quesid )
            self.db.execute(''' DELETE FROM like WHERE quesId = ?; ''', quesid)

    # selecting all messages with specific category
    def select_messages(self, category):
        messages = self.db.execute(''' SELECT * FROM questions WHERE category = ?; ''', category)
        return messages

    # selecting questions based on user search from questions 
    def selectUserQuestions(self, word):
        questions = self.db.execute(''' SELECT * FROM questions WHERE title LIKE '%' + ? + '%' OR body LIKE '%' + ? +'%'; ''', word, word)
        return questions

    # selecting the status of user
    def selectStatus(self, uname):
        status = self.db.execute(''' SELECT status FROM registration WHERE username = ?; ''', uname)
        return status

    # updating question status (show or hide)
    def update_ques_status(self, button):
        self.db.execute(''' UPDATE questions SET status = ? WHERE questionid = ?; ''', button[0], button[1])

    #selecting all user questions 
    def select_user_questions(self, uname):
        userQuestions = self.db.execute(''' SELECT * FROM questions WHERE uname = ?; ''', uname)
        return userQuestions

    # selecting questions with hidden status
    def select_hidden_ques(self):
        hiddenQues = self.db.execute(''' SELECT * FROM questions WHERE status = ?; ''', 'hiden')
        return hiddenQues

    # selecting the ban status from database
    def select_ban_status(self, uname):
        ban = self.db.execute(''' SELECT ban FROM registration WHERE username = ?; ''', uname)
        return ban

    def ban_user(self, button, username):
        self.db.execute(''' UPDATE registration SET ban = ? WHERE username = ?; ''', button, username)

    # selecting all banned users
    def select_all_banned(self):
        bannedUsers = self.db.execute(''' SELECT fname, lname, username FROM registration WHERE ban = ?; ''', 'banned')
        return bannedUsers

    # selecting the list of all users
    def select_all_users(self):
        data = self.db.execute(''' SELECT id, fname, lname, username, email FROM registration; ''')
        users = str()
        for i in range(len(data)):
            users = users + str(data[i]['id']) + ' ' + data[i]['fname'] + ' ' + data[i]['lname'] + ' ' + data[i]['username'] + ' ' + data[i]['email'] + '\n'
        return users

    # adding new category to categories
    def add_category(self, category):
        try:
            data = self.db.execute(''' SELECT category FROM categories WHERE category = ?; ''', category)
            
            if data:
                return "Name already exists!"
            self.db.execute(''' INSERT INTO categories (category) VALUES (?); ''', category)
            return "Success"
        except:
            return "Something went wrong"

    # selecting all categories from categories table
    def select_category(self):
        data = self.db.execute(''' SELECT id, category FROM categories; ''')
        category = str()
        for i in range(len(data)):
            category = category + str(data[i]['id']) + ' ' + data[i]['category'] + '\n'

        return category

    # selecting question with specific id
    def select_ques(self, id):
        ques = self.db.execute(''' SELECT * FROM questions WHERE questionid = ?; ''', id)
        return ques

    # returning number of pages 
    def get_page(self):
        pages = self.db.execute(''' SELECT COUNT(id) FROM questions; ''')
        
        if int(pages[0]['COUNT(id)']) % 2 == 0:
            return int(pages[0]['COUNT(id)'] / 2)
        
        return int(pages[0]['COUNT(id)'] / 2 ) + 1

    # selecting the questions for pagination
    def get_questions(self, page):
        y = 2 * page
        x = y - 2

        ques = self.db.execute(''' SELECT * FROM questions WHERE status = ? ORDER BY id DESC LIMIT ?, ?; ''', 'show', x, 2)
        
        return ques
 
    # selecting all comments which belongs to paticular questionid
    def select_comments(self, id):
        comments = self.db.execute(''' SELECT * FROM comments WHERE questionid = ? ''', id)
        return comments

    #wring new comments to comments table
    def add_comment(self, questionid, user, date, comment, avatar):
        self.db.execute(''' INSERT INTO comments (questionid, user, date, comment, avatar) VALUES (?, ?, ?, ?, ?); ''', questionid, user, date, comment, avatar)
    
    def update_comment_count(self, quesid):
        com = self.db.execute(''' SELECT comment FROM questions WHERE questionid = ?; ''', quesid )
        com = com[0]['comment'] + 1
        self.db.execute(''' UPDATE questions SET comment = ? WHERE questionid = ?; ''', com, quesid )

    # editing the category
    def edit_categ(self, msg):
        try:
            data = self.db.execute(''' SELECT category FROM categories WHERE category = ?; ''', msg[1])
            print('Ok1')
            if data:
                return "Name already exists!"
            print('Ok2')
            self.db.execute(''' UPDATE categories SET category = ?  WHERE id = ?; ''', msg[1], msg[0])
            print('Ok3')
            return "Success"
        except:
            return "Something went wrong. Probably no category under this number! \n Check Men!"

    def info_user(self, msg):
        data = self.db.execute(''' SELECT * FROM registration WHERE username = ?; ''', msg)

        if not data:
            return "No user with <i><b>{}</b></i> username".format(msg)

        info = str()
    
        info = info + '<b>id: </b>' + str(data[0]['id']) + '\n'
        info = info + '<b>first name: </b>' + '<i>' + data[0]['fname'] + '</i>' + '\n'
        info = info + '<b>last name: </b>' + '<i>' + data[0]['lname'] + '</i>' + '\n'
        info = info + '<b>username: </b>' + data[0]['username'] + '\n'
        info = info + '<b>email: </b>' + data[0]['email'] + '\n'
        info = info + '<b>status: </b>' + data[0]['status'] + '\n'

        return info

        


# DB = ForumDB()
# x = DB.update_user_passwordd('f99b26b5edc4f754d046cb7d550e20e3bec895fe7fb71f12408e1d5a3033e3a8')
# print(x)