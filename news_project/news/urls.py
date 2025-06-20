from django.urls import path
from .views import NewsListAPIView, SiteSettingsAPIView, CategoryListAPIView, TagListAPIView, NewsDetailBySlugAPIView


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('news/', NewsListAPIView.as_view(), name='news-list'),
    path('settings/', SiteSettingsAPIView.as_view(), name='site-settings'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # token alma
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # token yenileme
    path('news/<slug:slug>/', NewsDetailBySlugAPIView.as_view(), name='news-detail-slug'),
]
