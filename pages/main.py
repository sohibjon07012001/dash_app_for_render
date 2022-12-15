import time
import dash
import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback, State, ctx, dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import pickle
from catboost import CatBoostClassifier
import feffery_antd_components as fac
from components import dmc_select, dmc_numberselect, card_style
from features import loan_purpose, branch, duration_type, obespechenie, istochnik_sredstv, loan_type, loan_purpose, education, marital_status, byro, district
from def_main  import shap_value, result_model
from layouts.main_page_layout import main_page
from flask_login import current_user
import feffery_antd_components as fac
dash.register_page(__name__)



# Проверка на авторизованного пользователя
def layout():
    if not current_user.is_authenticated:
        return dcc.Location(href="/", refresh=True, id='1')  # login
    else:
        return main_page()



@callback(
    Output('amount_sum', 'value'),
    Output('duration', 'value'),
    Output('int_rate', 'value'),
    Output('otsenka_obespecheniya_income', 'value'),
    Output('branch_x', 'value'),
    Output('duration_type', 'value'),
    Output('obespechenie', "value"),
    Output("istochnik_sredstv", "value"),
    Output("loan_type", "value"),
    Output("loan_purpose", "value"),
    Input('button_clear', 'n_clicks')
)
def clear_values(n):
    if ctx.triggered_id == "button_clear":
        print(n)
        return 0, 0, 0, 0, None, None, None, None, None, None 
    else:
        raise dash.exceptions.PreventUpdate


@callback(
    Output('result', 'children'),
    Output("shap_value", "children"),
    Output('prediction_store', 'data'),
    Output("message_container_demo", "children"),
    Output("button_run", "children"),
    Input('button_run', 'n_clicks'),
    State('amount_sum', 'value'),
    State('duration', 'value'),
    State('int_rate', 'value'),
    State('otsenka_obespecheniya_income', 'value'),
    State('branch_x', 'value'),
    State('duration_type', 'value'),
    State('obespechenie', "value"),
    State("istochnik_sredstv", "value"),
    State("loan_type", "value"),
    State("loan_purpose", "value"),
    Input("treshold", "value"),
    Input('prediction_store', 'data'),
    prevent_initial_call=True,
)
def predict_model_catboost(n, amount_sum, duration, int_rate, otsenka_obespecheniya_income, branch_x, duration_type, obespechenie, istochnik_sredstv, loan_type, loan_purpose, treshold, storage_data_prediction):
    if otsenka_obespecheniya_income == None or branch_x == None or duration_type == None or obespechenie == None  or istochnik_sredstv == None  or loan_type == None or loan_purpose == None:
        return dash.no_update, dash.no_update, dash.no_update, fac.AntdMessage(
                                                            content='Не заполнены кредитные данные',
                                                            type="error"
                                                        ), dash.no_update
    
    try:
        if ctx.triggered_id == "button_run":
            data = [{"amount_sum": int(amount_sum), "duration": int(duration), "int_rate": float(int_rate), "otsenka_obespecheniya_income": int(otsenka_obespecheniya_income), "branch": branch_x,
                    "duration_type": duration_type, "obespechenie": obespechenie, "istochnik_sredstv": istochnik_sredstv, "loan_type": loan_type, "loan_purpose": loan_purpose}]
            clientData = pd.DataFrame(data=data)
            clientDataEncoded = pd.get_dummies(clientData)
            model_columns = pickle.load(
                open("model_columns.pkl", "rb")
            )
            clientDataEncoded = clientDataEncoded.reindex(
                columns=model_columns,
                fill_value=0
            )
            cat = CatBoostClassifier()
            model = cat.load_model("CatBoostModel06122022.cbm")
            prediction = model.predict_proba(clientDataEncoded)

            return result_model(prediction, treshold), shap_value(clientDataEncoded, cat) , prediction, dash.no_update, dash.no_update,
        elif treshold is not None and storage_data_prediction is not None:
            return result_model(storage_data_prediction, treshold), dash.no_update, dash.no_update, dash.no_update, dash.no_update,
        else:
            return "Заполните все поля и нажмите РАССЧИТАТЬ для получения результата.", dash.no_update, dash.no_update, dash.no_update, dash.no_update,
    except Exception as message:
        return dash.no_update, dash.no_update, dash.no_update, fac.AntdMessage(
                                                            content=str(message),
                                                            type="error"
                                                        ), dash.no_update