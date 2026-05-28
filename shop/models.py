from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    ROLE_CHOICES = [
        ('buyer',  'Покупатель'),
        ('master', 'Мастер'),
    ]
    role  = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer', verbose_name='Роль')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Master(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master_profile', verbose_name='Пользователь')
    specialty   = models.CharField(max_length=100, verbose_name='Специализация')
    description = models.TextField(blank=True, verbose_name='Описание')
    avatar      = models.ImageField(upload_to='masters/', blank=True, null=True, verbose_name='Фото')
    rating      = models.DecimalField(max_digits=3, decimal_places=2, default=0,
                                      validators=[MinValueValidator(0), MaxValueValidator(5)],
                                      verbose_name='Рейтинг')

    class Meta:
        db_table = 'masters'
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} — {self.specialty}'


class Product(models.Model):
    master      = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='products', verbose_name='Мастер')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name='Категория')
    name        = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price       = models.DecimalField(max_digits=10, decimal_places=2,
                                      validators=[MinValueValidator(1)], verbose_name='Цена')
    quantity    = models.PositiveIntegerField(default=0, verbose_name='Количество')
    image       = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Фото')
    is_active   = models.BooleanField(default=True, verbose_name='Активен')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.quantity > 0


class Order(models.Model):
    STATUS = [
        ('pending',    'Ожидает'),
        ('processing', 'Обрабатывается'),
        ('shipped',    'Отправлен'),
        ('delivered',  'Доставлен'),
        ('cancelled',  'Отменён'),
    ]
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Покупатель')
    total_price      = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    status           = models.CharField(max_length=20, choices=STATUS, default='pending', verbose_name='Статус')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    comment          = models.TextField(blank=True, verbose_name='Комментарий')
    created_at       = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} — {self.user.username}'


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price    = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    @property
    def subtotal(self):
        return self.price * self.quantity


class Cart(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Пользователь')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity   = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        unique_together = [['user', 'product']]

    def __str__(self):
        return f'{self.user.username} — {self.product.name}'

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Review(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating     = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    comment    = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = [['product', 'user']]

    def __str__(self):
        return f'{self.user.username} → {self.product.name} ({self.rating}★)'
