# forum_app
RESTful Flask API for forum platform with JWT authentication and user/admin roles.


# Flask Forum API

Bu proje, Flask ile geliştirilmiş, JWT tabanlı kimlik doğrulama sistemi bulunan bir forum API servisidir. Kullanıcılar kayıt olabilir, giriş yapabilir, post yazabilir, yorum yapabilir ve resim yükleyebilir. Admin kullanıcılar özel yetkilere sahiptir.

## 🚀 Özellikler

- Kullanıcı kayıt ve giriş sistemi (JWT ile)
- Kullanıcı rolleri: `user`, `admin`
- Blog post oluşturma, listeleme, güncelleme, silme
- Post'lara yorum yapma ve yorum listeleme
- Resim/dosya yükleme (kapak görseli)
- Giriş yapmış kullanıcının kendi profilini görüntüleme
- Admin kullanıcılar diğer postları silebilir
- Sayfalama ve başlığa göre arama

## 🔧 Teknolojiler

- Python 3.x
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Gunicorn (deploy için)
- SQLite (geliştirme ortamı için)

## 🗂️ API Endpointleri (Özet)

| Yöntem | URL                         | Açıklama                         |
|--------|-----------------------------|----------------------------------|
| POST   | `/users/register`           | Kullanıcı kaydı                 |
| POST   | `/users/login`              | JWT token al                    |
| GET    | `/users/me`                 | Giriş yapan kullanıcının profili|
| GET    | `/users/<id>`               | Kullanıcı profili ve postları   |
| POST   | `/posts/`                   | Post oluştur (resimle birlikte) |
| GET    | `/posts/`                   | Tüm postları listele (sayfalı)  |
| GET    | `/posts/search`             | Başlığa göre arama              |
| GET    | `/posts/<id>`               | Tek post detayları              |
| PUT    | `/posts/<id>`               | Post güncelle                   |
| DELETE | `/posts/<id>`               | Kendi postunu sil               |
| DELETE | `/posts/admin/delete/<id>`  | Admin olarak post sil           |
| POST   | `/comments/`                | Yorum yap                       |
| GET    | `/comments/post/<id>`       | Post'a ait yorumları getir      |

## 🖼️ Dosya Yükleme

- `POST /posts/` endpoint'ine `form-data` olarak `image`, `title`, `content` alanlarıyla yükleme yapılabilir.
- Görsel URL’si `uploads/` klasörü üzerinden servis edilir.

## ⚙️ Kurulum

1. Depoyu klonla:
```bash
git clone https://github.com/thousaba/forum_app.git
cd forum_app
