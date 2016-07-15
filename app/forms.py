from wtforms import Form, BooleanField, StringField, PasswordField, validators

#-------------------------------------------------------------------------------
#this for forms in Flask
#to render fields please check this link, it is very interresting:
# http://flask.pocoo.org/docs/0.11/patterns/wtforms/
#it will propose you a way to simply render fields in templates using jinja2
#-------------------------------------------------------------------------------

class loginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.DataRequired(),])
