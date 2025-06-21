from rest_framework import serializers
from .models import (
    User, Article, Category, Tag,
    Comment, Reaction, Bookmark,
    NewsletterSubscription, SiteSettings
)

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'profile_picture', 'bio', 'role', 'verified']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'featured_image']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class ArticleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'excerpt', 'featured_image', 
                 'publish_date', 'category', 'tags', 'author', 'view_count']

class ArticleDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    author = UserProfileSerializer()
    
    class Meta:
        model = Article
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at', 'parent', 'replies']
    
    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        return CommentSerializer(replies, many=True).data

class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Reaction
        fields = ['id', 'reaction_type', 'user', 'created_at']

class BookmarkSerializer(serializers.ModelSerializer):
    article = ArticleListSerializer()
    
    class Meta:
        model = Bookmark
        fields = ['id', 'article', 'created_at']

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['email', 'preferences']

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'