"""Parser module"""
import os
import time

from dotenv import load_dotenv
import requests

from send_email import send_message

load_dotenv()

URL_METTINGS = "https://applicant.21-school.ru/api/v3/meetings/piscine"
URL_LOGIN = "https://applicant.21-school.ru/api/v3/signin"
URL_JOIN_MEETING = "https://applicant.21-school.ru/api/v3/meetings_users"
URL_MY_MEETING = "https://applicant.21-school.ru/api/v3/meetings_users/piscine"

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def parser():
    """School21 meetings parser"""
    bearer = login_user()
    while True:
        time.sleep(60)
        mettings = requests.get(
            URL_METTINGS,
            headers={"Authorization": bearer},
            timeout=3
        )
        try:
            dates = mettings.json()["meetings"]
            if dates != []:
                meeting_id = dates[0]["id"]
                date_time = dates[0]["date"]
                address = dates[0]["address"]
                join_body = {
                    "meetings_user": {
                        "meeting_id": meeting_id
                    }
                }
                requests.post(
                    URL_JOIN_MEETING,
                    json=join_body,
                    headers={"Authorization": bearer},
                    timeout=3
                )
                my_metting = requests.get(
                    URL_MY_MEETING,
                    headers={"Authorization": bearer},
                    timeout=3
                )
                webinar_url = my_metting.json()["meetings_user"]["webinar_url"]
                message = f"You are subscribed to School21 webinar {date_time} {address}. Webinar link {webinar_url}"
                return send_message(message, "anastasia.borovik.1998@mail.ru")
            else:
                print("No meetings available.")
                continue
        except KeyError:
            bearer = login_user()
            continue


def login_user() -> str:
    """School21 meetings login"""
    login_body = {
        "api_user": {
            "email": EMAIL,
            "password": PASSWORD
        }
    }
    login = requests.post(URL_LOGIN, json=login_body, timeout=3)
    if login.status_code == 200:
        return login.json()["Authorization"]
    print(f"Login failed. Status code {login.status_code}.")
    return os.getenv("BEARER")


print(parser())
