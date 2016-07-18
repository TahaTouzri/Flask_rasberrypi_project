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

class settingsForm(Form):
    new_login_enable_sms              = BooleanField('new_login_enable_email',default=False)
    new_login_enable_email            = BooleanField('new_login_enable_email', default=False)
    temperature_exceed_enable_sms     = BooleanField('temperature_exceed_enable_sms',default = False)
    temperature_exceed_enable_email   = BooleanField('temperature_exceed_enable_email',default=False)
    temperature_decrease_enable_sms   = BooleanField('temperature_decrease_enable_sms',default=False)
    temperature_decrease_enable_email = BooleanField('temperature_decrease_enable_email',default=False)
    door_opened_enable_sms            = BooleanField('door_opened_enable_sms',default=False)
    door_opened_enable_email          = BooleanField('door_opened_enable_email',default=False)
    window_opened_enable_sms          = BooleanField('window_opened_enable_sms',default=False)
    window_opened_enable_email        = BooleanField('window_opened_enable_email',default=False)
