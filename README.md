# 📰 Xəbər Saytı API (Django Rest Framework)

Bu layihə, xəbər saytları üçün hazırlanmış bir RESTful API sistemidir. İstifadəçilər qeydiyyatdan keçə, məqalələr oxuya, şərh yaza, reaksiyalar bildirə və bəyənilən xəbərləri saxlayaraq qeyd edə bilər.

---

## 🔐 Authentication & User

### 🔹 Qeydiyyat
`POST /api/auth/register/`

**Body:**
```json
{
  "email": "test@example.com",
  "password": "12345678",
  "password2": "12345678",
  "full_name": "İstifadəçi Adı"
}
🔹 Giriş (Token əldə et)

POST /api/auth/login/

Body:

{
  "username": "test@example.com",
  "password": "12345678"
}

Cavab:

{
  "token": "xxxxxxxxxx",
  "user_id": 1,
  "email": "test@example.com",
  "role": "user"
}

🔹 Profilə bax / yenilə

GET /api/auth/profile/
PUT /api/auth/profile/

Header: Authorization: Token <token>
🔐 Şifrə əməliyyatları
🔹 Şifrə sıfırlama (mail göndərilir)

POST /api/auth/password-reset/

{
  "email": "test@example.com"
}

🔹 Yeni şifrəni təsdiqlə

POST /api/auth/password-reset-confirm/

{
  "uidb64": "Mg",
  "token": "set-password-token",
  "new_password": "yeni123456"
}

🔹 Şifrəni dəyiş

PUT /api/auth/change-password/

{
  "old_password": "12345678",
  "new_password": "yeni123456"
}

📄 Məqalələr
🔹 Məqalə siyahısı

GET /api/articles/
Query Parametrlər:

    search: başlıqda və məqalədə axtarış

    ordering: publish_date, view_count

    category, tags, author

Misal:

/api/articles/?search=Zəfər&ordering=-view_count

🔹 Məqalə detalları

GET /api/articles/<slug>/
🔥 Xüsusi xəbərlər
🔹 Seçilmiş xəbərlər

GET /api/articles/featured/
🔹 "Hot" xəbərlər

GET /api/articles/hot/
🗂️ Kateqoriya & Etiketlər
🔹 Kateqoriyalar

GET /api/categories/
🔹 Etiketlər

## Kateqoriyaya görə məqalələr
GET /api/categories/articles/?search=<slug>

GET /api/tags/
💬 Şərhlər
🔹 Şərhləri görüntüle / əlavə et

## Tags görə məqalələr
GET /api/Tags/articles/?search=<slug>

GET /api/articles/<slug>/comments/
POST /api/articles/<slug>/comments/

{
  "content": "Möhtəşəm xəbər!"
}

👍 Reaksiyalar
🔹 Reaksiya əlavə et / yenilə

POST /api/reactions/

{
  "article": 1,
  "reaction_type": "like"
}

📌 Qeyd edilənlər (Bookmark)
🔹 Siyahı

GET /api/bookmarks/
🔹 Əlavə et

POST /api/bookmarks/

{
  "article": 1
}

🔹 Sil

DELETE /api/bookmarks/<article_id>/
📨 Bülleten abunəliyi

POST /api/newsletter/

{
  "email": "test@example.com"
}

⚙️ Sayt ayarları

GET /api/settings/
🔍 Məqalə Axtarışı (POST ilə)

POST /api/articles/?search=<slug>


Cavab: uyğun olan məqalələrin siyahısı.
🔗 API Root

GET /api/ — bütün əsas endpoint-lərin linklərini verir.
📌 Qeyd

    Bütün istifadəçi ilə əlaqəli endpoint-lər üçün Token tələb olunur.

    Token başlıqda belə verilməlidir:

Authorization: Token <sənin-token>

🛠 Texnologiyalar

    Django

    Django Rest Framework

    Token Authentication

    Django Filters

📁 Quraşdırma (yerli işlətmək üçün)

git clone <repo>
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
