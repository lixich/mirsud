from io import StringIO
from typing import Any, Dict, Union

import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel


class HtmlTableConfig(BaseModel):
    selector_id: str
    selector_tag: str = 'div'
    table_num: int = 0
    table_value_column: Union[int, str]
    table_name_column: Union[int, str]


class HtmlTransformer:
    _configs = [
        # Вкладка Основное
        HtmlTableConfig(
            selector_id='part1',
            table_name_column=0,
            table_value_column=1,
        ),
        # Вкладка Участники
        HtmlTableConfig(
            selector_id='part2',
            table_name_column='Статус участника',
            table_value_column='Участник',
        ),
        # Вкладка Движение
        HtmlTableConfig(
            selector_id='part5',
            table_name_column='Состояние',
            table_value_column='Дата',
        ),
    ]

    def __init__(self, html: str):
        self._soup = BeautifulSoup(html, features='lxml')

    def run(self) -> Dict[str, Any]:
        row = {}
        for config in self._configs:
            part_soup = self._soup.find(config.selector_tag, {'id': config.selector_id})
            df = pd.read_html(StringIO(str(part_soup)))[config.table_num]
            names = df[config.table_name_column].to_list()
            values = df[config.table_value_column].to_list()
            table_as_dict = {name: value for name, value in zip(names, values)}
            row.update(table_as_dict)

        return row
