from flask import session, redirect, url_for, render_template, request, Blueprint

unyang4cut = Blueprint('photo', __name__, url_prefix='/photo')

@unyang4cut.route('/', methods = ['GET', 'POST'])
def lobby():
    return 'Hello'