# API Contract — نسخه ۱

Base URL محلی: `http://localhost:8000`

## Resources
- **User**: `id`, `name`, `email`
- **Task**: `id`, `title`, `description`, `completed`, `user_id`

## Users endpoints

| Method | Endpoint | شرح | موفق | خطاهای مهم |
|---|---|---|---|---|
| POST | `/users` | ساخت کاربر | 201 | 409 ایمیل تکراری، 422 ورودی نامعتبر |
| GET | `/users` | فهرست کاربران | 200 | — |
| GET | `/users/{user_id}` | دریافت یک کاربر | 200 | 404 یافت نشد |
| DELETE | `/users/{user_id}` | حذف کاربر | 204 | 404 یافت نشد |

نمونه بدنه POST:
```json
{"name":"Sara","email":"sara@example.com"}
```

## Tasks endpoints

| Method | Endpoint | شرح | موفق | خطاهای مهم |
|---|---|---|---|---|
| POST | `/tasks` | ساخت وظیفه برای کاربر موجود | 201 | 404 کاربر وجود ندارد، 422 ورودی نامعتبر |
| GET | `/tasks` | فهرست وظایف؛ فیلتر اختیاری `user_id` | 200 | — |
| PATCH | `/tasks/{task_id}` | ویرایش عنوان/توضیح/وضعیت | 200 | 400 بدنه خالی، 404 یافت نشد، 422 ورودی نامعتبر |
| DELETE | `/tasks/{task_id}` | حذف وظیفه | 204 | 404 یافت نشد |

نمونه بدنه POST:
```json
{"title":"Finish report","description":"Chapter 3","user_id":1}
```

نمونه PATCH:
```json
{"completed":true}
```

## سایر مسیرها
| Method | Endpoint | شرح | پاسخ |
|---|---|---|---|
| GET | `/health` | بررسی سلامت سرویس | 200 `{"status":"ok"}` |

## قواعد
- شناسه‌ها عدد صحیح و خودکار هستند.
- ایمیل کاربر یکتا است.
- ساخت Task فقط برای `user_id` موجود مجاز است.
- خطای اعتبارسنجی FastAPI به‌صورت 422 بازگردانده می‌شود.
- حذف موفق، پاسخ بدون بدنه با کد 204 دارد.
