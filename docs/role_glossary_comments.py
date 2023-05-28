#!/usr/bin/env python3

# Предполагается, что модуль logger_utils и alation
# реализованы корректно
import utils.logger_utils as logger
from utils.alation import Alation
import requests

# Отключение предупреждений о сертификатах. По всей видимости
# взаимодействие с API выполняется по протоколу HTTPS
requests.packages.urllib3.disable_warnings()


def main(settings, *args, **kwargs):
    # Создание объекта alation с передачей настроек
    alation = Alation(**settings.ALATION_API, name='role_model')

    # Получение базового URL из объекта alation и сессии для подключения
    base_url = alation.api_entry
    alation_s = alation.session

    # Создание словаря с названиями групп с названием группы в качестве
    # ключа и вложенным словарем с информацией по ID группы и ее названию
    # в качестве значения словаря
    groups = {
        group['display_name']: {
            'id': group['id'],
            'name': group['display_name']
        } for group in alation.get_groups()
    }

    # Создание словаря с политиками доступа к редактированию и к группам для
    # редактирования (значения получены из словаря групп)
    policies = {
        "permissions": {
            "private": 'true',
            "private_edit": 'false',
            "users_can_share": 'true',
            "allowed_group_editors": [
                groups["Metodolog"],
            ],
            "allowed_groups": [
                groups["Коннектор"],
            ]
        }
    }
    
    template_name = "Бизнес-глоссарий"
    custom_template_id = 26

    # Логирование начала скрипта
    logger.info('ROLE TEST')

    # Выполнение GET-запроса по указанному URL с помощью созданной сессии
    with alation_s.get(f"{base_url}/integration/v1/article/?custom_field_templates=[{custom_template_id}]") as r:
        for article in r.json():
            # Логирование ID каждой отфильтрованной статьи
            logger.info(f"ID {article['id']}")

            if article['id'] == 149:
                # Выполнение PATCH-запроса по указанному URL с помощью
                # созданной сессии (изменение политик доступа)
                with alation_s.patch(
                        f"{base_url}/api/v1/article/{article['id']}/",
                        json=policies
                ) as patch_resp:
                    # Логирование информации об измененной статье
                    logger.debug("Title {}".format(article['title']))
                    logger.debug(patch_resp.status_code)
                    logger.debug(patch_resp.json())


# Точка входа
if __name__ == "__main__":
    main()
