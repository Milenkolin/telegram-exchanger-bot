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
                    euflag = "🇪🇺"
                    usflag = "🇺🇸"
                    ruflag = "🇷🇺"

                    if data == "USD":
                        flag = usflag

                    elif data == "EUR":
                        flag = euflag

                    elif data == "RUB":
                        flag = ruflag
                        result1 = f"{i[0]}{flag} -> UAH🇺🇦"
                        result2 = f"\nКупівля: {float((i[1]) / 10)}\nПродаж: {float((i[2]) / 10)}"
                        result3 = result1 + "\n" + result2
                        return result3

                    result1 = f"{i[0]}{flag} -> UAH🇺🇦"
                    result2 = f"\nКупівля: {float(i[1])}\nПродаж: {float(i[2])}"
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
        euflag = "🇪🇺"
        usflag = "🇺🇸"
        ruflag = "🇷🇺"
        btcflag = "💰"
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
                result1 = f"{values[0]}{flag} -> {values[1]}🇺🇸"
                result2 = f"\nКупівля: {float(values[2])}\nПродаж: {float(values[3])}"
                result3 = result1 + "\n" + result2
                return result3

        values = list(f1.values())
        result1 = f"{values[0]}{flag} -> {values[1]}🇺🇦"
        result2 = f"\nКупівля: {float(values[2])}\nПродаж: {float(values[3])}"
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
#             error_phrase = "Занадто багато запитів до сайту Монобанк. Спробуйте через хвилину."
#             return error_phrase
#
#     def pretify_data(self, f1):
#         flag = ""
#         country = ""
#         euflag = "🇪🇺"
#         usflag = "🇺🇸"
#         ruflag = "🇷🇺"
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
#         result1 = f"{country}{flag} -> UAH🇺🇦"
#         result2 = f"\nКупити: {float(values[3])}\nПродати: {float(values[4])}"
#         result3 = result1 + "\n" + result2
#         return result3


class NationalBankOfUkraine:

    def get_data(self, cc):
        for data in get_table_National():
            if cc == data['cc']:
                return cc, data['rate']
        return False


    def pretify_data(self, data):
        country_dict = {'AUD': "🇦🇺", "CAD": "🇨🇦", "CNY": "🇨🇳", "HRK": "🇭🇷", "CZK": "🇨🇿", "DKK": "🇩🇰",
                        "HKD": "🇭🇰",
                        "HUF": "🇭🇺", "INR": "🇮🇳", "IDR": "🇮🇩", "ILS": "🇮🇱", "JPY": "🇯🇵", "KZT": "🇰🇿",
                        "KRW": "🇰🇷", "MXN": "🇲🇽",
                        "MDL": "🇲🇩", "NZD": "🇳🇿", "NOK": "🇳🇴", "RUB": "🇷🇺", "SAR": "🇸🇦", "SGD": "🇸🇬",
                        "ZAR": "🇿🇦", "SEK": "🇸🇪",
                        "CHF": "🇨🇭", "EGP": "🇪🇬", "GBP": "🇬🇧", "USD": "🇺🇸", "BYN": "🇧🇾", "RON": "🇷🇴",
                        "TRY": "🇹🇷", "BGN": "🇧🇬",
                        "EUR": "🇪🇺", "PLN": "🇵🇱", "DZD": "🇩🇿", "BDT": "🇧🇩", "AMD": "🇦🇲", "IRR": "🇮🇷",
                        "IQD": "🇮🇶", "KGS": "🇰🇬", "LBP": "🇱🇧", "LYD": "🇱🇾", "MYR": "🇲🇾", "MAD": "🇲🇦",
                        "PKR": "🇵🇰", "VND": "🇻🇳",
                        "THB": "🇹🇭", "AED": "🇦🇪", "TND": "🇹🇳", "UZS": "🇺🇿", "TMT": "🇹🇲", "RSD": "🇷🇸",
                        "AZN": "🇦🇿", "TJS": "🇹🇯", "GEL": "🇬🇪", "BRL": "🇧🇷"}

        for i in country_dict.keys():
            if i == data[0]:
                result1 = f"{i}{country_dict[i]} -> UAH🇺🇦"
                result2 = f"\nОфіційний курс: {data[1]}"
                result = result1 + "\n" + result2
                return result


