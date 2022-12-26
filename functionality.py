from hashlib import sha256
from werkzeug.utils import secure_filename
from filters import *
import os

absolute_path = os.path.dirname(__file__)
relative_path = "static\images"
full_path = os.path.join(absolute_path, relative_path)

# converting image into BLOB format and returning blob 
def convert(filename):
    with open(filename, "rb") as file:
        blobData = file.read()

    return blobData


# hashing the password 
def hash_pass(val):
    h = sha256()
    h.update(val.encode('utf8'))
    return h.hexdigest()

# protecting the system from entering whitespaces
def checkME(fname, lname, uname):
    fname = fname.strip()
    lname = lname.strip()
    uname = uname.strip()

    if fname == "" or lname == "" or uname == "":
        return False
    else:
        return True

# checking for uploaded image, if empty insert default user image
def upload_user_photo(photo, filters, uname):
    filename = secure_filename(photo.filename)  
    if filename == '':     
        
        return 'default.png'
    else:
        for i in range(10):            
            print(full_path)
        photo.save(full_path + '\{}.png'.format(uname))
        if filters != "none":
            if filters == "Blur":
                blur(uname)
            elif filters == "Solarized":
                solarize(uname)
            elif filters == "Black":
                gray(uname)
        else:
            image = '{}.png'.format(uname)         
            return image