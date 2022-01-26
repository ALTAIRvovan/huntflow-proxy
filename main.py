import logging
import requests

from typing import List
from fastapi import FastAPI, Form
from pydantic import Field, BaseModel, BaseSettings

logger = logging.getLogger("mil-jobs")


class Settings(BaseSettings):
    account_id: int
    huntflow_token: str

settings = Settings()
app = FastAPI()

# CONSTS
APPLICANTS_URL = "https://api.huntflow.ru/account/{}/applicants".format(settings.account_id)
AUTHORIZATION_HEADER = "Bearer {}".format(settings.huntflow_token)


#! uncomment to setup webhooks
# @app.post("/vacancy")
# def test_form(test: str = Form(...)):
#     if test == "test":
#         return "ok"
#     return "error"


#! Main handler
@app.post("/vacancy")
def parse_form(
        Email: str = Form(...),
        Name: str = Form(...),
        position: str = Form(default='intern'),
        cv: str = Form(...),
        portfolio: str = Form(default=''),
        level: str = Form(default=''),
        area: List[str] = Form(default=''),
        topic: List[str] = Form(default='')
    ):
    extra_data = """
    Дополнительная информация:
    Уровень: {}
    Область: {}
    Тема: {}
    Резюме с тильды: {}
    Портфолио: {}
    """.format(level, area, topic, cv, portfolio)

    result = requests.post(APPLICANTS_URL, json={
        "last_name": Name,
        "first_name": "*",
        "email": Email,
        "position": position,
        "externals": [{
            "data": {
                "body": extra_data
            },
            "auth_type": "NATIVE",
        }, ],
    }, headers={
        "Authorization": AUTHORIZATION_HEADER,
    })
    logger.info("Response: %s", result)
    try:
        result_json = result.json()
        logger.info("Response json: %s", result_json)
        return "ok" if "id" in result_json else "error"
    except:
        return "error"
