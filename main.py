import requests

from typing import List
from fastapi import FastAPI, Form
from pydantic import Field, BaseModel

app = FastAPI()


# @app.post("/vacancy")
# def test_form(test: str = Form(...)):
#     if test == "test":
#         return "ok"
#     return "error"


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

    result = requests.post("https://api.huntflow.ru/account/109916/applicants", json={
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
        "Authorization": "Bearer <token>",
    })
    print(result)
    print(result.json())
    try:
        result_json = result.json()
        return "ok" if "id" in result_json else "error"
    except:
        return "error"
