from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserRegisterView, UserProfileView,
    ArticleListView, ArticleDetailView, FeaturedArticlesView, HotNewsView,
    CategoryListView, TagListView,
    CommentListView,
    ReactionView,
    BookmarkListView, BookmarkDetailView,
    NewsletterSubscriptionView,
    SiteSettingsView,
    PasswordResetRequestView, 
    PasswordResetConfirmView, 
    ChangePasswordView,
    CategoryArticleListView,
    TagArticleListView,
    UpdateUsernameView
)
from .views import api_root


urlpatterns = [
    
    path('', api_root, name='api-root'),

    # Auth
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/login/', obtain_auth_token, name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/change-username/', UpdateUsernameView.as_view(), name='change-username'),


    
    # Articles
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/featured/', FeaturedArticlesView.as_view(), name='featured-articles'),
    path('articles/hot/', HotNewsView.as_view(), name='hot-news'),
    
    # Categories & Tags
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/articles/', CategoryArticleListView.as_view(), name='category-article-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/articles/', TagArticleListView.as_view(), name='tag-article-list'),
    # Comments
    path('articles/<slug:slug>/comments/', CommentListView.as_view(), name='comment-list'),
    
    # Reactions
    path('reactions/', ReactionView.as_view(), name='reaction'),
    
    # Bookmarks
    path('bookmarks/', BookmarkListView.as_view(), name='bookmark-list'),
    path('bookmarks/<int:article_id>/', BookmarkDetailView.as_view(), name='bookmark-detail'),
    
    # Newsletter
    path('newsletter/', NewsletterSubscriptionView.as_view(), name='newsletter'),
    
    # Site Settings
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
]