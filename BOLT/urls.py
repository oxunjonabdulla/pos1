from django.contrib import admin
from django.urls import path, include

# Static settings
from django.conf import settings
from django.conf.urls.static import static

from .views import home_page, \
    add_to_cart, remove_all_cart, order_page, profile_page, \
    order_detail_page, superadmin_all_orders_page, \
    superadmin_orders_1_page, superadmin_orders_2_page, superadmin_orders_3_page, \
    superadmin_edit_order_page, superadmin_order_status_2, user_sklad, update_cart_quantity, \
    get_cart_items, remove_cart_item, warehouse_page, mechanic_page, bad_request_view, filter_products, search_products, \
    user_tutorial_page, admin_tutorial_page, order1_details, user_order_details, search_orders, \
    check_section, \
     submit_order, cancel_order, dashboard_page, orders_page

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('warehouse/', warehouse_page, name='warehouse_page'),
    path('mechanic/', mechanic_page, name='mechanic_page'),
    path('check-section/', check_section, name='check_section'),

    path("dashboard1/", dashboard_page  , name="dashboard1"),
    path('warehouse/search-products/', search_products, name='warehouse_search_products'),
    path('mechanic/search-products/', search_products, name='mechanic_search_products'),

    path('filter-products/', filter_products, name='filter_products'),
    path('search-products/', search_products, name='search_products'),
    path('search-orders/', search_orders, name='search_orders'),

    path("order1-detail/<int:pk>/", order1_details, name="order1-detail"),

    path('submit-order/<int:pk>/', submit_order, name='submit_order'),

    path('cancel-order/<int:pk>/', cancel_order, name='cancel_order'),

    path('user_order_detail/<int:pk>/', user_order_details, name='user_order_details'),
    path("user-tutor/", user_tutorial_page, name="tutorial_page"),
    path("admin-tutor/", admin_tutorial_page, name="admin_tutor"),
    path('auth/', include('user_app.urls')),
    path('404/', bad_request_view, name='404'),

    # Ui routes
    path('', dashboard_page, name='home_page'),
    path('sklad/', user_sklad, name='user_sklad'),

    # User
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart-quantity/<int:cart_item_id>/', update_cart_quantity, name='update_cart_quantity'),

    path('get-cart-items/', get_cart_items, name='get_cart_items'),

    path('remove-cart-item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),

    path('remove-all-cart/', remove_all_cart, name='remove_all_cart'),

    path('order/', order_page, name='order_page'),

    path("orders/", orders_page, name="orders_page"),

    path('kabinet/', profile_page, name='profile_page'),
    path('kabinet/order/<int:pk>/', order_detail_page, name='order_detail_page'),

    # Admin
    path('all-orders/', superadmin_all_orders_page, name='superadmin_all_orders_page'),
    path('buyurtma-berilganlar/', superadmin_orders_1_page, name='superadmin_orders_1_page'),
    path('yetkazib-berilganlar/', superadmin_orders_2_page, name='superadmin_orders_2_page'),
    path('bekor-qilinganlar/', superadmin_orders_3_page, name='superadmin_orders_3_page'),

    path('edit-order/<int:pk>/', superadmin_edit_order_page, name='superadmin_edit_order_page'),
    path('edit-order/success/<int:pk>/', superadmin_order_status_2, name='superadmin_order_status_2'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'BOLT.views.bad_request_view'
