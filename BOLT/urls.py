from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from BOLT.views.cart import (
    add_to_cart,
    update_cart_quantity,
    get_cart_items,
    remove_cart_item,
    remove_all_cart,
)
from BOLT.views.main import (
    warehouse_page,
    mechanic_page,
    check_section,
    dashboard_page,
    search_products,
    filter_products,
    bad_request_view, products_page, set_language, admin_warehouse_page, add_product, get_product, update_product,
)
from BOLT.views.order import (
    search_orders,
    order1_details,
    submit_order,
    cancel_order,
    user_order_details,
    orders_page, order_page, approve_order, warehouse_orders, admin_order_details,
)
from BOLT.views.tutorial import user_tutorial_page, admin_tutorial_page

urlpatterns = [
    # Admin Routes
    path('admin/', admin.site.urls),

    # Authentication and User Management
    path('auth/', include('user_app.urls')),

    # Main Pages
    path('', dashboard_page, name='home_page'),  # Home page
    path('dashboard1/', dashboard_page, name='dashboard1'),
    path('warehouse/', warehouse_page, name='warehouse_page'),
    path('add-product/', add_product, name='add_product'),
    path('update-product/<int:product_id>/', update_product, name="update_product"),
    path('get-product/<int:product_id>/', get_product, name="get_product"),
    path("admin_warehouse_page/", admin_warehouse_page, name="admin_warehouse_page"),
    path('mechanic/', mechanic_page, name='mechanic_page'),
    path('check-section/', check_section, name='check_section'),

    path('products-page/', products_page, name='products_page'),

    # Search and Filter
    path('warehouse/search-products/', search_products, name='warehouse_search_products'),
    path('mechanic/search-products/', search_products, name='mechanic_search_products'),

    path('search-products/', search_products, name='search_products'),
    path('filter-products/', filter_products, name='filter_products'),
    path('search-orders/', search_orders, name='search_orders'),

    # Order Management
    path('order1-detail/<int:pk>/', order1_details, name='order1-detail'),
    path('submit-order/<int:pk>/', submit_order, name='submit_order'),
    path('approve-order/<int:pk>/', approve_order, name='approve-order'),
    path('cancel-order/<int:pk>/', cancel_order, name='cancel_order'),
    path('user_order_detail/<int:pk>/', user_order_details, name='user_order_details'),

    path('admin_order_details/<int:pk>/', admin_order_details, name='admin_order_details'),
    path('orders/', orders_page, name='orders_page'),
    path('warehouse_orders/', warehouse_orders, name='warehouse_orders'),
    path('order/', order_page, name='order_page'),

    # Cart Management
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart-quantity/<int:cart_item_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('get-cart-items/', get_cart_items, name='get_cart_items'),
    path('remove-cart-item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('remove-all-cart/', remove_all_cart, name='remove_all_cart'),

    # Tutorial Pages
    path('user-tutor/', user_tutorial_page, name='tutorial_page'),
    path('admin-tutor/', admin_tutorial_page, name='admin_tutor'),

    # Error Handling
    path('404/', bad_request_view, name='404'),

]

urlpatterns += [

    path('i18n/', include('django.conf.urls.i18n')),
    path("set_language/<str:language>", set_language, name="set-language"),

]
# Static and Media Files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Error Handlers
handler404 = 'BOLT.views.main.bad_request_view'
