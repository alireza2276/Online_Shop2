# Online Shop 2 - Refreshed

A Django e-commerce learning project with product catalog, categories, comments, likes, session cart, coupons, orders, Zarinpal payment integration, authentication, and a REST API.

## What was refreshed
- Removed hard-coded Django secret and database password from settings.
- SQLite is now the zero-config default; MySQL is optional through environment variables.
- Fixed web checkout so `Order.customer` is populated correctly.
- Fixed cart totals and coupon handling.
- Fixed several payment bugs (`get_total_price()`, customer access, authority key, ref id persistence).
- Fixed broken API product creation, cart validation, duplicate order-item creation, comment author handling, and customer lookup.
- Debug toolbar is enabled only in debug mode.
- Replaced unsafe/obsolete Pickle session serializer with JSON.
- Added missing REST/JWT/filter/router dependencies and normalized `requirements.txt`.
- Added `.env.example` and a safer `.gitignore`.

## Run locally
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Notes
This is still best treated as a learning/portfolio project, not a production store. Before production use, add automated tests, inventory/stock management, robust payment error handling/timeouts, order state transitions, logging/monitoring, and deployment configuration.
