from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

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
    SiteSettingsSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    ChangePasswordSerializer
)

# API Root
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'auth': {
            'register': reverse('register', request=request, format=format),
            'login': reverse('login', request=request, format=format),
            'profile': reverse('profile', request=request, format=format),
            'password_reset': reverse('password-reset-request', request=request, format=format),
            'password_change': reverse('change-password', request=request, format=format),
            'username_update': reverse('change-username', request=request, format=format), 
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

# Password Reset Views
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = f"http://frontend-url.com/reset-password/{uid}/{token}/"

            send_mail(
                subject="Şifre Sıfırlama",
                message=f"Şifrenizi sıfırlamak için bağlantı: {reset_url}",
                from_email="noreply@example.com",
                recipient_list=[user.email]
            )
        except User.DoesNotExist:
            pass

        return Response({'detail': 'Eğer e-posta kayıtlıysa şifre sıfırlama bağlantısı gönderildi.'})

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = smart_str(urlsafe_base64_decode(serializer.validated_data['uidb64']))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'error': 'Geçersiz bağlantı.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, serializer.validated_data['token']):
            return Response({'error': 'Token geçersiz veya süresi dolmuş.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Şifreniz başarıyla sıfırlandı.'})

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": ["Yanlış eski şifre."]}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"detail": "Şifre başarıyla değiştirildi."})

class UpdateUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        new_username = request.data.get('username')

        if not new_username:
            return Response({'error': 'Yeni istifadəçi adı tələb olunur.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            return Response({'error': 'Bu istifadəçi adı artıq istifadə olunur.'}, status=status.HTTP_400_BAD_REQUEST)

        user.username = new_username
        user.save()
        return Response({'detail': 'İstifadəçi adı uğurla yeniləndi.', 'username': user.username})

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
    
class CategoryArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            category = Category.objects.filter(slug__iexact=search_query).first()
            if category:
                return Article.objects.filter(category=category, status='published')
        return Article.objects.none()

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            tag = Tag.objects.filter(
                Q(slug__iexact=search_query) | Q(name__icontains=search_query)
            ).first()
            if tag:
                return Article.objects.filter(tags=tag, status='published')
        return Article.objects.none()
        
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
