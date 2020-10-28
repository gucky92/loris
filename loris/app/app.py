"""
"""

from flask import Flask, session, request, redirect
from flask_login import LoginManager
# from dash import Dash
# import dash_html_components as html

from loris import config
from loris.app.login import User
from loris.app.pymysql_flask import MySQL


class LorisApp(Flask):

    def session_refresh(self):
        config.refresh()
        # for testing when refresh happens
        self.config['schemata'] = list(config['schemata'].keys())
        self.config['tables'], self.config['autotables'] = \
            config.tables_to_list()


app = LorisApp(__name__)
app.secret_key = config['secret_key']
app.config['include_fly'] = config['include_fly']
app.config['external_wiki'] = config['external_wiki']

mysql = MySQL(app)
login_manager = LoginManager(app)

# Test of dash app
# TODO
# dash_app = Dash(__name__, server=app, url_base_pathname='/dashapp/')
# dash_app.layout = html.Div(
#     children=[html.H1(children='Dash App')]
# )


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?target=' + request.path)


from loris.app import views, errors
