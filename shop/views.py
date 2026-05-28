from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Product, Category, Master, Cart, Order, OrderItem, Review, User


# ───────────────────────────── ГЛАВНАЯ ─────────────────────────────
def index(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search = request.GET.get('search', '').strip()

    products = Product.objects.filter(is_active=True).select_related('master__user', 'category')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if search:
        products = products.filter(name__icontains=search)

    masters = Master.objects.select_related('user').all()

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()

    return render(request, 'shop/index.html', {
        'products':      products,
        'categories':    categories,
        'masters':       masters,
        'cart_count':    cart_count,
        'selected_cat':  category_slug,
        'search':        search,
    })


# ───────────────────────────── ДЕТАЛИ ТОВАРА ─────────────────────────────
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    reviews = Review.objects.filter(product=product).select_related('user')

    if request.method == 'POST' and request.user.is_authenticated:
        rating  = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        Review.objects.update_or_create(
            product=product, user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Отзыв сохранён!')
        return redirect('product_detail', product_id=product_id)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })


# ───────────────────────────── АВТОРИЗАЦИЯ ─────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name or user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль!')

    return render(request, 'shop/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username   = request.POST.get('username')
        email      = request.POST.get('email')
        password   = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        role       = request.POST.get('role', 'buyer')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует!')
        elif len(password) < 6:
            messages.error(request, 'Пароль должен быть не менее 6 символов!')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name, role=role
            )
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')

    return render(request, 'shop/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('index')


# ───────────────────────────── КОРЗИНА ─────────────────────────────
@login_required
def cart_view(request):
    items = Cart.objects.filter(user=request.user).select_related('product')
    total = sum(item.subtotal for item in items)
    return render(request, 'shop/cart.html', {'items': items, 'total': total})


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if product.quantity == 0:
        messages.error(request, 'Товар закончился!')
        return redirect('index')

    item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        if item.quantity < product.quantity:
            item.quantity += 1
            item.save()
            messages.success(request, f'Количество «{product.name}» увеличено.')
        else:
            messages.error(request, 'Больше нет в наличии!')
    else:
        messages.success(request, f'«{product.name}» добавлен в корзину!')

    return redirect('index')


@login_required
def cart_remove(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Товар удалён из корзины.')
    return redirect('cart')


# ───────────────────────────── ОФОРМЛЕНИЕ ЗАКАЗА ─────────────────────────────
@login_required
def checkout_view(request):
    items = Cart.objects.filter(user=request.user).select_related('product')
    if not items.exists():
        messages.error(request, 'Корзина пуста!')
        return redirect('cart')

    total = sum(item.subtotal for item in items)

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not address:
            messages.error(request, 'Укажите адрес доставки!')
            return render(request, 'shop/checkout.html', {'items': items, 'total': total})

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=total,
                delivery_address=address,
                comment=comment,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                # Уменьшаем остаток на складе
                item.product.quantity -= item.quantity
                item.product.save()

            items.delete()

        messages.success(request, f'Заказ №{order.id} оформлен! Спасибо за покупку.')
        return redirect('orders')

    return render(request, 'shop/checkout.html', {'items': items, 'total': total})


# ───────────────────────────── МОИ ЗАКАЗЫ ─────────────────────────────
@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'shop/orders.html', {'orders': orders})
