"""
Сериализаторы для REST API
"""

from rest_framework import serializers
from .models import User, Master, Category, Product, Order, OrderItem, Cart, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'created_at']
        read_only_fields = ['id', 'created_at']


class MasterSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Master
        fields = ['id', 'user', 'user_name', 'username', 'specialty', 'description', 'avatar', 'rating', 'created_at']
        read_only_fields = ['id', 'rating', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'products_count']
        read_only_fields = ['id']


class ProductListSerializer(serializers.ModelSerializer):
    master_name = serializers.CharField(source='master.user.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'quantity', 'in_stock',
            'image', 'category', 'category_name', 'master', 'master_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'quantity', 'in_stock',
            'image', 'category', 'master', 'is_active', 'created_at', 'updated_at',
            'reviews', 'average_rating'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_reviews(self, obj):
        reviews = obj.reviews.all()[:5]
        return ReviewSerializer(reviews, many=True).data
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 2)
        return 0


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'total_price', 'status',
            'delivery_address', 'comment', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_price', 'created_at', 'updated_at']


class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    in_stock = serializers.BooleanField(source='product.in_stock', read_only=True)
    
    class Meta:
        model = Cart
        fields = [
            'id', 'product', 'product_name', 'product_price', 'product_image',
            'quantity', 'subtotal', 'in_stock', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
