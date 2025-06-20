from django.contrib import admin
from .models import Category, Tag, News, NewsGalleryImage, SiteSettings

class NewsGalleryInline(admin.TabularInline):
    model = NewsGalleryImage
    extra = 1

class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsGalleryInline]
    list_display = ('title', 'slug', 'category', 'created_at', 'view_count')
    search_fields = ('title', 'slug')
    list_filter = ('category', 'tags')
    prepopulated_fields = {"slug": ("title",)}  # Admin'de slug otomatik dolsun


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(News, NewsAdmin)
admin.site.register(SiteSettings)
