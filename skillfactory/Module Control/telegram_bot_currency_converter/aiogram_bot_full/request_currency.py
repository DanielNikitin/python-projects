import requests, json

def convert_currency():
    from_currency = str(
    input("Enter desired currency ")).upper()

    to_currency = str(
    input("Enter to currency ")).upper()

    amount = float(input("Enter amount "))

    responce = requests.get(
    f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}")

    print(
    f"{amount} {from_currency} is {responce.json()['rates'][to_currency]} {to_currency}")


def data_currency():
    #response = requests.get("https://api.frankfurter.app/latest")  # тут найдём ключ 'rates'
    response = requests.get("https://api.frankfurter.app/currencies")
    data = response.json()
    # Сортируем словарь по ключам (кодам валют) и сохраняем его в новую переменную
    sorted_data = dict(sorted(data.items()))

    # Выводим данные в желаемом формате
    for currency_code, currency_name in sorted_data.items():
        print(f'"{currency_code}": "{currency_name}",')

if __name__ == '__main__':
    #convert_currency()
    data_currency()