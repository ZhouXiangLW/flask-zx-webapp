from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, RadioField
from wtforms.validators import Required, Length, Email

class LoginForm(Form):
    email = StringField('邮电子箱:',validators=[Required(), Length(1, 64), Email()])
    passwd = PasswordField('密码:',validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')

class RegisterForm(Form):
    name = StringField('姓名:', validators=[Required()])
    email = StringField('邮电子箱:',validators=[Required(), Length(1, 64), Email()])
    passwd = PasswordField('密码:',validators=[Required()])
    remember_me = BooleanField('登录并记住我')
    submit = SubmitField('注册')


