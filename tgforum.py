import json
from database import ForumDB
import requests

TOKEN = "5466989984:AAHIwjOaHUMHPkMNlGqRtta_T8oWx9L_1bg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


DB = ForumDB()
last_msg = 'none'

def send_msg(msg):
    url = URL + 'sendMessage?chat_id=224133650&text={}'.format(msg) + '&parse_mode=HTML&reply_markup='
    requests.post(url)

def send_photo(msg):
    try:
        url = URL + 'sendPhoto'
        requests.post(url, {'chat_id': '224133650', }, files = {'photo' : open('static/images/' + msg,"rb")})
    except:
        url = URL + 'sendPhoto'
        requests.post(url, {'chat_id': '224133650', }, files = {'photo' : open('default.png',"rb")})

# check for mistakes if ok add category
def add_category(msg):
    if msg.strip() == '' or len(msg) < 2 or len(msg) > 20 or msg.isalpha() != True:
        send_msg('This name is not valid!')
    else:                 
        result = DB.add_category(msg.lower())
        send_msg(result)

# check for mistakes if ok edit category
def edit_category(msg):
    try:
        msg = msg.split(',')
        msg[1] = msg[1].lower().strip()
    except:
        send_msg('Invalid input, Please check!')
        return 1


    if msg[0].isdigit() != True or msg[1].isalpha() != True or len(msg[1]) < 2 or len(msg[1]) > 20:
        print(msg[0].isdigit())
        print(msg[1].isalpha())
        print(len(msg[1]) < 2)
        print(len(msg[1]) > 20)
        send_msg('Invalid input, Please check!')
    else:
        result = DB.edit_categ(msg)
        send_msg(result)

# information about user
def user_info(msg):
    result = DB.info_user(msg)
    send_msg(result)
    send_photo(msg + '.png')

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def parsing(updates):
    updates = json.loads(updates)
    global last_msg

    if 'entities' in updates['result'][-1]['message']:
        last_msg = updates['result'][-1]['message']['text']

        if updates['result'][-1]['message']['text'] == '/list':
            # selecting the list of all users
            users = DB.select_all_users()
            send_msg(users)

        elif updates['result'][-1]['message']['text'] == '/add':
            send_msg('Enter category name')

        elif updates['result'][-1]['message']['text'] == '/edit':
            category = DB.select_category()
            send_msg(category)
            send_msg('Send № and new name of category \nEx:  1, nature')        

        elif updates['result'][-1]['message']['text'] == '/info':
            send_msg("Enter username of person")
        
    else:      
        if last_msg == '/add':            
            last_msg = updates['result'][-1]['message']['text']
            # check for mistakes if ok add category
            add_category(last_msg)

        elif last_msg == '/edit':
            last_msg = updates['result'][-1]['message']['text']
            # check for mistakes if ok edit category
            edit_category(last_msg)

        elif last_msg == '/info':
            last_msg = updates['result'][-1]['message']['text']
            # check for mistakes if ok edit category
            user_info(last_msg)

        else:
            last_msg = updates['result'][-1]['message']['text']
            send_msg('Choose command, Bro')




def main():
    last_update_id = None  

    while True:
        updates = get_updates(last_update_id)
        if len(json.loads(updates)['result']) > 0:
           last_update_id = json.loads(updates)['result'][-1]['update_id'] + 1
           parsing(updates)


if __name__ == '__main__':
    main()

