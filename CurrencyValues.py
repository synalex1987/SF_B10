from config import *


class CurrencyValues:
    def __init__(self, base_url=url, **kwargs):
        self.last_error = ''
        self.url = base_url
        self.params = kwargs
        self.full_url = self.return_full_url(**self.params)
        self.data = self.get_data_from_site()
        self.list_of_values = {}
        self.get_all_currencies()
        self.count_of_values = len(self.list_of_values)
        self.format_str = ''

    def return_full_url(self, **kwargs) -> str:
        params = ''
        for key, value in kwargs.items():
            params += f'{key}={value}&'
        return self.url + params[:-1]

    def get_data_from_site(self) -> dict:
        try:
            _data = requests.get(self.full_url)
            if _data.status_code == 200:
                return _data.json()
        except Exception as e:
            print('Произошла ошибка. Подробное описание: ', e)
            return {}

    @property
    def get_data(self) -> dict:
        return self.data

    def exchange_currency(self, base: str, quote: str, amount: int):
        if base in self.list_of_values and quote in self.list_of_values:
            try:
                self.full_url = f'{self.url}/pair/{base}/{quote}/{amount}'
                self.data = self.get_data_from_site()
            except Exception as e:
                print('Произошла ошибка. Подробное описание: ', e)
                self.last_error = str(e)
                return False
            self.format_str = f'За {amount} {base} вы получите {self.data["conversion_result"]} ' \
                              f'{quote} по курсу {self.data["conversion_rate"]}'
            return True
        return False

    @property
    def get_quota(self) -> bool:
        try:
            self.full_url = f'{self.url}/quota'
            self.data = self.get_data_from_site()
        except Exception as e:
            print('Произошла ошибка. Подробное описание: ', e)
            self.last_error = str(e)
            return False
        return True

    def __repr__(self):
        result = f'Источник данных(URL): {self.full_url}\nparameters: \n'
        for key, value in self.params.items():
            result += f'{key}: {value}\n'
        if self.data:
            result += f'data length: {len(self.data)}\nType of data: {type(self.data)}\n'
        return result

    @staticmethod
    def info():
        info = 'Привет. Я умею показывать текущие курсы валют.\n' \
               'Для использования отправь мне команду:\n' \
               'Валюта1 Валюта2 Количество\n' \
               'Валюта1 - имя валюты цену которой хочешь узнать,\n' \
               'Валюта2 - имя валюты в которой надо узнать цену первой валюты,\n' \
               'Количество - количество первой валюты\n' \
               'Список валют доступен по команде /values'
        return info

    def get_all_currencies(self) -> dict:
        try:
            html = requests.get(list_of_currencies_url).content
        except Exception as e:
            print('Произошла ошибка. Подробное описание: ', e)
            self.last_error = str(e)
            return {}

        soup = BeautifulSoup(html, 'lxml')
        result = {}
        table = soup.select('table')[2]
        for tr in table.select('tr'):
            tds = tr.select('td')
            name, value = tds[0].text.strip(), [tds[1].text.strip(), tds[2].text.strip()]
            result[name] = value

        result.pop('Currency Code')
        self.list_of_values = result
