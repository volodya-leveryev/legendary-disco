""" Генерация HTML-страниц для аутентификации """
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, Flask, abort, redirect, render_template, request, session, url_for

from jimmy.models import Person

oauth = OAuth()
bp = Blueprint('auth', __name__)


def init(app: Flask) -> None:
    """ Инициализация библиотеки для OAuth """
    oauth.init_app(app)

    azure_tenat_id = app.config.get('AZURE_TENANT_ID')
    openid_path = '.well-known/openid-configuration'
    scope = {'scope': 'openid email'}
    urls = {
        'azure': f'https://login.microsoftonline.com/{azure_tenat_id}/v2.0/{openid_path}',
        'google': f'https://accounts.google.com/{openid_path}',
    }

    for provider in ('azure', 'google'):
        oauth.register(provider, server_metadata_url=urls[provider], client_kwargs=scope)


def init_session(user_email):
    """ Начало сеанса работы пользователя после успешной аутентификации """
    user = Person.objects(emails=user_email)
    if not user:
        abort(401)
    session['sem'] = 2021 * 2
    session['user'] = {
        'id': str(user[0].id),
        'str': str(user[0]),
    }


@bp.route('/login/')
def login_page():
    """ Страница аутентификации """
    return render_template('login.html')


@bp.route('/azure/init/')
def azure_init():
    """ Перенаправление на страницу аутентификации MS Azure """
    scheme = request.headers.get('X-Forwarded-Proto')
    redirect_uri = url_for('auth.azure_done', _external=True, _scheme=scheme)
    return oauth.azure.authorize_redirect(redirect_uri)


@bp.route('/azure/done/')
def azure_done():
    """ Успешная аутентификация через MS Azure """
    token = oauth.azure.authorize_access_token()
    userinfo = oauth.azure.parse_id_token(token)
    init_session(userinfo.get('email'))
    return redirect(url_for('home'))


@bp.route('/google/init/')
def google_init():
    """ Перенаправление на страницу аутентификации Google """
    scheme = request.headers.get('X-Forwarded-Proto')
    redirect_uri = url_for('auth.google_done', _external=True, _scheme=scheme)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route('/google/done/')
def google_done():
    """ Успешная аутентификация через Google """
    token = oauth.google.authorize_access_token()
    userinfo = oauth.google.parse_id_token(token)
    init_session(userinfo.get('email'))
    return redirect(url_for('home'))


@bp.route('/logout/')
def logout():
    """ Завершение сеанса работы пользователя """
    session.clear()
    return redirect(url_for('auth.login_page'))
