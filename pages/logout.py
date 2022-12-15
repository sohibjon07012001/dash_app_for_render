import dash
from dash import html, dcc
from pages.login import layout as login

dash.register_page(__name__)




# Проверка на авторизованного пользователя 
def layout():
        return dcc.Location(href="/", refresh=True, id='lsdgf')


