import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback, State, ctx, dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import feffery_antd_components as fac
from components import dmc_select, dmc_numberselect, card_style
from features import loan_purpose, branch, duration_type, obespechenie, istochnik_sredstv, loan_type, loan_purpose, education, marital_status, byro, district



def main_page():
    return html.Div([
        dmc.Space(h=20),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    card_style(
                        dbc.Row([
                            dmc.Grid([

                                dmc.Col(
                                    html.H4('Кредитные данные'), span=8),
                                    dmc.Col(dmc.Button(
                                    "Отчистить", id="button_clear", color="red"),span=2),
                                dmc.Col(dmc.Button(
                                    "Рассчитать", id="button_run"), span=2),
                            ]),

                            dbc.Row([
                                dbc.Col(dmc_numberselect(
                                    'Сумма*', step=100, max_number=35000000, id="amount_sum", precision=0)),
                                dbc.Col(dmc_numberselect(
                                    'Срок*', max_number=60, id="duration", step=1, precision=0)),
                            ]),
                            dbc.Row([
                                dbc.Col(dmc_numberselect(
                                    'Процентная ставка*', max_number=35, id="int_rate")),
                                dbc.Col(dmc_numberselect(
                                    'Оценка Обеспечения*', max_number=220000000, id="otsenka_obespecheniya_income", step=1, precision=0)),
                            ]),
                            dbc.Row([
                                dbc.Col(dmc_select(
                                    branch(), "Филиал/Пункт*", id="branch_x")),
                                dbc.Col(dmc_select(duration_type(),
                                                   "Тип срока*", id="duration_type"))
                            ]),
                            dbc.Row([
                                dbc.Col(dmc_select(obespechenie(),
                                                   "Обеспечение*", id="obespechenie")),
                                dbc.Col(dmc_select(
                                    istochnik_sredstv(), "Источник Средств*", id="istochnik_sredstv"))
                            ]),
                            dbc.Row([
                                dbc.Col(dmc_select(
                                    loan_type(), "Вид Кредитования*", id="loan_type")),
                                dbc.Col(dmc_select(
                                    loan_purpose(), "Цель Кредитования*", id="loan_purpose"))
                            ]),

                            dbc.Row([
                                dbc.Col(dmc_select(
                                    byro(), "Скоринговый балл кредитного бюро (A-J)", id="byro")),
                                dbc.Col(dmc_select(
                                    district(), "Район", id="district"))
                            ]),
                        ]),
                    ),
                    dmc.Space(h=20),
                    card_style(dbc.Row([
                        html.Div([
                            html.H4('Данные клиента'),
                            dbc.Row([
                                dbc.Col(dmc_numberselect(
                                    'Возраст', max_number=79, id="age")),
                                dbc.Col(dmc_select(education(),
                                                   "Образование", id="education")),
                            ]),
                            dbc.Row([
                                dbc.Col(dmc_select(
                                    ["Mужчина", "Женщина"], "Пол", id="gender")),
                                dbc.Col(dmc_select(
                                    district(), "Район", id="district")),
                            ]),
                            dbc.Row([
                                dbc.Col(dmc_numberselect(
                                    "Количество кредитных историй", max_number=100)),
                                # dbc.Col(dmc_select(district(), "Район")),
                                dbc.Col(dmc_numberselect(
                                    "Иждивенцы", max_number=100)),
                            ]),
                        ])
                    ])),
                    dmc.Space(h=20),
                    dbc.Row([
                        card_style(
                            html.Div([
                                html.H4('Обеспечение клиента'),
                                dbc.Row([
                                    dbc.Col(dmc_select(
                                        ["Работающий(ая)", "Безработный(ая)", "Другое"], "Текущее рабочее положение")),
                                    dbc.Col(dmc_select(["Государственное учреждение", "Частная компания", "Общественная организация",
                                                        "Индивидуальный предприниматель", "Другое", "Отсутствует"], "Место работы")),
                                ]),
                                dbc.Row([
                                    dbc.Col(dmc_numberselect(
                                        "Стаж работы (в годах) на посл. работе", max_number=70)),
                                    dbc.Col(dmc_numberselect(
                                        "Ежемесячный доход", max_number=1000000000)),
                                ]),
                                dbc.Row([
                                    dbc.Col(dmc_select(
                                        ["Аренда", "Собственность", "Кредит", "Другое", "Отсутствует"], "Наличие автомобиля")),
                                    # dbc.Col(dmc_select(district(), "Район")),
                                    dbc.Col(dmc_select(["iOS", "Android", "Другое", "Отсутствует"],
                                                       "Наличие и операционная система мобильного телефона")),
                                ]),
                                dbc.Row([
                                    dbc.Col(dmc_numberselect(
                                        "Год производства автомобиля (если имеется)", max_number=2023)),
                                    dbc.Col(dmc_select(
                                        ["Аренда", "Собственность", "Кредит", "Другое", "Отсутствует"], "Наличие жилья")),
                                ]),
                            ])
                        ),
                    ])

                ], md=8),

                dbc.Col([
                    dbc.Row([
                        card_style(
                            html.Div([
                                html.H4('Результат'),
                                dcc.Loading(html.Div(id="result"))
                            ]),
                        ),
                    ]),
                    dbc.Row([
                        dmc.Space(h=30),
                        html.Div(id="shap_value")
                    ]),
                    dmc.Space(h=50),
                    dbc.Row([
                        card_style(
                            fac.AntdSlider(
                                tooltipVisible=True, min=0.1, max=1, step=0.01, value=0.15, id='treshold'),
                        ),
                    ])
                ]),
            ]),
            dcc.Store(id="prediction_store", storage_type="session"),
            html.Div(id='message_container_demo')
        ], fluid=True)
    ])
