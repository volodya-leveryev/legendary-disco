from authlib.integrations.flask_client import OAuth
from flask import Blueprint, abort, redirect, render_template, request, session, url_for

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


def init_session(user_email):
    user = Person.objects(emails=user_email)
    if not user:
        abort(401)
    session['user'] = {
        'id': str(user[0].id),
        'str': str(user[0]),
    }
    session['sem'] = 2021 * 2


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
    init_session(userinfo.get('email'))
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
    init_session(userinfo.get('email'))
    return redirect(url_for('home'))


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('auth.login_page'))
