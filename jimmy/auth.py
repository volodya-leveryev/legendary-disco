from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, render_template, request, session, url_for

from jimmy.models import Person

oauth = OAuth()
bp = Blueprint('auth', __name__)


def init(app):
    oauth.init_app(app)

    azure_url = 'https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0/.well-known/openid-configuration'
    azure_url = azure_url.format(**app.config)
    oauth.register('azure', server_metadata_url=azure_url, client_kwargs={'scope': 'openid email'})

    google_url = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register('google', server_metadata_url=google_url, client_kwargs={'scope': 'openid email'})


@bp.route('/login/')
def login_page():
    return render_template('login.html')


@bp.route('/azure/init/')
def azure_init():
    scheme = request.headers.get('X-Forwarded-Proto')
    redirect_uri = url_for('auth.azure_done', _external=True, _scheme=scheme)
    return oauth.azure.authorize_redirect(redirect_uri)


@bp.route('/azure/done/')
def azure_done():
    token = oauth.azure.authorize_access_token()
    userinfo = oauth.azure.parse_id_token(token)
    persons = Person.objects(emails=userinfo.get('email'))
    if not persons:
        return redirect(url_for('auth.login_page'))
    session['user'] = {
        'id': str(persons[0].id),
        'str': str(persons[0]),
    }
    return redirect(url_for('home'))


@bp.route('/google/init/')
def google_init():
    scheme = request.headers.get('X-Forwarded-Proto')
    redirect_uri = url_for('auth.google_done', _external=True, _scheme=scheme)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route('/google/done/')
def google_done():
    token = oauth.google.authorize_access_token()
    userinfo = oauth.google.parse_id_token(token)
    persons = Person.objects(emails=userinfo.get('email'))
    if not persons:
        return redirect(url_for('auth.login_page'))
    session['user'] = {
        'id': str(persons[0].id),
        'str': str(persons[0]),
    }
    return redirect(url_for('home'))


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('auth.login_page'))
