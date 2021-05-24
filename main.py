#Covid-19 Vaccine tracker telegram bot

import requests
from datetime import datetime


cowin_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict'

now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
odisha_districts_ids = [445,448,447,472,454,468,457,473,458,467,449,459,460,474,464,450,461,455,446,451,469,456,470,462,465,463,471,452,466,453]

api_url_telegram = "https://api.telegram.org/bot<your_bot_id>/sendMessage?chat_id=@__groupid__&text="
group_id = '<your_public_grp_link>'



# fetching data district wise
def fetch_data(district_id):
    query_pms = "?district_id={}&date={}".format(district_id,today_date)
    final_url = cowin_url+query_pms
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(final_url, headers=headers)
    # print(response.text)
    extract_data(response)


# fetching data for each district in Odisha state
def fetch_data_for_state(district_ids):
    for district_id in district_ids:
        fetch_data(district_id)


def extract_data(response):
    data = response.json()
    for center in data["centers"]:
        # print(center["center_id"], center['name'])
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["min_age_limit"] == 45:
                message = "Pincode: {}, Name: {},Slots: {}, Minimum Age: {}".format(
                    center["pincode"], center["name"],
                    session["available_capacity_dose1"], session["min_age_limit"]
                )
                send_message(message)



def send_message(message):
    final_tel_url = api_url_telegram.replace("__groupid__", group_id)
    final_tel_url = final_tel_url + message
    response = requests.get(final_tel_url)
    print(response)




if __name__ == '__main__' :
    fetch_data_for_state(odisha_districts_ids)
