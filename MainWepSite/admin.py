from django.contrib import admin
from .models import Product, Category, Brand, ProductImage, Wishlist, \
    Review, Comment, Cart, CartItem, ProductViewLog, ProductPurchaseLog, ProductSize, Color, Size
from MainWepSite.models import BlogPost, Tag, BlogComment


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['value']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name']
@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'size_price', 'size_sku', 'product_number', 'package_type']
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock_quantity', 'category', 'brand',)
    search_fields = ('name', 'sku', 'category__name', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'brand')  # новое поле
    readonly_fields = ('sales_count', 'rating')  # новое поле


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}



from django.contrib import admin
from .models import BlogPost, BlogPostImage, BlogPostCategory, Tag, BlogComment

class BlogPostImageInline(admin.TabularInline):
    model = BlogPostImage
    extra = 1  # Number of extra forms to display

class BlogPostAdmin(admin.ModelAdmin):
    inlines = [BlogPostImageInline, ]
    list_display = ('title', 'author', 'created_at', 'updated_at', 'published')
    search_fields = ('title', 'content', 'author__username', 'b_category__name', 'tags__name')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('published', 'created_at', 'updated_at', 'tags', 'b_category')
    date_hierarchy = 'created_at'

class BlogPostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('post__title', 'author__customer_name', 'content')
    list_filter = ('created_at', 'post')

# Регистрация моделей и их админ-классов
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogPostCategory, BlogPostCategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductImage)
admin.site.register(Wishlist)

admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ProductViewLog)
admin.site.register(ProductPurchaseLog)

