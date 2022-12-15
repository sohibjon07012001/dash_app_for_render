import dash_mantine_components as dmc
from dash_iconify import DashIconify
from features import loan_purpose
import dash_bootstrap_components as dbc


def dmc_select(data, feature=" ", description=None, id=""):
    return dmc.Select(
        data=data,
        value="USDJPY",
        label=feature,
        id=id,
        # required=True,
        # style={"width": 200},
        searchable=True,
        nothingFound="No options found",
        description=description,
        # icon=[DashIconify(icon="radix-icons:magnifying-glass")],
        # rightSection=[DashIconify(icon="radix-icons:chevron-down")],
    )


def dmc_numberselect(label, description=None, step=0.1, min_nubmber=0, max_number=1000000000, id="", precision=1):

    return dmc.NumberInput(
        label=label,
        description=description,
        precision=precision,
        id=id,
        min=min_nubmber,
        max=max_number,
        step=step

        # icon=[DashIconify(icon="fa6-solid:weight-scale")],
        # style={"width": 250},
    )


def card_style(content):
    return dbc.CardGroup([
        dbc.Card([
            dbc.CardBody([
                content
            ])
        ], color="#f2f2fa", style={'border-radius': '10px'})
    ])
