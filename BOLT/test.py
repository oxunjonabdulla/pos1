import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from product_app.models import Maxsulot, CartItems, Order, OrderItems, Kategoriya, Department
from settings_app.models import SiteSettings, AdminParol
from user_app.models import User



@login_required(login_url='login_page')
def dashboard1_page(request):
    site_settings = SiteSettings.objects.last()
    today = timezone.now().date()

    if request.user.is_superuser:
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
        else:
            orders = Order.objects.all()

        # Add pagination for orders
        paginator = Paginator(orders, 10)  # Show 10 orders per page
        page_number = request.GET.get('page', 1)
        try:
            paginated_orders = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_orders = paginator.page(1)
        except EmptyPage:
            paginated_orders = paginator.page(paginator.num_pages)

        orders_1 = orders.filter(status='1')
        orders_2 = orders.filter(status='2')
        orders_3 = orders.filter(status='3')

        today_orders = orders.filter(created_at__date=today)
        today_orders_1 = today_orders.filter(status='1')
        today_orders_2 = today_orders.filter(status='2')

        users = User.objects.all()

        admin_ctx = {
            'site_settings': site_settings,
            'user_orders': paginated_orders,  # Use paginated orders here
            'top_orders': orders[:10],
            'orders_1': orders_1,
            'orders_2': orders_2,
            'orders_3': orders_3,
            'today_orders': today_orders,
            'today_orders_1': today_orders_1,
            'today_orders_2': today_orders_2,
            'users': users,
        }

        return render(request, 'user/dashboard.html', admin_ctx)

    elif request.user.is_staff:
        kategoriya = get_object_or_404(Kategoriya, id=1)
        maxsulotlar = Maxsulot.objects.filter(Q(kategoriya=kategoriya) | Q(kategoriya__isnull=True))
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1
        user_ctx = {
            'site_settings': site_settings,
            'maxsulotlar': maxsulotlar,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
        }

        return render(request, 'user-home.html', user_ctx)

    else:
        return redirect('login_page')




