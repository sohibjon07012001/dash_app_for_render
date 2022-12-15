import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt
from catboost import CatBoostClassifier
from dash import html, get_app
from dash_svg import Svg, G, Path, Circle
import base64
import feffery_antd_components as fac
from components import card_style


def shap_value(clientDataEncoded, cat):
    # clientDataEncoded = pd.get_dummies(clientData)
    # model_columns = pickle.load(
    #     open("model_columns.pkl", "rb")
    # )
    # clientDataEncoded = clientDataEncoded.reindex(
    #     columns=model_columns,
    #     fill_value=0
    # )
    shap.initjs()
    # cat = CatBoostClassifier()
    # model = cat.load_model("CatBoostModel06122022.cbm")
    explainer = shap.TreeExplainer(cat)
    shap_values = explainer.shap_values(clientDataEncoded)
    # len(shap_values[0])
    # matplotlib=True, show = False
    force = shap.force_plot(explainer.expected_value,
                            shap_values, clientDataEncoded)
    # p = shap.force_plot(explainerModel.expected_value, shap_values_Model[j], S.iloc[[j]], matplotlib = True, show = False)
    # plt.savefig('tmp.png')
    # plt.close()
    # encoded_image = base64.b64encode(open('tmp.png', 'rb').read())
    shap_html = f"<head>{shap.getjs()}</head><body>{force.html()}</body>"
    return card_style(html.Iframe(srcDoc=shap_html,
                                  style={"width": "100%", "height": "200px", "border": 0}))
    # return html.Img(src=('tmp.png'))
    # return  html.Div([
    #                     html.Img(src='base64,{}'.format(encoded_image))
    #                 ])



def result_model(prediction, treshold):
    if prediction[0][1] > treshold:
        status = "error"
        title = f"Не одобряется {round(prediction[0][0]*100, 2)}%"
    else:
        status = "success"
        title = f"Одобряется {round(prediction[0][0]*100, 2)}%"

    return fac.AntdSpace(
        [
            fac.AntdResult(
                status=status,
                title=title,
                # subTitle=f'status="{status}"'
            )
        ],
        direction='vertical',
        addSplitLine=True,
        style={
            'width': '100%'
        }
    )