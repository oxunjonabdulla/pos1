import json

from django.contrib.auth.decorators import login_required
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


@login_required(login_url="login_page")
def user_tutorial_page(request):
    if request.user.is_superuser:
        return redirect("admin_tutor")
    today = timezone.now().date()
    orders = Order.objects.filter(created_at__date=today, foydalanuvchi=request.user)
    return render(request=request,
                  template_name="user/tutor/tutorial.html",
                  context={"today_orders": orders.filter(status__in=['2', '3'])})


@login_required(login_url="login_page")
def admin_tutorial_page(request):
    today = timezone.now().date()

    if request.user.is_superuser:
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
        else:
            orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        orders_1_count = orders.filter(status='1').count()
        orders_2_count = orders.filter(status='2').count()
        orders_3_count = orders.filter(status='3').count()

        user_ctx = {
            "orders_1_count": orders_1_count,
            "orders_2_count": orders_2_count,
            "orders_3_count": orders_3_count,
            "today_orders": orders.filter(created_at__date=today, status='1'),
        }

        return render(
            request=request,
            template_name="user/tutor/admin-tutor.html",
            context=user_ctx,
        )
    else:
        return redirect("tutorial_page")
