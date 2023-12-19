from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
import random
import string

from custom_users.models import Client
from orders.models import Order


# Модель для категории
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Модель для бренда
class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='brands/', null=True, blank=True)  # Добавлено поле для изображения

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name






class Size(models.Model):
    value = models.CharField(max_length=50)
    image = models.ImageField(upload_to='sizes/', null=True, blank=True)

    def __str__(self):
        return self.value


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Модель для товара
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sku = models.CharField(max_length=50, unique=True, null=True)  # Уникальный SKU
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Средний рейтинг
    sales_count = models.IntegerField(default=0)  # Количество проданных единиц
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    stock_quantity = models.IntegerField(null=True)
    main_image = models.ImageField(upload_to='products/main_images/', null=True,
                                   blank=True)  # Главное изображение продукта
    sizes = models.ManyToManyField(Size, through='ProductSize', blank=True)
    colors = models.ManyToManyField(Color, blank=True)  # Отношение многие ко многим с цветами
    display_order = models.IntegerField(default=0, blank=True)  # Новое поле для порядка отображения

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Проверка уникальности slug
            while Product.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
                self.slug = f"{slugify(self.name)}-{suffix}"

        super().save(*args, **kwargs)

    def get_related_products(self, limit=5):
        return Product.objects.filter(category=self.category) \
                   .exclude(id=self.id) \
                   .order_by('-rating', '-sales_count')[:limit]

    def __str__(self):
        return f"{self.sku} - {self.name}"

    @classmethod
    def search(cls, query):
        return cls.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        )

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')
    description = models.TextField(blank=True, null=True)  # Описание изображения
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('product', 'order')

    def save(self, *args, **kwargs):
        if not self.order:
            max_order = ProductImage.objects.filter(product=self.product).aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    size_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    size_sku = models.CharField(max_length=100, unique=True, null=True)  # Уникальный SKU для комбинации продукт-размер

    # Product number for this specific SKU.
    product_number = models.CharField(max_length=100, blank=True, null=True)

    # Packaging options: Boxed or Single
    BX = 'bx'
    EACH = 'each'
    ZERO = '-'
    PACKAGE_CHOICES = [
        (BX, 'bx'),
        (EACH, 'each'),
        (ZERO, '-')
    ]
    package_type = models.CharField(max_length=10, choices=PACKAGE_CHOICES, default=ZERO, null=True)


    def __str__(self):
        return f"{self.size_sku} - {self.product.name} ({self.size.value})"






class Wishlist(models.Model):
    user = models.OneToOneField('auth.User', related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')




# Модель для отзывов
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)  # новое поле
    author = models.CharField(max_length=100)
    email = models.EmailField()  # Убран уникальный индекс
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.author} for {self.product.name}"

# Модель для комментариев к отзывам
class Comment(models.Model):
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} for review #{self.review.id}"


# Модель для корзины
class Cart(models.Model):
    user = models.OneToOneField('auth.User', related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

# Модель для элемента в корзине
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def total_price(self):
        return self.product.price * self.quantity


class ProductViewLog(models.Model):
    user = models.ForeignKey('auth.User', related_name='viewed_products', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, related_name='views', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class ProductPurchaseLog(models.Model):
    user = models.ForeignKey('auth.User', related_name='purchased_products', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, related_name='purchases', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



from django.utils.text import slugify
from django.db.utils import IntegrityError

import time
import random

def create_unique_slug(instance, new_slug=None):
    slug = slugify(instance.title) if new_slug is None else new_slug
    qs = BlogPost.objects.filter(slug=slug)
    if qs.exists():
        new_slug = f"{slug}-{int(time.time())}-{random.randint(1, 1000)}"
        return create_unique_slug(instance, new_slug=new_slug)
    return slug


class BlogPostCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





class BlogPost(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    main_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', blank=True)
    b_category = models.ForeignKey(BlogPostCategory, related_name='blog_posts', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(self)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.title


class BlogPostImage(models.Model):
    post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    small_image = models.ImageField(upload_to='blog_images/small_images/')

    def __str__(self):
        return f"Image for {self.post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Client, on_delete=models.CASCADE)  # Linking to Client model
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.customer_name} on {self.post.title}"



