# Brand Rating Analysis (CLI)

CLI-утилита для агрегации CSV с товарами и построения отчётов.

# Требования

Python 3.12+
# Установка
1) Клонирование репозитория
```bash
  git clone https://github.com/Akds-ubuntu/Brand-Rating-Analysis.git
  cd Brand-Rating-Analysis
```
2) Подготовка окружения
```bash
  python -m venv .venv
  # macOS/Linux
  source .venv/bin/activate
  # Windows (PowerShell)
  .venv\Scripts\Activate.ps1
```
3) Установка зависимостей
```bash
    pip install -r requirements.txt
```
4) Запуск CLI
```bash
  python -m scr.cli --files data/Products_1.csv data/Products_2.csv --report average-rating
```
5) Тесты и покрытие
```bash
  pytest
```
# Контракт пользовательского отчёта
Добавьте файл в каталог scr/reports/, где будет находиться новый отчёт.
## Сигнатура
```python
from collections.abc import Iterable
from scr.reports import ReportRow  # = Mapping[str, Any]

def my_report(rows: Iterable[ReportRow]) -> list[ReportRow]:
    ...

```
### Вход(rows)
Доступные поля:
- name
- brand
- price
- rating

### Выход (обязательно)

Итерируемое (список или генератор) из словарей с ровно этими ключами:

- label

- metric ← сюда кладём любую числовую метрику (среднее, медиана, максимум и т.д.)

- contexst: 

CLI форматирует вывод строго по этим ключам, поэтому их нельзя менять.

# Регистрация отчёта
В конце файла с новым отчётом зарегистрируйте функцию под именем, которое будет использоваться в --report:
```python
from scr.reports import register_report

register_report("имя-для-cli", my_report)
```
Необязательные метаданные (заголовки таблицы)
В отчёте можно задать шапку таблицы:
```python
my_report.HEADERS = ["brand", "median rating", "count"]

```
