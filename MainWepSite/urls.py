from django.urls import path
from . import views
from MainWepSite.views import BlogPostListView, blog_post_detail, BlogPostCreateView, BlogPostUpdateView, \
    BlogPostDeleteView, CommentListView, CommentDeleteView

app_name = 'MainWepSite'  # только если вы используете пространство имен
# handler404 = 'FrogInsulationManufacturersInc2.views.error_404_view'

urlpatterns = [
    path('', views.index, name='index'),  # Эта строка указывает, что корневой URL будет обрабатываться функцией index
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # path('api/get_product_by_sku/<str:sku>/', views.get_product_by_sku, name='get_product_by_sku'),
    path('error/', views.error_404_view, name='error_page'),

    path('update_based_on_package/<int:product_id>/<str:package_type>/', views.update_based_on_package, name='update_based_on_package'),
    path('update_based_on_product_number/<int:product_id>/<zeston>/<str:package_type>/', views.update_based_on_product_number, name='update_based_on_product_number'),
    path('update_based_on_sku/<int:product_id>/<str:size_sku>/', views.update_based_on_sku, name='update_based_on_sku'),
    path('update_based_on_size_and_package/<int:product_id>/<size_desc>/<str:package_type>/', views.update_based_on_size_and_package, name='update_based_on_size_and_package'),

    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),

    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/(?P<sku>[\w-]+)/\\Z', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/(?P<sku>[\w-]+)/\\Z', views.update_cart_quantity, name='update_cart_quantity'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),

    path('recent-views/', views.recent_views, name='recent-views'),  # URL для недавно просмотренных продуктов

    path('blog/', BlogPostListView.as_view(), name='post_list'),
    path('blog/category/<slug:category_slug>/', BlogPostListView.as_view(), name='post_list_by_category'),
    path('blog/<slug:slug>/', blog_post_detail, name='blog_detail'),
    path('blog_new/', BlogPostCreateView.as_view(), name='blog_new'),
    path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_delete'),

    path('blog_comments/<slug:slug>/', CommentListView.as_view(), name='comment_list'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),



]




