# 1️⃣ نصب کتابخانه فشرده‌سازی 7z (فقط بار اول اجرا لازمه)
!pip install py7zr

# 2️⃣ ایمپورت کتابخانه‌ها
import requests
import py7zr
import os

# 3️⃣ 🎬 پارامترهای قابل تنظیم توسط کاربر
MOVIE_NAME = "Inception"          # ← نام فیلم
NUM_REVIEWS = 5                   # ← تعداد نقدهایی که می‌خوای ذخیره کنی
API_KEY = "اینجا API KEY خودتو بذار"  # ← کلید API اختصاصی نیویورک تایمز

# 4️⃣ تابع گرفتن نقدهای فیلم
def get_reviews(movie_name, max_results):
    url = "https://api.nytimes.com/svc/movies/v2/reviews/search.json"
    params = {
        "query": movie_name,
        "api-key": API_KEY
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("⚠️ خطا در اتصال به API:", response.status_code)
        return []

    data = response.json()
    results = data.get("results", [])
    return results[:max_results]

# 5️⃣ ذخیره نقدها در فایل متنی
def save_reviews_to_txt(reviews, filename="movie_reviews.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for i, review in enumerate(reviews, 1):
            file.write(f"📝 نقد شماره {i}:\n")
            file.write(f"عنوان فیلم: {review.get('display_title', 'نامشخص')}\n")
            file.write(f"منتقد: {review.get('byline', 'نامشخص')}\n")
            file.write(f"تاریخ انتشار: {review.get('publication_date', 'ندارد')}\n")
            file.write(f"خلاصه نقد: {review.get('summary_short', 'ندارد')}\n")
            file.write(f"لینک نقد: {review.get('link', {}).get('url', 'ندارد')}\n")
            file.write("-" * 60 + "\n")
    print(f"✅ ذخیره شد در فایل: {filename}")

# 6️⃣ تبدیل فایل متنی به فایل 7z
def compress_to_7z(input_file, archive_name="movie_reviews.7z"):
    with py7zr.SevenZipFile(archive_name, 'w') as archive:
        archive.write(input_file)
    print(f"📦 فایل فشرده ساخته شد: {archive_name}")

# 7️⃣ اجرای توابع
reviews = get_reviews(MOVIE_NAME, NUM_REVIEWS)
if reviews:
    save_reviews_to_txt(reviews)
    compress_to_7z("movie_reviews.txt")

# 8️⃣ آماده‌سازی لینک دانلود فایل 7z
from google.colab import files
files.download("movie_reviews.7z")
