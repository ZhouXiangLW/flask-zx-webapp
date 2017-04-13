from flask import Blueprint
from . import forms
main = Blueprint('main', __name__)
LoginForm = forms.LoginForm
RegisterForm = forms.RegisterForm
from . import views, errors