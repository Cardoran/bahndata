from datetime import datetime, timedelta
import requests
import xmltodict

def get_timetable_xml(api_auth, EVA_NR, date:datetime = None) -> str:
    if date is None:
        date = datetime.now()
    date_string = date.strftime("%y%m%d")
    hour: str = date.strftime("%H")
    url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/{EVA_NR}/{date_string}/{hour}"
    # print(url)
    response = requests.get(
        f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1"
        f"/plan/{EVA_NR}/{date_string}/{hour}",
        headers=api_auth
    )
    print(response.url)

    # print("'{}'".format(response.text))
    # with open("plan.txt", "w") as text_file:
    #     text = response.text
    #     text = text.replace("><",">\n<")
    #     text_file.write(text)

    if response.status_code == 410:
        return get_timetable_xml(api_auth,EVA_NR,date+timedelta(days=1))
    elif response.status_code == 401:
        raise Exception("Code 401: Can't request timetable because the credentials are not correct. Please make sure that "
                        "you are providing the correct credentials.")
    elif response.status_code == 400:
        raise Exception("Code 400: Can't request timetable because the EVA number is not correct. Please make sure that "
                        "you are providing the correct EVA number.")
    elif response.status_code != 200:
        raise Exception("Can't request timetable! The request failed with the HTTP status code {}: {}"
                        .format(response.status_code, response.text))
    return response.text

if __name__ == "__main__":
    api_auth = {
                "DB-Api-Key": "235a6da868e721b3ed0f8915d17759fb",
                "DB-Client-Id": "2b83a09f021fad54d68cc31e3b5e03e2",
            }
    xml = get_timetable_xml(api_auth, 8080040)
    print(xml)
    datadict = xmltodict.parse(xml, attr_prefix='')["timetable"]
    print(datadict)
    print(datadict.keys())
    print(datadict["station"])
    for s in datadict["s"]:
        print(s)