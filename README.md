# FORUM SITE
### Video Demo:   [FORUM SITE YOUTUBE LINK](https://youtu.be/DLR-RHQQx08)
<br/>

### Description:
A website where you can ask questions, comment, like and explore different categories. Also it has an telegram bot for admin users. This project was created as an final project for CS50!
<br/>
<br/>

## Usage 
<br/>

### 1. Run the following command in your terminal:

```
git clone
```

### 2.Setup your vertual environment:
<br/>

### Download:
```
pip install virtualenv
```
or 
```
pip3 install virtualenv 
```

### Create venv:
<https://docs.python.org/3/library/venv.html>
<br/>
<br/>
### 3.Install all required modules and packages from requirements.txt file. Run following command:

```
pip install -r /path/to/requirements.txt
```

## Run
### Execute below command in working dir:
```
flask run
```
<br/>
<br/>


## What each file contains?
\
**static** - dir contains all the necessary css and image files

**templates** - dir contains all the html files of the site

**database.py** - file contains all sql commands for CRUD opetations in the site

**filters.py** - file used when uploadin user avatar and appliying some filters to photo

**forum.py** - stores all the code for this application

**functionality.py** -  file contains all the scripts and methods

**tgforum.py** - this file you should run separately if you want to use a telegram bot
username of telegram bot:
<https://t.me/manage_forum_bot>