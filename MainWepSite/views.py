from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from MainWepSite.models import BlogPost
from MainWepSite.forms import BlogPostForm  # Make sure you have a BlogPostForm in forms.py
from _decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Category, Brand, ProductSize, Size, ProductViewLog
from .models import ProductImage  # Импортируйте ваши модели
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from MainWepSite.models import Product, CartItem
from .models import ProductSize
from django.shortcuts import get_list_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Case, When, Value
from django.shortcuts import render, get_object_or_404, redirect
from MainWepSite.models import BlogPost, BlogComment
from MainWepSite.forms import BlogCommentForm
from django.views.generic import ListView
from .models import BlogPost


from django.shortcuts import render
from django.http import HttpResponseNotFound

def error_404_view(request, exception):
    """A custom view function for handling 404 errors."""
    return render(request, 'ForMainWepSite/error_page.html', {}, status=404)


def get_top_products(limit=12, name_length=20):
    # Сортируем продукты так, чтобы те, у которых display_order равен 0, шли в конце
    top_products = Product.objects.annotate(
        sort_order=Case(
            When(display_order=0, then=Value(9999)),
            default='display_order'
        )
    ).order_by('sort_order')[:limit]

    # Собираем детали продуктов
    top_products_details = []
    for product in top_products:
        # Проверяем, есть ли изображение у продукта
        if product.main_image:
            name = product.name
            if len(name) > name_length:
                name = name[:name_length] + '...'  # Обрезаем и добавляем многоточие

            top_products_details.append({
                'name': name,
                'main_image': product.main_image.url,
                'sales_count': product.sales_count,
                'rating': product.rating,
                'detail_url': f'/product/{product.slug}/'
            })

    return top_products_details









def get_top_selling_products(limit=6, name_length=25):
    top_products = Product.objects.order_by('-sales_count')[:limit]
    top_products_details = []

    for product in top_products:
        name = product.name
        if len(name) > name_length:
            name = name[:name_length] + '...'  # Обрезаем и добавляем многоточие

        top_products_details.append({
            'name': name,
            'main_image': product.main_image.url if product.main_image else None,
            'sales_count': product.sales_count,
            'rating': product.rating,
            'detail_url': f'/product/{product.slug}/'
        })

    return top_products_details



# Главная страница
# Главная страница
from django.db.models import Prefetch

def index(request):
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', None)
    brand_slug = request.GET.get('brand', None)
    filter_category = request.GET.get('filter_category', '0')
    filter_brand = request.GET.get('filter_brand', '0')

    # Фильтрация и поиск
    products = Product.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)
    if filter_category == '1' and category_slug:
        products = products.filter(category__slug=category_slug)
    if filter_brand == '1' and brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # Подготовка запроса для получения данных ProductSize
    product_size_prefetch = Prefetch('productsize_set', queryset=ProductSize.objects.all(), to_attr='sizes_info')
    products = products.prefetch_related(product_size_prefetch)

    # Пагинация
    paginator = Paginator(products, 5)  # Показывать по 5 продуктов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = Brand.objects.all()
    # Подсчет количества товаров в корзине
    cart = request.session.get('cart', {})
    total_items_in_cart = sum(item['quantity'] for item in cart.values())

    top_selling_products = get_top_selling_products()
    top_products = get_top_products()
    recent_posts = get_recent_posts()

    return render(request, 'ForMainWepSite/index.html', {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'top_selling_products': top_selling_products,
        'top_products': top_products,
        'recent_posts': recent_posts,  # Добавьте это
        'total_items_in_cart': total_items_in_cart,  # Добавьте это
    })





def view_cart(request, size=None):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    skus_to_remove = []  # list to hold skus that should be removed
    total_items_in_cart = sum(item['quantity'] for item in cart_items)

    for sku, item_data in list(cart.items()):
        try:
            product_id = item_data['product_id']
            product = Product.objects.get(id=product_id)

            # Используем SKU для получения объекта ProductSize
            product_size = ProductSize.objects.get(product=product, size_sku=sku)
            price = product_size.size_price
            sku_value = product_size.size_sku

            quantity = item_data['quantity']
            total_price += price * quantity

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'size': product_size.size.value,
                'total': price * quantity,
                'sku': sku_value,
                'product_number': item_data.get('product_number'),
                'package_type': item_data.get('package_type')
            })
        except Product.DoesNotExist:
            messages.warning(request, f"Product with SKU {sku} was removed or does not exist.")
            skus_to_remove.append(sku)
        except ProductSize.DoesNotExist:
            messages.warning(request, f"Product size with SKU {sku} not found for product {product.name}.")
            skus_to_remove.append(sku)

    for sku in skus_to_remove:  # Remove skus after iterating through the cart
        del cart[sku]

    request.session['cart'] = cart

    return render(request, 'ForMainWepSite/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items_in_cart': total_items_in_cart  # добавьте это
    })



def _add_product_to_session_cart(request, product_id, quantity, selected_package_type, selected_zeston, selected_sku, selected_size_desc):
    cart = request.session.get('cart', {})

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ValueError(f"Product with ID {product_id} does not exist.")

    try:
        # Формируем запрос с учетом возможного отсутствия selected_zeston
        product_size_query = ProductSize.objects.filter(
            product=product,
            package_type=selected_package_type,
            size_sku=selected_sku,
            size__value=selected_size_desc
        )
        if selected_zeston:
            product_size_query = product_size_query.filter(product_number=selected_zeston)

        product_size = product_size_query.get()
        price = product_size.size_price
    except ProductSize.DoesNotExist:
        raise ValueError("Combination of provided parameters does not exist.")
    except ProductSize.MultipleObjectsReturned:
        raise ValueError("Multiple product sizes found for the provided parameters.")

    # Обновление или добавление продукта в корзину
    cart_data = {
        'product_id': product_id,
        'quantity': cart.get(selected_sku, {}).get('quantity', 0) + quantity,
        'price': str(price),
        'sku': selected_sku,
        'product_number': product_size.product_number,  # Всегда добавляем product_number, если он доступен
        'package_type': selected_package_type,
        'zeston': selected_zeston,
        'size_desc': selected_size_desc
    }
    cart[selected_sku] = cart_data

    request.session['cart'] = cart







# Add product to cart
# Add product to cart
def add_to_cart(request, product_id):
    if request.method == "POST":
        action = request.POST.get('action')

        try:
            product = get_object_or_404(Product, id=product_id)
            quantity = int(request.POST.get('quantity', 1))
            selected_size_desc = request.POST.get('size_desc')
            selected_package_type = request.POST.get('packageType')
            selected_sku = request.POST.get('size_sku')
            selected_zeston = request.POST.get('zeston') or None  # Установите None, если zeston пустой

            # Формируем запрос с учетом возможного отсутствия selected_zeston
            product_size_query = ProductSize.objects.filter(
                product=product,
                package_type=selected_package_type,
                size_sku=selected_sku,
                size__value=selected_size_desc
            )

            if selected_zeston:
                product_size_query = product_size_query.filter(product_number=selected_zeston)

            product_size = product_size_query.get()

            _add_product_to_session_cart(request, product.id, quantity, selected_package_type, selected_zeston,
                                         selected_sku, selected_size_desc)

            if action == 'add_to_cart':
                # Перенаправление на главную страницу после добавления в корзину
                return redirect('MainWepSite:index')
            elif action == 'buy_now':
                # Перенаправление на страницу оформления заказа
                return redirect('orders:save_order_details')

        except ProductSize.MultipleObjectsReturned:
            messages.error(request, "Multiple matching product sizes found. Please contact support.")
            return redirect('MainWepSite:index')
        except ProductSize.DoesNotExist:
            messages.error(request, "Selected product size or SKU combination does not exist.")
            return redirect('MainWepSite:product_detail', product.slug)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('MainWepSite:index')
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('MainWepSite:index')
    else:
        messages.warning(request, "Invalid request type.")
        return redirect('MainWepSite:index')

def remove_from_cart(request, sku):
    cart = request.session.get('cart', {})
    sku_str = str(sku)


    if sku_str in cart:
        del cart[sku_str]
        print(f"Updated cart after removal: {cart}")

        request.session['cart'] = cart
        messages.success(request, f"Product with SKU {sku_str} successfully removed from cart.")
    else:
        messages.error(request, f"Product with SKU {sku_str} not found in cart. Current cart items: {list(cart.keys())}")

    return redirect('MainWepSite:view_cart')



def update_cart_quantity(request, sku):
    # print(f"SKU: {sku}")
    if request.method == "POST":
        cart = request.session.get('cart', {})

        try:
            # Получаем новое количество товаров из POST-запроса
            new_quantity = int(request.POST.get('quantity', 1))

            # Если sku не существует в корзине, выводим сообщение об ошибке
            sku_str = str(sku)
            if sku_str not in cart:
                messages.error(request, "Product not found in cart.")
                return redirect('MainWepSite:view_cart')

            # Проверяем, что количество товаров больше нуля
            if new_quantity <= 0:
                messages.error(request, "Quantity must be greater than zero.")
                return redirect('MainWepSite:view_cart')

            # Обновляем количество товаров в корзине
            cart[sku_str]['quantity'] = new_quantity


            # Обновляем состояние корзины в сессии
            request.session['cart'] = cart
            print(f"Cart after updating quantity: {cart}")


            # Выводим сообщение об успешном обновлении количества товаров
            messages.success(request, "Quantity updated successfully.")

        except ValueError:
            # Если введено неверное количество товаров (например, не целое число),
            # выводим сообщение об ошибке
            messages.error(request, "Invalid quantity.")


    return redirect('MainWepSite:view_cart')



def clear_cart(request):
    # Очистка корзины в сессии
    request.session['cart'] = {}
    messages.success(request, "Корзина была успешно очищена.")
    return redirect('MainWepSite:view_cart')




from django.utils import timezone

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    main_image = product.main_image
    additional_images = product.images.all()
    product_sizes = ProductSize.objects.filter(product=product)
    unique_package_types = ProductSize.objects.filter(product=product).values_list('package_type', flat=True).distinct()
    # Подсчет количества товаров в корзине
    cart = request.session.get('cart', {})
    total_items_in_cart = sum(item['quantity'] for item in cart.values())

    # Запись просмотра продукта
    if request.user.is_authenticated:
        ProductViewLog.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={'timestamp': timezone.now()}
        )
        # Получение недавних просмотров
        recent_views = get_recent_views_with_details(request.user, limit=10)
    else:
        recent_views = []

    context = {
        'product': product,
        'main_image': main_image,
        'additional_images': additional_images,
        'product_sizes': product_sizes,
        'unique_package_types': unique_package_types,
        'recent_views': recent_views,
        'total_items_in_cart': total_items_in_cart,  # Добавьте это
    }

    return render(request, 'ForMainWepSite/product_detail.html', context)


def get_recent_views_with_details(user, limit=10):
    recent_views = ProductViewLog.objects.filter(user=user).order_by('-timestamp')

    # Фильтрация уникальных продуктов с использованием Python
    unique_products = set()
    unique_views = []
    for view in recent_views:
        if view.product.id not in unique_products:
            unique_products.add(view.product.id)
            unique_views.append(view)
            if len(unique_views) >= limit:
                break

    products_details = [{
        'name': view.product.name,
        'main_image': view.product.main_image.url if view.product.main_image else None,
        'detail_url': f'/product/{view.product.slug}/'
    } for view in unique_views]
    return products_details


def recent_views(request):
    user = request.user
    print("Current user:", user)  # Для отладки
    if user.is_authenticated:
        recent_views = get_recent_views_with_details(user, limit=10)
        print("Recent views:", recent_views)  # Для отладки
        return render(request, 'ForMainWepSite/recent_views.html', {'recent_views': recent_views})
    else:
        return render(request, 'ForMainWepSite/recent_views.html', {'recent_views': []})



def recommend_products_based_on_views(user):
    viewed_products = ProductViewLog.objects.filter(user=user).values_list('product', flat=True)

    viewed_categories = Product.objects.filter(id__in=viewed_products).values_list('category', flat=True)

    recommended_products = Product.objects.filter(category__in=viewed_categories).exclude(id__in=viewed_products)[:10]

    recommended_products_details = [{
        'name': product.name,
        'main_image': product.main_image.url if product.main_image else None,
        'detail_url': f'/product/{product.slug}/'
    } for product in recommended_products]


    return recommended_products_details














from django.shortcuts import get_object_or_404

def update_based_on_package(request, product_id, package_type):
    sizes_p = ProductSize.objects.filter(product_id=product_id, package_type=package_type).distinct()


    sizes_data = [
        {
            "id": size.size.id,
            "value": size.size.value,
            "price": size.size_price,
            "sku": size.size_sku,
            "product_number": size.product_number,
            "package_type": size.package_type
        }
        for size in sizes_p
    ]
    return JsonResponse(sizes_data, safe=False)





def update_based_on_product_number(request, product_id, zeston,  package_type):
    sizes_n = ProductSize.objects.filter(product_id=product_id, product_number=zeston, package_type=package_type)
    sizes_data = [
        {
            "id": size.size.id,
            "value": size.size.value,
            "price": size.size_price,
            "sku": size.size_sku,
            "product_number": size.product_number,
            "package_type": size.package_type,
            "image_url": size.size.image.url if size.size.image else None
        }
        for size in sizes_n
    ]
    return JsonResponse(sizes_data, safe=False)

def update_based_on_sku(request, product_id, size_sku):
    sizes_s = ProductSize.objects.filter(product_id=product_id, size_sku=size_sku)
    sizes_data = [
        {
            "id": size.size.id,
            "value": size.size.value,
            "price": size.size_price,
            "sku": size.size_sku,
            "product_number": size.product_number,
            "package_type": size.package_type,
            "image_url": size.size.image.url if size.size.image else None
        }
        for size in sizes_s
    ]
    return JsonResponse(sizes_data, safe=False)


def update_based_on_size_and_package(request, product_id, size_desc, package_type):
    try:
        sizes = ProductSize.objects.filter(product_id=product_id, size__value=size_desc, package_type=package_type)
        sizes_data = [
            {
                "id": size.size.id,
                "value": size.size.value,
                "price": size.size_price,
                "sku": size.size_sku,
                "product_number": size.product_number,
                "package_type": size.package_type,

                "image_url": size.size.image.url if size.size.image else None
            }
            for size in sizes
        ]

    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse(sizes_data, safe=False)


















# Страница категории
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'ForMainWepSite/category_detail.html', {'category.html': category, 'products': products})

# Страница бренда
def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand)
    return render(request, 'ForMainWepSite/brand_detail.html', {'brand': brand, 'products': products})









# @login_required
# def take_order_by_operational_manager(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     employee = request.user.mainofficeemployee
#     if isinstance(employee, OperationalManager) and order.operational_manager is None:
#         order.operational_manager = employee
#         order.save()
#         messages.success(request, "Заказ успешно взят!")
#     else:
#         messages.warning(request, "Заказ уже взят другим менеджером или вы не являетесь операционным менеджером.")
#     return redirect('orders:operator_order_list')  # замените на ваш URL
#
#


from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import BlogPost, BlogPostCategory
from django.db.models import Q
from django.db.models import Q

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'ForMainWepSite/blog/blog_list.html'  # Specify your template here
    context_object_name = 'posts'
    paginate_by = 12  # Optional: if you want pagination
    ordering = ['-created_at']  # Order by creation date, newest first

    def get_queryset(self):
        queryset = super().get_queryset().annotate(comment_count=Count('comments'))

        # Получение списка категорий из параметров запроса
        category_slugs = self.request.GET.getlist('b_category')
        if category_slugs:
            queryset = queryset.filter(b_category__slug__in=category_slugs)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogPostCategory.objects.all()
        return context




from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogCommentForm

def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    # Get previous and next posts
    previous_post = BlogPost.objects.filter(created_at__lt=post.created_at).order_by('-created_at').first()
    next_post = BlogPost.objects.filter(created_at__gt=post.created_at).order_by('created_at').first()

    comments_list = post.comments.all()
    paginator = Paginator(comments_list, 3)  # Show 3 comments per page
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    recent_posts = get_recent_posts()



    if request.method == 'POST':
        comment_form = BlogCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post  # Ensure the post is set here
            if hasattr(request.user, 'client'):
                comment.author = request.user.client
            else:
                # Handle the case where the user is not a Client
                # For example, redirect to an error page or show a message
                # return redirect('some_error_page')  # Replace with your error handling
                pass
            comment.save()
            return redirect('MainWepSite:blog_detail', slug=post.slug)
    else:
        comment_form = BlogCommentForm()

    return render(request, 'ForMainWepSite/blog/blog_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'previous_post': previous_post,
        'next_post': next_post,
        'recent_posts': recent_posts,  # Добавьте это
    })



from .models import BlogPost

def get_recent_posts(count=3):
    return BlogPost.objects.all().order_by('-created_at')[:count]







from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import BlogPostForm, BlogPostImageFormSet

class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'ForMainWepSite/blog/blog_form.html'
    success_url = reverse_lazy('MainWepSite:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = BlogPostImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = BlogPostImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid() and form.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return self.form_invalid(form)



from django.views.generic.edit import UpdateView

from django.views.generic.edit import UpdateView

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'ForMainWepSite/blog/blog_form.html'
    success_url = reverse_lazy('MainWepSite:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = BlogPostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = BlogPostImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.tags.set(form.cleaned_data['tags'])  # Обновление тегов
        formset = BlogPostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid():
            formset.save()
        else:
            return self.form_invalid(form)
        return response




class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'ForMainWepSite/blog/blog_confirm_delete.html'
    success_url = reverse_lazy('MainWepSite:blog_list')


from django.views.generic import ListView
from .models import BlogComment

class CommentListView(ListView):
    model = BlogComment
    template_name = 'ForMainWepSite/blog/comment_list.html'  # Specify your template here
    context_object_name = 'comments'
    paginate_by = 10  # Optional: if you want pagination



from django.views.generic import DeleteView
from .models import BlogComment

from django.urls import reverse_lazy

class CommentDeleteView(DeleteView):
    model = BlogComment
    template_name = 'ForMainWepSite/blog/comment_confirm_delete.html'



    def get_success_url(self):
        post = self.object.post
        return reverse_lazy('MainWepSite:blog_detail', kwargs={'slug': post.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_slug'] = self.object.post.slug  # Assuming `post` is the related blog post
        return context





