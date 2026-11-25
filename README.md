# Users & Tasks API

پروژه آموزشی برای فعالیت‌های فصل ۳، ۴ و ۵: طراحی API، Docker و تست/CI.

## نیازمندی‌ها
- Python 3.12+
- (اختیاری) Docker

## اجرای محلی
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```
سپس مستندات تعاملی در `http://127.0.0.1:8000/docs` و سلامت سرویس در `/health` در دسترس است.

## اجرای تست‌ها
```bash
pip install -r requirements-dev.txt
pytest -q
```

## اجرای Docker
```bash
docker build -t users-tasks-api .
docker run --name users-tasks-api -p 8000:8000 users-tasks-api
```
در مرورگر `http://localhost:8000/docs` را باز کنید. برای توقف: `docker stop users-tasks-api`.

## فعالیت ۳ — API Contract
منابع اصلی `Users` و `Tasks` هستند. جزئیات متدها، ورودی‌ها و کدهای پاسخ در `docs/api-contract.md` آمده است. دیاگرام معماری: `docs/architecture.mmd`.

## فعالیت ۴ — Containerization
`Dockerfile` تصویر برنامه را می‌سازد؛ `.dockerignore` فایل‌های غیرضروری را از build context کنار می‌گذارد. نگاشت پورت `8000:8000` پورت میزبان را به پورت برنامه داخل کانتینر وصل می‌کند.

## فعالیت ۵ — Testing و CI/CD
پنج تست در `tests/test_api.py` قرار دارد. گردش CI در `.github/workflows/ci.yml` ابتدا تست‌ها را اجرا می‌کند و فقط در صورت موفقیت، Docker image را build می‌کند. مرحله شکست تست، گام `Run tests` است؛ در این حالت job متوقف می‌شود و build اجرا نخواهد شد.

## نکته آموزشی
این پروژه برای تمرین است؛ قبل از استفاده واقعی باید احراز هویت، مجوزدهی، اعتبارسنجی دقیق ایمیل، مدیریت خطا و پیکربندی امن پایگاه داده تکمیل شود.
