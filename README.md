# Тестовое задание для разработчика команды Краулинг

## Описание задачи
Нужно получить самые свежие данные с сайта https://ms1.mirsud24.ru/ms/sudoproizvodstvo/informatsiya-po-sudebnym-delam/ по судебному делу, которое было заведено, истцом по которому выступает Тинькофф Банк. Нас интересует гражданское судопроизводство и дело должно быть этого года.

Для найденного дела нам нужно получить общую информацию по делу и его статусы.

## Запуск скрипта
```console
python -m main
```

## Проверка кода
```console
poetry run python -m pytest
poetry run python -m mypy .
poetry run python -m ruff check
poetry run python -m ruff check --select I --fix
poetry run python -m ruff format
```