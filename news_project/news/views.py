from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import News, SiteSettings, Category, Tag
from .serializers import NewsSerializer, SiteSettingsSerializer, CategorySerializer, TagSerializer
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import AllowAny  # import et
from rest_framework.generics import RetrieveAPIView
class NewsListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.GET.get('search', '')
        if query:
            queryset = News.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).order_by('-created_at')
        else:
            queryset = News.objects.all().order_by('-created_at')
        serializer = NewsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteSettingsAPIView(APIView):
    def get(self, request):
        settings = SiteSettings.objects.first()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class TagListAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
        
class NewsDetailBySlugAPIView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]  # public olsun