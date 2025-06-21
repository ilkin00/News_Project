# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

# 1. Kullanıcı Modeli (Custom User)
class User(AbstractUser):
    ROLES = (
        ('admin', 'Yönetici'),
        ('editor', 'Editör'),
        ('reporter', 'Muhabir'),
        ('user', 'Standart Kullanıcı'),
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default='user',
        verbose_name="Kullanıcı Rolü"
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        verbose_name="Profil Resmi"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biyografi"
    )
    verified = models.BooleanField(
        default=False,
        verbose_name="Doğrulanmış Kullanıcı"
    )
    preferences = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Tercihler"
    )
    
    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username

# 2. Kategori Modeli
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kategori Adı"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="SEO URL"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Açıklama"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif Mi?"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıralama"
    )
    featured_image = models.ImageField(
        upload_to='category_images/',
        null=True,
        blank=True,
        verbose_name="Kapak Resmi"
    )
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_news', kwargs={'slug': self.slug})

# 3. Etiket Modeli
class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Etiket Adı"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="SEO URL"
    )
    
    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# 4. Haber Modeli (Ana Model)
class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Taslak'),
        ('published', 'Yayında'),
        ('archived', 'Arşivlendi'),
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name="Başlık"
    )
    slug = models.SlugField(
        max_length=200,
        unique_for_date='publish_date',
        verbose_name="SEO URL"
    )
    content = models.TextField(
        verbose_name="İçerik"
    )
    excerpt = models.TextField(
        max_length=300,
        blank=True,
        verbose_name="Özet"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name="Yazar"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name="Kategori"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles',
        verbose_name="Etiketler"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Durum"
    )
    publish_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Yayın Tarihi"
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Güncellenme Tarihi"
    )
    featured_image = models.ImageField(
        upload_to='article_images/%Y/%m/%d/',
        verbose_name="Kapak Resmi"
    )
    view_count = models.PositiveBigIntegerField(
        default=0,
        verbose_name="Görüntülenme Sayısı"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Öne Çıkarılmış"
    )
    is_hot = models.BooleanField(
        default=False,
        verbose_name="Son Dakika"
    )
    hot_expiry = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Son Dakika Bitiş Tarihi"
    )
    meta_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Meta Başlık"
    )
    meta_description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Meta Açıklama"
    )
    
    class Meta:
        verbose_name = "Haber"
        verbose_name_plural = "Haberler"
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['publish_date']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_hot']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.month,
            'day': self.publish_date.day,
            'slug': self.slug
        })
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

# 5. Medya Modeli
class Media(models.Model):
    MEDIA_TYPES = (
        ('image', 'Resim'),
        ('video', 'Video'),
        ('audio', 'Ses'),
        ('gallery', 'Galeri'),
    )
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='media_files',
        verbose_name="Haber"
    )
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
        verbose_name="Medya Türü"
    )
    file = models.FileField(
        upload_to='article_media/%Y/%m/%d/',
        verbose_name="Dosya"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Başlık"
    )
    alt_text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Alternatif Metin"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıralama"
    )
    
    class Meta:
        verbose_name = "Medya"
        verbose_name_plural = "Medya Dosyaları"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.get_media_type_display()} - {self.article.title}"

# 6. Yorum Modeli
class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Haber"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Kullanıcı"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="Üst Yorum"
    )
    content = models.TextField(
        verbose_name="Yorum"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Güncellenme Tarihi"
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name="Onaylandı Mı?"
    )
    
    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.article.title[:20]}..."

# 7. Tepki Modeli
class Reaction(models.Model):
    REACTION_TYPES = (
        ('like', 'Beğen'),
        ('love', 'Sevgi'),
        ('haha', 'Güldü'),
        ('wow', 'Şaşırdı'),
        ('sad', 'Üzüldü'),
        ('angry', 'Kızdı'),
    )
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name="Haber"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name="Kullanıcı"
    )
    reaction_type = models.CharField(
        max_length=10,
        choices=REACTION_TYPES,
        verbose_name="Tepki Türü"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    class Meta:
        verbose_name = "Tepki"
        verbose_name_plural = "Tepkiler"
        unique_together = ('article', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_reaction_type_display()} - {self.article.title[:20]}..."

# 8. Yer İşareti Modeli
class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
        verbose_name="Kullanıcı"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='bookmarked_by',
        verbose_name="Haber"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    class Meta:
        verbose_name = "Yer İşareti"
        verbose_name_plural = "Yer İşaretleri"
        unique_together = ('user', 'article')
    
    def __str__(self):
        return f"{self.user.username} - {self.article.title[:20]}..."

# 9. Trend Haber Modeli
class TrendingArticle(models.Model):
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        related_name='trending_status',
        verbose_name="Haber"
    )
    score = models.FloatField(
        default=0.0,
        verbose_name="Popülerlik Skoru"
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Son Güncellenme"
    )
    
    class Meta:
        verbose_name = "Trend Haber"
        verbose_name_plural = "Trend Haberler"
        ordering = ['-score']
    
    def __str__(self):
        return f"{self.article.title[:20]}... - Skor: {self.score:.2f}"

# 10. Son Dakika Haber Modeli
class HotNews(models.Model):
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        related_name='hot_news_status',
        verbose_name="Haber"
    )
    priority = models.PositiveIntegerField(
        default=1,
        verbose_name="Öncelik"
    )
    expiry = models.DateTimeField(
        verbose_name="Son Geçerlilik Tarihi"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    class Meta:
        verbose_name = "Son Dakika Haberi"
        verbose_name_plural = "Son Dakika Haberleri"
        ordering = ['priority', '-created_at']
    
    def __str__(self):
        return f"{self.article.title[:20]}... - Öncelik: {self.priority}"

# 11. Bülten Aboneliği Modeli
class NewsletterSubscription(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="E-posta"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif Abonelik"
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Abonelik Tarihi"
    )
    preferences = models.JSONField(
        default=list,
        verbose_name="Tercihler"
    )
    
    class Meta:
        verbose_name = "Bülten Aboneliği"
        verbose_name_plural = "Bülten Abonelikleri"
    
    def __str__(self):
        return self.email

# 12. Bildirim Modeli
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('breaking', 'Son Dakika'),
        ('recommendation', 'Öneri'),
        ('system', 'Sistem'),
        ('social', 'Sosyal'),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Kullanıcı"
    )
    notification_type = models.CharField(
        max_length=15,
        choices=NOTIFICATION_TYPES,
        verbose_name="Bildirim Türü"
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Başlık"
    )
    message = models.TextField(
        verbose_name="Mesaj"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="İlgili Haber"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Okundu Mu?"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    class Meta:
        verbose_name = "Bildirim"
        verbose_name_plural = "Bildirimler"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title[:20]}..."

# 13. Haber Görüntüleme Modeli (Analiz)
class ArticleView(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name="Haber"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kullanıcı"
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="IP Adresi"
    )
    user_agent = models.TextField(
        blank=True,
        null=True,
        verbose_name="Tarayıcı Bilgisi"
    )
    referrer = models.URLField(
        blank=True,
        null=True,
        verbose_name="Referans URL"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    class Meta:
        verbose_name = "Haber Görüntüleme"
        verbose_name_plural = "Haber Görüntülemeleri"
        indexes = [
            models.Index(fields=['article', 'created_at']),
            models.Index(fields=['ip_address', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.article.title[:20]}... - {self.created_at}"

# 14. Arama Sorgusu Modeli (Analiz)
class SearchQuery(models.Model):
    query = models.CharField(
        max_length=200,
        verbose_name="Arama Sorgusu"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kullanıcı"
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="IP Adresi"
    )
    results_count = models.PositiveIntegerField(
        verbose_name="Sonuç Sayısı"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    class Meta:
        verbose_name = "Arama Sorgusu"
        verbose_name_plural = "Arama Sorguları"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.query} - {self.created_at}"

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Haber Sitesi')
    site_description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site_settings/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site_settings/', null=True, blank=True)
    contact_email = models.EmailField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Site Ayarı"
        verbose_name_plural = "Site Ayarları"
    
    def __str__(self):
        return self.site_name