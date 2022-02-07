# Advanced-Login-System-Tkinter
Tkinter is known for its outdated GUi. So for this project I tried to make an aesthetic gui with an advanced login system. 

This is a secure login system made with python tkinter. To run the program run 'main.py'.
If there is no database file, it will be created automatically.

### Requirements:
- Python 3

To install the other requirements run this on command line:
```
pip list --format=freeze > requirements.txt
```

Main features:
- Working login
- Working registration
- Secure hashed passwords (blake2b algorithm)
- Plaaceholder entries
- Aethetic tkinter gui
- Database storage

To browse the db file you can download this database browser: 
- [DB Browser](https://sqlitebrowser.org/)

# How it works
When in main.py create an instance of the StartApp(), this will show the aplication itself:
```python
>>> app = StartApp()
```
![Start page](Images/StartPage.png)

After having logged in as a user or guest the window will close, you can then get the following attributes.

Having logged in:
```python
>>> print(app.logged_in)
True

>>> print(app)
'Logged in as user/guest'

>>> print(app.mode)
'guest/user'
```

Closing window without login nor entering as guest:
```python
>>> print(app.logged_in)
False

>>> print(app)
'Not logged in'

>>> print(app.mode)
None
```

## Login page
The Login page has the following features:
- Validate username and password. 
- Hide and show the password.
- Reset forgotten password through email.
- Placeholder entries
- Password hidden with '*'

![LoginPage](Images/LoginPage.png)

## Registration Page
The Registration page has the following features:
- Validation of data 
- Appropiate feedback.
- Data added and stored in 'users.db' file.
- Placeholder entries

![RegistrationPage](Images/RegistrationPage.png)
