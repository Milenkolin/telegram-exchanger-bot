from bs4 import BeautifulSoup
import requests
import json



def get_table_Oschadbank():
    url = 'https://www.oschadbank.ua/ua/private/currency'
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", class_="table-responsive")
    table = div.find("table", class_=['table', 'table-striped', 'table-hover', 'table-primary'])
    return table


def get_table_Privatbank():
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    html = json.loads(requests.get(url).text)
    return html


def get_table_National():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    html = json.loads(requests.get(url).text)
    return html


# def get_table_Monobank():
#     url = "https://api.monobank.ua/bank/currency"
#     html = json.loads(requests.get(url).text)
#     return html

class OschadBank:



    def get_code(self):
        code_list = []
        table = get_table_Oschadbank()
        td_s = table.find_all('td', class_='')

        for td in td_s:
            code_list.append(td.get_text())
        return code_list

    def buy_currency(self):
        value_list = []
        table = get_table_Oschadbank()
        td_s = table.select('td.text-right:nth-child(6)')

        for td in td_s:
            value_list.append(float(td.get_text()))
        return value_list

    def sell_currency(self):
        value_list = []
        table = get_table_Oschadbank()
        td_s = table.select('td.text-right:nth-child(7)')

        for td in td_s:
            value_list.append(float(td.get_text()))
        return value_list

    def get_data(self, f1, f2, f3):

        data_list = list(zip(f1, f2, f3))
        return data_list

    def pretify_data(self, f1, code):
        for i in f1:
            for data in i:
                if data == code:
                    flag = ""
                    euflag = "πͺπΊ"
                    usflag = "πΊπΈ"
                    ruflag = "π·πΊ"

                    if data == "USD":
                        flag = usflag

                    elif data == "EUR":
                        flag = euflag

                    elif data == "RUB":
                        flag = ruflag
                        result1 = f"{i[0]}{flag} -> UAHπΊπ¦"
                        result2 = f"\nΠΡΠΏΡΠ²Π»Ρ: {float((i[1]) / 10)}\nΠΡΠΎΠ΄Π°ΠΆ: {float((i[2]) / 10)}"
                        result3 = result1 + "\n" + result2
                        return result3

                    result1 = f"{i[0]}{flag} -> UAHπΊπ¦"
                    result2 = f"\nΠΡΠΏΡΠ²Π»Ρ: {float(i[1])}\nΠΡΠΎΠ΄Π°ΠΆ: {float(i[2])}"
                    result3 = result1 + "\n" + result2
                    return result3


class PrivatBank:

    def get_data(self, ccy_key):
        for data in get_table_Privatbank():
            if ccy_key == data['ccy']:
                return data
        return False

    def pretify_data(self, f1):
        flag = ""
        euflag = "πͺπΊ"
        usflag = "πΊπΈ"
        ruflag = "π·πΊ"
        btcflag = "π°"
        for data in f1.values():
            if data == "EUR":
                flag = euflag
            elif data == "USD":
                flag = usflag
            elif data == "RUR":
                flag = ruflag
            elif data == "BTC":
                flag = btcflag
                values = list(f1.values())
                result1 = f"{values[0]}{flag} -> {values[1]}πΊπΈ"
                result2 = f"\nΠΡΠΏΡΠ²Π»Ρ: {float(values[2])}\nΠΡΠΎΠ΄Π°ΠΆ: {float(values[3])}"
                result3 = result1 + "\n" + result2
                return result3

        values = list(f1.values())
        result1 = f"{values[0]}{flag} -> {values[1]}πΊπ¦"
        result2 = f"\nΠΡΠΏΡΠ²Π»Ρ: {float(values[2])}\nΠΡΠΎΠ΄Π°ΠΆ: {float(values[3])}"
        result3 = result1 + "\n" + result2
        return result3


# class MonoBank:
#     def get_data(self,cca):
#         try:
#             for data in get_table_Monobank():
#                 if int(cca) == data["currencyCodeA"]:
#                     return data
#             return False
#         except AttributeError:
#             error_phrase = "ΠΠ°Π½Π°Π΄ΡΠΎ Π±Π°Π³Π°ΡΠΎ Π·Π°ΠΏΠΈΡΡΠ² Π΄ΠΎ ΡΠ°ΠΉΡΡ ΠΠΎΠ½ΠΎΠ±Π°Π½ΠΊ. Π‘ΠΏΡΠΎΠ±ΡΠΉΡΠ΅ ΡΠ΅ΡΠ΅Π· ΡΠ²ΠΈΠ»ΠΈΠ½Ρ."
#             return error_phrase
#
#     def pretify_data(self, f1):
#         flag = ""
#         country = ""
#         euflag = "πͺπΊ"
#         usflag = "πΊπΈ"
#         ruflag = "π·πΊ"
#         for data in f1.values():
#             if data == 978:
#                 country = "EUR"
#                 flag = euflag
#             elif data == 840:
#                 country = "USD"
#                 flag = usflag
#             elif data == 643:
#                 country = "RUB"
#                 flag = ruflag
#
#         values = list(f1.values())
#         result1 = f"{country}{flag} -> UAHπΊπ¦"
#         result2 = f"\nΠΡΠΏΠΈΡΠΈ: {float(values[3])}\nΠΡΠΎΠ΄Π°ΡΠΈ: {float(values[4])}"
#         result3 = result1 + "\n" + result2
#         return result3


class NationalBankOfUkraine:

    def get_data(self, cc):
        for data in get_table_National():
            if cc == data['cc']:
                return cc, data['rate']
        return False


    def pretify_data(self, data):
        country_dict = {'AUD': "π¦πΊ", "CAD": "π¨π¦", "CNY": "π¨π³", "HRK": "π­π·", "CZK": "π¨πΏ", "DKK": "π©π°",
                        "HKD": "π­π°",
                        "HUF": "π­πΊ", "INR": "π?π³", "IDR": "π?π©", "ILS": "π?π±", "JPY": "π―π΅", "KZT": "π°πΏ",
                        "KRW": "π°π·", "MXN": "π²π½",
                        "MDL": "π²π©", "NZD": "π³πΏ", "NOK": "π³π΄", "RUB": "π·πΊ", "SAR": "πΈπ¦", "SGD": "πΈπ¬",
                        "ZAR": "πΏπ¦", "SEK": "πΈπͺ",
                        "CHF": "π¨π­", "EGP": "πͺπ¬", "GBP": "π¬π§", "USD": "πΊπΈ", "BYN": "π§πΎ", "RON": "π·π΄",
                        "TRY": "πΉπ·", "BGN": "π§π¬",
                        "EUR": "πͺπΊ", "PLN": "π΅π±", "DZD": "π©πΏ", "BDT": "π§π©", "AMD": "π¦π²", "IRR": "π?π·",
                        "IQD": "π?πΆ", "KGS": "π°π¬", "LBP": "π±π§", "LYD": "π±πΎ", "MYR": "π²πΎ", "MAD": "π²π¦",
                        "PKR": "π΅π°", "VND": "π»π³",
                        "THB": "πΉπ­", "AED": "π¦πͺ", "TND": "πΉπ³", "UZS": "πΊπΏ", "TMT": "πΉπ²", "RSD": "π·πΈ",
                        "AZN": "π¦πΏ", "TJS": "πΉπ―", "GEL": "π¬πͺ", "BRL": "π§π·"}

        for i in country_dict.keys():
            if i == data[0]:
                result1 = f"{i}{country_dict[i]} -> UAHπΊπ¦"
                result2 = f"\nΠΡΡΡΡΠΉΠ½ΠΈΠΉ ΠΊΡΡΡ: {data[1]}"
                result = result1 + "\n" + result2
                return result


