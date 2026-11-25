# پنج Test Case

| ID | سناریو | ورودی/پیش‌شرط | نتیجه مورد انتظار | پوشش |
|---|---|---|---|---|
| TC-01 | بررسی سلامت | GET `/health` | 200 و status=ok | health endpoint |
| TC-02 | ساخت و دریافت کاربر | نام و ایمیل معتبر | POST=201، GET=200 و اطلاعات درست | Users |
| TC-03 | ایمیل تکراری | ساخت دوباره با همان ایمیل | 409 Conflict | یکتایی ایمیل |
| TC-04 | ساخت Task برای کاربر ناموجود | user_id=999 | 404 Not Found | رابطه User/Task |
| TC-05 | تکمیل Task | ساخت کاربر و Task، سپس PATCH completed=true | 200 و completed=true | چرخه Task |

## محل شکست Pipeline
اگر هر assertion در مرحله `Run tests` ناموفق باشد، دستور `pytest -q` با کد خروج غیرصفر تمام می‌شود. GitHub Actions مرحله بعدی یعنی `Build Docker image` را اجرا نمی‌کند.

## ارتباط Docker و Pipeline
Pipeline در محیط runner وابستگی‌ها را نصب و تست‌ها را اجرا می‌کند. پس از موفقیت تست‌ها، همان سورس با Dockerfile به image تبدیل می‌شود. در این نسخه image ساخته می‌شود اما به registry انتشار داده نمی‌شود.
