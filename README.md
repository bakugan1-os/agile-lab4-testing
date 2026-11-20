# HealthyDay — юніт-тести та CI

Лабораторна робота 4 з дисципліни «Гнучкі технології розробки ПЗ».

- `math_module.py` — приклад із методичних вказівок (факторіал, парність числа);
- `healthyday/hydration.py` — бізнес-логіка застосунку HealthyDay: денна норма води, прогрес, «тихі години», рішення про нагадування;
- `tests/` — юніт-тести на PyTest;
- `.github/workflows/ci.yml` — GitHub Actions: тести на Python 3.10, 3.11, 3.12 при кожному push і pull request;
- `Jenkinsfile` — той самий конвеєр для Jenkins (перевірка нових комітів щохвилини).

Запуск локально:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest --cov=healthyday --cov=math_module --cov-report=term-missing
```
