from django.contrib import admin
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import (
    User, Category, Tag, Article, Media,
    Comment, Reaction, Bookmark,
    TrendingArticle, HotNews,
    NewsletterSubscription, Notification,
    ArticleView, SearchQuery
)

# Custom User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

# Article Admin
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'publish_date', 'view_count')
    list_filter = ('status', 'category', 'is_featured', 'is_hot')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date',)
    
    # Optional: CKEditor interfeysi göstərmək üçün (əgər göstərilmirsə)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }

# Tüm modelleri kaydet
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Media)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Bookmark)
admin.site.register(TrendingArticle)
admin.site.register(HotNews)
admin.site.register(NewsletterSubscription)
admin.site.register(Notification)
admin.site.register(ArticleView)
admin.site.register(SearchQuery)
