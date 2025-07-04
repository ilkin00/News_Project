# Generated by Django 5.2.3 on 2025-06-21 11:54

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Kategori Adı')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='SEO URL')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif Mi?')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Sıralama')),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='category_images/', verbose_name='Kapak Resmi')),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategoriler',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='NewsletterSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-posta')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif Abonelik')),
                ('subscribed_at', models.DateTimeField(auto_now_add=True, verbose_name='Abonelik Tarihi')),
                ('preferences', models.JSONField(default=list, verbose_name='Tercihler')),
            ],
            options={
                'verbose_name': 'Bülten Aboneliği',
                'verbose_name_plural': 'Bülten Abonelikleri',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Haber Sitesi', max_length=100)),
                ('site_description', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='site_settings/')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='site_settings/')),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('facebook_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Site Ayarı',
                'verbose_name_plural': 'Site Ayarları',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Etiket Adı')),
                ('slug', models.SlugField(unique=True, verbose_name='SEO URL')),
            ],
            options={
                'verbose_name': 'Etiket',
                'verbose_name_plural': 'Etiketler',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('admin', 'Yönetici'), ('editor', 'Editör'), ('reporter', 'Muhabir'), ('user', 'Standart Kullanıcı')], default='user', max_length=10, verbose_name='Kullanıcı Rolü')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/', verbose_name='Profil Resmi')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Biyografi')),
                ('verified', models.BooleanField(default=False, verbose_name='Doğrulanmış Kullanıcı')),
                ('preferences', models.JSONField(blank=True, default=dict, verbose_name='Tercihler')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Kullanıcı',
                'verbose_name_plural': 'Kullanıcılar',
                'ordering': ['-date_joined'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Başlık')),
                ('slug', models.SlugField(max_length=200, unique_for_date='publish_date', verbose_name='SEO URL')),
                ('content', models.TextField(verbose_name='İçerik')),
                ('excerpt', models.TextField(blank=True, max_length=300, verbose_name='Özet')),
                ('status', models.CharField(choices=[('draft', 'Taslak'), ('published', 'Yayında'), ('archived', 'Arşivlendi')], default='draft', max_length=10, verbose_name='Durum')),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Yayın Tarihi')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('featured_image', models.ImageField(upload_to='article_images/%Y/%m/%d/', verbose_name='Kapak Resmi')),
                ('view_count', models.PositiveBigIntegerField(default=0, verbose_name='Görüntülenme Sayısı')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Öne Çıkarılmış')),
                ('is_hot', models.BooleanField(default=False, verbose_name='Son Dakika')),
                ('hot_expiry', models.DateTimeField(blank=True, null=True, verbose_name='Son Dakika Bitiş Tarihi')),
                ('meta_title', models.CharField(blank=True, max_length=100, verbose_name='Meta Başlık')),
                ('meta_description', models.CharField(blank=True, max_length=200, verbose_name='Meta Açıklama')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Yazar')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='news.category', verbose_name='Kategori')),
                ('tags', models.ManyToManyField(blank=True, related_name='articles', to='news.tag', verbose_name='Etiketler')),
            ],
            options={
                'verbose_name': 'Haber',
                'verbose_name_plural': 'Haberler',
                'ordering': ['-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Yorum')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')),
                ('is_approved', models.BooleanField(default=True, verbose_name='Onaylandı Mı?')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.article', verbose_name='Haber')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='news.comment', verbose_name='Üst Yorum')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'Yorum',
                'verbose_name_plural': 'Yorumlar',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='HotNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='Öncelik')),
                ('expiry', models.DateTimeField(verbose_name='Son Geçerlilik Tarihi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hot_news_status', to='news.article', verbose_name='Haber')),
            ],
            options={
                'verbose_name': 'Son Dakika Haberi',
                'verbose_name_plural': 'Son Dakika Haberleri',
                'ordering': ['priority', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('image', 'Resim'), ('video', 'Video'), ('audio', 'Ses'), ('gallery', 'Galeri')], max_length=10, verbose_name='Medya Türü')),
                ('file', models.FileField(upload_to='article_media/%Y/%m/%d/', verbose_name='Dosya')),
                ('caption', models.CharField(blank=True, max_length=200, verbose_name='Başlık')),
                ('alt_text', models.CharField(blank=True, max_length=100, verbose_name='Alternatif Metin')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Sıralama')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_files', to='news.article', verbose_name='Haber')),
            ],
            options={
                'verbose_name': 'Medya',
                'verbose_name_plural': 'Medya Dosyaları',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('breaking', 'Son Dakika'), ('recommendation', 'Öneri'), ('system', 'Sistem'), ('social', 'Sosyal')], max_length=15, verbose_name='Bildirim Türü')),
                ('title', models.CharField(max_length=100, verbose_name='Başlık')),
                ('message', models.TextField(verbose_name='Mesaj')),
                ('is_read', models.BooleanField(default=False, verbose_name='Okundu Mu?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.article', verbose_name='İlgili Haber')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'Bildirim',
                'verbose_name_plural': 'Bildirimler',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=200, verbose_name='Arama Sorgusu')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP Adresi')),
                ('results_count', models.PositiveIntegerField(verbose_name='Sonuç Sayısı')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'Arama Sorgusu',
                'verbose_name_plural': 'Arama Sorguları',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TrendingArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0.0, verbose_name='Popülerlik Skoru')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Son Güncellenme')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trending_status', to='news.article', verbose_name='Haber')),
            ],
            options={
                'verbose_name': 'Trend Haber',
                'verbose_name_plural': 'Trend Haberler',
                'ordering': ['-score'],
            },
        ),
        migrations.CreateModel(
            name='ArticleView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP Adresi')),
                ('user_agent', models.TextField(blank=True, null=True, verbose_name='Tarayıcı Bilgisi')),
                ('referrer', models.URLField(blank=True, null=True, verbose_name='Referans URL')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='news.article', verbose_name='Haber')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'Haber Görüntüleme',
                'verbose_name_plural': 'Haber Görüntülemeleri',
                'indexes': [models.Index(fields=['article', 'created_at'], name='news_articl_article_25bea2_idx'), models.Index(fields=['ip_address', 'created_at'], name='news_articl_ip_addr_8a3c33_idx')],
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked_by', to='news.article', verbose_name='Haber')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'Yer İşareti',
                'verbose_name_plural': 'Yer İşaretleri',
                'unique_together': {('user', 'article')},
            },
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction_type', models.CharField(choices=[('like', 'Beğen'), ('love', 'Sevgi'), ('haha', 'Güldü'), ('wow', 'Şaşırdı'), ('sad', 'Üzüldü'), ('angry', 'Kızdı')], max_length=10, verbose_name='Tepki Türü')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='news.article', verbose_name='Haber')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'Tepki',
                'verbose_name_plural': 'Tepkiler',
                'unique_together': {('article', 'user')},
            },
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['publish_date'], name='news_articl_publish_e83d07_idx'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['status'], name='news_articl_status_a95c4c_idx'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['is_featured'], name='news_articl_is_feat_0df2de_idx'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['is_hot'], name='news_articl_is_hot_804ea1_idx'),
        ),
    ]
