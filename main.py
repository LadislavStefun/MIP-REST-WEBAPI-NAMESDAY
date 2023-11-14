import requests
import calendar
from datetime import datetime
import pandas as pd

'''
    Príklad použitia REST web api na získavanie údajov z internetového zdroja.
    Program využíva knižnice :
    requests - naviazanie spojenia so zdrojovou stránkou a posielanie špecifických parametrov
    padnas - vytvorenie dataframe-u a export do formátu csv
    datetime & calendar - na formátovanie dátumu
    na overenie výsledkov slúži výstupný súbor meniny.csv
'''

def translate(month):
    if month <= 0 and month >= 12:
        return -1
    formated_date = "{:02d}".format(month)
    translation = {
        "01": "Január",
        "02": "Február",
        "03": "Marec",
        "04": "Apríl",
        "05": "Máj",
        "06": "Jún",
        "07": "Júl",
        "08": "August",
        "09": "September",
        "10": "Október",
        "11": "November",
        "12": "December"
    }
    return translation[str(formated_date)]

def data_api_call(url, year, month):
    #formatovanie datumu do potrebneho formátu
    formated_date = translate(month)
    number_of_days = calendar.monthrange(year, month)[1]

    
    #vytvorenie základnej dátovej štruktúry
    data_dict = {formated_date: [], "Meno": []}
    
    #konkretizácia parametrov, vďaka ktorej bude web api stránka vedieť aké
    #informácie poslať ako odpveď
    params = {
        "date": "",
        "lang": "sk"
    }

    #pre dni v mesiaci pošli stránke get requests a vlož ich do dátovej štruktúry
    for day in range(1, number_of_days+1):
        params["date"] = "{:02d}{:02d}".format(day, month)
        response = requests.get(url, params=params)
        #ak odpoveď od servera obsahuje status kód 200 = OK 
        #spojenie prebehlo v poriadku a správne
        if response.status_code == 200:
            data = response.json()
            date_object = datetime.strptime(data[0]["date"], "%d%m")
            data_dict[formated_date].append(f"{date_object.day}")
            data_dict["Meno"].append(data[0]["name"])
        #Ak by nastala chyba vypiš ju na obrazovku
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    #1. Vytvor a 2. Exportni dataframe pozbieraných dát
    df = pd.DataFrame(data_dict)
    df.to_csv('meniny.csv', index=False, encoding="utf-8")

def main():
    #určenie konkrétnych potrebných parametrov
    url = "http://svatky.adresa.info/json"
    data_api_call(url, 2023, 9)

if __name__ == '__main__':
    #hlavný chod programu
    main()
