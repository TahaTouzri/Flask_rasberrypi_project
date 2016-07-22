from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_login import LoginManager,login_user,login_required,current_user,logout_user
from modules import *
from views import *

#-------------------------------------------------------------------------------
#this for forms in Flask
#to render fields please check this link, it is very interresting:
# http://flask.pocoo.org/docs/0.11/patterns/wtforms/
#it will propose you a way to simply render fields in templates using jinja2
#-------------------------------------------------------------------------------

class loginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.DataRequired(),])
    #print "----------------------------------------------"
    #print password.data

class changePasswordForm(Form):
    password = PasswordField('password1', [validators.DataRequired(),])
    repeated_password = PasswordField('password2', [validators.DataRequired(),])
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not (self.password.data==self.repeated_password.data):
            return False
        return True

class settingsForm(Form):
    new_login_enable_sms              = BooleanField('new_login_enable_sms')#,default=get_new_login_enable_sms())
    new_login_enable_email            = BooleanField('new_login_enable_email')#,default=get_new_login_enable_email())
    temperature_exceed_enable_sms     = BooleanField('temperature_exceed_enable_sms')#,default = get_temperature_decrease_enable_sms())
    temperature_exceed_enable_email   = BooleanField('temperature_exceed_enable_email')#,default=get_temperature_decrease_enable_email())
    temperature_decrease_enable_sms   = BooleanField('temperature_decrease_enable_sms')#,default=get_temperature_decrease_enable_sms())
    temperature_decrease_enable_email = BooleanField('temperature_decrease_enable_email')#,default=get_temperature_decrease_enable_email())
    door_opened_enable_sms            = BooleanField('door_opened_enable_sms')#,default=get_door_opened_enable_sms())
    door_opened_enable_email          = BooleanField('door_opened_enable_email')#,default=get_door_opened_enable_email())
    window_opened_enable_sms          = BooleanField('window_opened_enable_sms')#,default = get_window_opened_enable_sms())
    window_opened_enable_email        = BooleanField('window_opened_enable_email')#,default = get_window_opened_enable_email())
    temperature_max_val               = StringField('temperature_max_val', [validators.Length(min=1, max=2)])
    temperature_min_val               = StringField('temperature_min_val', [validators.Length(min=1, max=2)])
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    def validate(self):
        if not Form.validate(self):
            return False
        if not(self.temperature_min_val.data.isdigit() and self.temperature_max_val.data.isdigit()):
            return False
        else:
            if int(self.temperature_min_val.data)>int(self.temperature_max_val.data):
                return False
        return True
