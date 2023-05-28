'''
    Скрипт для обращения к внешнему API Alation для сохранения всех
    объектов типа «отчет BI» с «зеленым светофором» в виде csv файла.
'''
from __future__ import annotations

from json import loads
from typing import List, Dict, Any

from pandas import DataFrame
import requests


def get_articles(
        alation_instance_url: str,
        token: str
) -> List[Dict[str, str | int]]:
    '''
        Получение статей из внешнего ресурса.

        Реализация запроса к API Alation для получения информации
        обо всех отчетах для соответствующего каталога Alation.

        :param alation_instance_url: URL-адрес каталога, в котором
        происходит поиск.
        :param token: Токен идентификации.

        :raise: Исключение (кастомное) при неуспешной отправке запроса.

        :return: Список отчетов с информацией о каждом (пример вывода в файле
        `./docs/response.txt`.
    '''
    headers = {'Token': token}
    all_flags_url = alation_instance_url + '/integration/flag'

    response = requests.get(all_flags_url, headers=headers, timeout=5)

    if response.status_code != 200:
        # Вызов исключения, дополнительная логика
        ...

    found_reports = loads(response.text)

    return found_reports


def extract_urls_and_names(found_reports) -> tuple[tuple[str, str]]:
    '''
        Извлечение данных из ответа от внешнего ресурса.

        Получение URL-адресов статей с измененным флагом
        и имен пользователей, которые установили его.

        Фильтрация по типу объектов (Отчет BI) и по типу флага ("ENDORSEMENT").

        :param found_reports: Ответ от внешнего ресурса с полной
        информацией об отчетах.

        :return: Кортеж кортежей с URL-адресами статей и искомыми
        именами пользователей.
    '''
    urls_and_names = tuple(
        (report['subject']['url'], report['user']['display_name'])
        for report in found_reports
        if (
                report['subject']['otype'] == 'bi_report'
                and report['flag_type'] == 'ENDORSEMENT'
        )
    )

    return urls_and_names


def write_to_csv(
        data_to_write: tuple[tuple[str, str]],
        path_to_csv: str = './output/flags.csv'
) -> bool:
    '''
        Запись URL-адресов статей и имен пользователей в CSV-файл.

        Создание CSV-файла, заполнение первой строки названиями столбцов
        и заполнение остальных строк информацией из полученных кортежей.

        :param data_to_write: Данные об URL-адресах статей
        и именах пользователей, которые необходимо внести в CSV-файл.
        :param path_to_csv: Путь, по которому хранится
        созданный/измененный файл.

        :return: -
    '''
    df = DataFrame(
        data_to_write,
        columns=['URL отчета', 'ФИО пользователя, который установил флаг']
    )
    df.to_csv(path_to_csv, sep=';', index=False, encoding='utf-8')

    return True


if __name__ == '__main__':
    AlationInstanceURL = 'known_alation_instance_url'
    token = 'known_token'

    reports = get_articles(
        alation_instance_url=AlationInstanceURL,
        token=token
    )
    urls_and_names = extract_urls_and_names(reports)
    write_to_csv(data_to_write=urls_and_names)
