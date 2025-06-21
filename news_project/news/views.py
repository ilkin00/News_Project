from rest_framework import generics, permissions, status, filters
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from .models import (
    User, Article, Category, Tag, 
    Comment, Reaction, Bookmark,
    NewsletterSubscription, SiteSettings
)

from .serializers import (
    UserRegisterSerializer, UserProfileSerializer,
    ArticleListSerializer, ArticleDetailSerializer,
    CategorySerializer, TagSerializer,
    CommentSerializer, ReactionSerializer,
    BookmarkSerializer, NewsletterSubscriptionSerializer,
    SiteSettingsSerializer
)

# API Root
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'auth': {
            'register': reverse('register', request=request, format=format),
            'login': reverse('login', request=request, format=format),
            'profile': reverse('profile', request=request, format=format),
        },
        'articles': {
            'list': reverse('article-list', request=request, format=format),
            'detail': 'articles/<slug:slug>/',
            'featured': reverse('featured-articles', request=request, format=format),
            'hot': reverse('hot-news', request=request, format=format),
        },
        'categories': reverse('category-list', request=request, format=format),
        'tags': reverse('tag-list', request=request, format=format),
        'comments': 'articles/<slug:slug>/comments/',
        'reactions': reverse('reaction', request=request, format=format),
        'bookmarks': {
            'list': reverse('bookmark-list', request=request, format=format),
            'delete': 'bookmarks/<article_id>/'
        },
        'newsletter': reverse('newsletter', request=request, format=format),
        'settings': reverse('site-settings', request=request, format=format),
    })

# Auth Views
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# Article Views
class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')
    serializer_class = ArticleListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'tags', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['publish_date', 'view_count']
    ordering = ['-publish_date']

class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'
    
    def get_object(self):
        obj = super().get_object()
        obj.increment_view_count()
        return obj

class FeaturedArticlesView(generics.ListAPIView):
    queryset = Article.objects.filter(status='published', is_featured=True).order_by('-publish_date')[:5]
    serializer_class = ArticleListSerializer

class HotNewsView(generics.ListAPIView):
    queryset = Article.objects.filter(status='published', is_hot=True, hot_expiry__gte=timezone.now()).order_by('-publish_date')[:3]
    serializer_class = ArticleListSerializer

# Category & Tag Views
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# Comment Views
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        article_slug = self.kwargs['slug']
        return Comment.objects.filter(
            article__slug=article_slug,
            parent__isnull=True
        ).select_related('user')
    
    def perform_create(self, serializer):
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        serializer.save(user=self.request.user, article=article)

# Reaction Views
class ReactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        article_id = request.data.get('article')
        reaction_type = request.data.get('reaction_type')
        
        article = get_object_or_404(Article, pk=article_id)
        reaction, created = Reaction.objects.get_or_create(
            user=request.user,
            article=article,
            defaults={'reaction_type': reaction_type}
        )
        
        if not created:
            reaction.reaction_type = reaction_type
            reaction.save()
        
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Bookmark Views
class BookmarkListView(generics.ListCreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('article')
    
    def perform_create(self, serializer):
        article_id = self.request.data.get('article')
        article = get_object_or_404(Article, pk=article_id)
        serializer.save(user=self.request.user, article=article)

class BookmarkDetailView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'article_id'
    
    def get_object(self):
        return get_object_or_404(
            Bookmark,
            user=self.request.user,
            article_id=self.kwargs['article_id']
        )

# Newsletter Views
class NewsletterSubscriptionView(generics.CreateAPIView):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    permission_classes = [permissions.AllowAny]

# Site Settings View
class SiteSettingsView(generics.RetrieveAPIView):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    
    def get_object(self):
        return SiteSettings.objects.first()
