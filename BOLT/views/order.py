import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _  # Import for translation
from django.views.decorators.csrf import csrf_exempt

from product_app.models import Maxsulot, CartItems, Order, OrderItems
from settings_app.models import AdminParol, SectionChoices


@login_required(login_url="login_page")
def orders_page(request):
    if request.user.is_superuser:
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
        else:
            orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1
        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today, status='1')
        # Add pagination
        paginator = Paginator(orders, 10)  # Show 10 orders per page
        page_number = request.GET.get('page', 1)
        try:
            paginated_orders = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_orders = paginator.page(1)
        except EmptyPage:
            paginated_orders = paginator.page(paginator.num_pages)

        orders_1_count = orders.filter(status='1').count()
        orders_2_count = orders.filter(status='2').count()
        orders_3_count = orders.filter(status='3').count()
        orders_4_count = orders.filter(status='4').count()

        user_ctx = {
            "order_id": order_id,
            "user_orders": paginated_orders,  # Use paginated orders here
            "orders_1_count": orders_1_count,
            "orders_2_count": orders_2_count,
            "orders_3_count": orders_3_count,
            "orders_4_count": orders_4_count,
            "today_orders": today_orders,
        }
        return render(request, 'user/order/orders.html', user_ctx)

    elif request.user.is_staff:
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1
        user_orders = Order.objects.filter(foydalanuvchi=request.user)
        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today, foydalanuvchi=request.user)
        # Add pagination
        paginator = Paginator(user_orders, 10)  # Show 10 orders per page
        page_number = request.GET.get('page', 1)
        try:
            paginated_orders = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_orders = paginator.page(1)
        except EmptyPage:
            paginated_orders = paginator.page(paginator.num_pages)

        orders_1_count = user_orders.filter(status='1').count()
        orders_2_count = user_orders.filter(status='2').count()
        orders_3_count = user_orders.filter(status='3').count()
        orders_4_count = user_orders.filter(status='4').count()

        user_ctx = {
            "order_id": order_id,
            "user_orders": paginated_orders,  # Use paginated orders here
            "orders_1_count": orders_1_count,
            "orders_2_count": orders_2_count,
            "orders_3_count": orders_3_count,
            "orders_4_count": orders_4_count,
            "today_orders": today_orders.filter(status__in=['2', '3']),
        }
        return render(request, 'user/order/orders.html', user_ctx)


@login_required(login_url='login_page')
def search_orders(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '').strip()
        page_number = request.GET.get('page', 1)

        # Map readable statuses to their keys
        status_mapping = {
            'Buyurtma berildi': '1',
            'Bajarildi': '2',
            'Bekor qilindi': '3',
            'Qabul qilindi': '4'
        }

        # Find matching status keys for partial matches
        matching_status_keys = [
            key for name, key in status_mapping.items()
            if query.lower() in name.lower()
        ]

        # Adjust order filtering based on user type
        if request.user.is_superuser:
            if request.user.username == "sklad":
                orders_query = Order.objects.filter(kimga="2")
            else:
                orders_query = Order.objects.filter(Q(kimga="1") | Q(kimga=None))
        else:
            # Regular users can view only their own orders
            orders_query = Order.objects.filter(foydalanuvchi=request.user)

        # Apply search filters
        filtered_orders = orders_query.filter(
            Q(id__icontains=query) |
            Q(maxsulotlar__maxsulot__nomi__icontains=query) |
            Q(status__in=matching_status_keys)  # Match status keys for partial matches
        ).distinct() if query else orders_query

        # Paginate results
        paginator = Paginator(filtered_orders, 10)
        try:
            paginated_orders = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_orders = paginator.page(1)
        except EmptyPage:
            paginated_orders = paginator.page(paginator.num_pages)

        # Render the table and pagination HTML
        html_table = render_to_string('user/partials/order_list.html', {
            'user_orders': paginated_orders,
            'query': query  # Pass query to template for pagination links
        }, request=request)

        html_pagination = render_to_string('user/partials/pagination.html', {
            'user_orders': paginated_orders,
            'query': query
        }, request=request)

        return JsonResponse({'html_table': html_table, 'html_pagination': html_pagination})

    return JsonResponse({'error': _("Noto'g'ri so'rov usuli.")}, status=400)


@csrf_exempt
def approve_order(request, pk):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=pk)

        if request.method == "POST":
            try:
                data = json.loads(request.body)
                password = data.get("password")

                user = authenticate(username=request.user.username, password=password)
                if user is None:
                    return JsonResponse({"success": False, "message": _("Noto'g'ri parol!")})

                order.status = '4'  # "Qabul qilindi"
                order.save()
                return JsonResponse({"success": True, "message": _("Buyurtma qabul qilindi!")})
            except Exception as e:
                return JsonResponse({"success": False, "message": _("Xatolik yuz berdi!")})

        return JsonResponse({"success": False, "message": _("Noto'g'ri so'rov usuli.")})

    return JsonResponse({"success": False, "message": _("Ruxsat berilmagan.")})

@csrf_exempt
@login_required
def submit_order(request, pk):
    if not request.user.is_superuser:
        return JsonResponse({"success": False, "message": _("Ruxsat berilmagan.")}, status=403)

    # Determine the section based on the admin's username
    section = SectionChoices.WAREHOUSE if request.user.username == "sklad" else SectionChoices.MECHANICS

    order = get_object_or_404(Order, id=pk)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            password = data.get("password")

            # Validate password
            if not password.isdigit():
                return JsonResponse({"success": False, "message": _("Noto'g'ri parol!")}, status=400)

            password = int(password)

            # Retrieve the latest password for the section
            parol = AdminParol.objects.filter(section=section).last()
            if not parol or password != int(parol.parol):
                return JsonResponse({"success": False, "message": _("Noto'g'ri parol!")}, status=400)

            # Check if stock is available for each product
            order_items = order.maxsulotlar.all()
            if request.user.username == "sklad":
                for item in order_items:
                    product = item.maxsulot
                    if product.count < item.soni:
                        return JsonResponse({
                            "success": False,
                            "message": _(f"{product.nomi} yetarli emas! Omborda {product.count} ta bor."),
                        }, status=400)

                # Deduct stock
                for item in order_items:
                    product = item.maxsulot
                    product.count -= item.soni
                    product.save()

            # Update order status
            order.status = '2'  # Completed
            order.save()

            return JsonResponse({"success": True, "message": _("Buyurtma muvaffaqiyatli tasdiqlandi!")})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": _("Ma'lumotni qayta ishlashda xatolik yuz berdi.")}, status=400)

    return JsonResponse({"success": False, "message": _("Noto'g'ri so'rov usuli.")}, status=405)

@csrf_exempt
def cancel_order(request, pk):
    if request.user.is_superuser:
        # Determine the section based on the username
        if request.user.username == "sklad":
            section = SectionChoices.WAREHOUSE
        else:
            section = SectionChoices.MECHANICS

        # Get the order object
        order = get_object_or_404(Order, id=pk)

        if request.method == "POST":
            try:
                data = json.loads(request.body)
                password = data.get("password")
                reason = data.get("reason")

                # Validate the password as an integer
                try:
                    password = int(password)
                except (TypeError, ValueError):
                    return JsonResponse({"success": False, "message": _("Noto'g'ri parol!")})

                # Retrieve the latest password for the specified section
                parol = AdminParol.objects.filter(section=section).last()

                if parol and password == int(parol.parol):  # Validate password
                    if reason:  # Ensure a cancellation reason is provided
                        order.status = '3'  # Mark order as canceled
                        order.bekor_qilish_sababi = reason  # Save cancellation reason
                        order.save()
                        return JsonResponse({"success": True})
                    else:
                        return JsonResponse({"success": False, "message": _("Bekor qilish sababi talab qilinadi!")})
                else:
                    return JsonResponse({"success": False, "message": _("Noto'g'ri parol!")})

            except json.JSONDecodeError:
                return JsonResponse({"success": False, "message": _("Xatolik yuz berdi.")})

        return JsonResponse({"success": False, "message": _("Noto'g'ri so'rov usuli.")})

    return JsonResponse({"success": False, "message": _("Ruxsat berilmagan.")})


@login_required(login_url='login_page')
def order1_details(request, pk):
    if not request.user.is_superuser:
        return redirect('mechanic_page')

    if request.user.is_superuser:
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
        else:
            orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        # Filter today's orders with status '1'
        today_orders = orders.filter(created_at__date=timezone.now().date(), status='1')

        # Get the specific order or return 404
        order = get_object_or_404(Order, id=pk)

        context = {
            'order': order,
            'today_orders': today_orders
        }

        return render(request, 'user/order/order-details.html', context)

    else:
        return redirect('dashboard1')


@login_required(login_url="login_page")
def user_order_details(request, pk):
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today, foydalanuvchi=request.user)
    if request.user.is_superuser:
        return redirect('dashboard1')
    if request.user.is_staff:
        order = get_object_or_404(Order, id=pk)
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1

        user_ctx = {

            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
            'order': order,
            'today_orders': today_orders.filter(status__in=['2', '3'])
        }

        return render(request, 'user/order/user-order-detail.html', user_ctx)


@csrf_exempt
def admin_order_details(request, pk):
    today = timezone.now().date()
    today_orders = Order.objects.filter(updated_at__date=today, foydalanuvchi=request.user)
    if not request.user.is_superuser:
        return redirect('mechanic_page')
    if request.user.is_superuser and request.user.username != "sklad":
        order = get_object_or_404(Order, id=pk)
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1

        user_ctx = {

            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
            'order': order,
            'today_orders': today_orders.filter(status__in=['2', '3'])
        }
        return render(request, 'user/order/admin-order-detail.html', user_ctx)


@login_required(login_url='login_page')
def order_page(request):
    # Common data for both GET and POST requests

    maxsulotlar = Maxsulot.objects.all()
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
    cart_item_count = cart_items.count()
    order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1

    # Retrieve user orders and add pagination
    user_orders = Order.objects.filter(foydalanuvchi=request.user).order_by('-id')
    paginator = Paginator(user_orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page', 1)
    try:
        paginated_orders = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    # Count orders by status
    orders_1_count = user_orders.filter(status='1').count()
    orders_2_count = user_orders.filter(status='2').count()
    orders_3_count = user_orders.filter(status='3').count()

    user_ctx = {
        'maxsulotlar': maxsulotlar,
        'order_id': order_id,
        'cart_items': cart_items,
        'cart_item_count': cart_item_count,
        'user_orders': paginated_orders,
        'orders_1_count': orders_1_count,
        'orders_2_count': orders_2_count,
        'orders_3_count': orders_3_count,
    }

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            additional_text = data.get('additionalText', '').strip()
            to_field = data.get('toField', None)  # Retrieve the 'To' field from the POST data
            if not to_field:
                return JsonResponse({'success': False, 'message': _("Bo'lim tanlanmadi.")}, status=400)
            if to_field == "Mexanika bo'limi" or to_field == "Механический отдел":
                to_field = "1"
            elif to_field == "Omborxona" or to_field == "Склад":
                to_field = "2"
            if cart_items.exists():
                # Create the order instance
                order_instance = Order.objects.create(
                    foydalanuvchi=request.user,
                    jami_maxsulot=0,
                    status='1',
                    qoshimcha_matn=additional_text,
                    kimga=to_field  # Save the 'To' field
                )

                total_quantity = 0
                for item in cart_items:
                    maxsulot = OrderItems.objects.create(
                        maxsulot=item.maxsulot,
                        soni=item.soni,
                        foydalanuvchi=item.foydalanuvchi,
                    )
                    item.delete()  # Remove the item from the cart
                    total_quantity += maxsulot.soni
                    order_instance.maxsulotlar.add(maxsulot)

                order_instance.jami_maxsulot = total_quantity
                order_instance.save()

                return JsonResponse({'success': True, 'message': _("Buyurtma muvaffaqiyatli jo'natildi")}, status=200)

            return JsonResponse({'success': False, 'message': _("Savatda mahsulot mavjud emas.")}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': _("Noto'g'ri so'rov usuli.")}, status=400)

    return render(request, 'user/department/pos-mechanic.html', user_ctx)


@login_required(login_url="login_page")
def warehouse_orders(request):
    if not request.user.is_superuser:
        return redirect('mechanic_page')
    elif request.user.is_superuser:
        if request.user.username == "sklad":
            return redirect('dashboard1')
        else:
            order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1
            user_orders = Order.objects.filter(foydalanuvchi=request.user)
            today = timezone.now().date()
            today_orders = Order.objects.filter(
                updated_at__date=today,
                foydalanuvchi=request.user
            )
            # Add pagination
            paginator = Paginator(user_orders, 10)  # Show 10 orders per page
            page_number = request.GET.get('page', 1)
            try:
                paginated_orders = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_orders = paginator.page(1)
            except EmptyPage:
                paginated_orders = paginator.page(paginator.num_pages)

            orders_1_count = user_orders.filter(status='1').count()
            orders_2_count = user_orders.filter(status='2').count()
            orders_3_count = user_orders.filter(status='3').count()
            orders_4_count = user_orders.filter(status='4').count()

            user_ctx = {
                "order_id": order_id,
                "user_orders": paginated_orders,  # Use paginated orders here
                "orders_1_count": orders_1_count,
                "orders_2_count": orders_2_count,
                "orders_3_count": orders_3_count,
                "orders_4_count": orders_4_count,
                "today_orders": today_orders.filter(status__in=['2', '3']),
            }
            return render(request, 'user/order/admin-warehouse-orders.html', user_ctx)

    return render(request, 'user/order/admin-warehouse-orders.html')



@login_required(login_url="login_page")
def super_admin_orders(request):
    if request.user.is_superuser and request.user.username == "superadmin":

        orders = Order.objects.order_by("-created_at")
        paginator = Paginator(orders, 10)
        page_number = request.GET.get('page', 1)
        try:
            paginated_orders = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_orders = paginator.page(1)
        except EmptyPage:
            paginated_orders = paginator.page(paginator.num_pages)
        orders_1_count = orders.filter(status='1').count()
        orders_2_count = orders.filter(status='2').count()
        orders_3_count = orders.filter(status='3').count()
        orders_4_count = orders.filter(status='4').count()
        today_orders = Order.objects.filter(created_at__date=timezone.now().date(), status='1')
        return render(request,
                      'user/order/superadmin-orders.html',
                      {'user_orders': paginated_orders,
                       'orders_1_count': orders_1_count,
                       "orders_2_count": orders_2_count,
                       "orders_3_count": orders_3_count,
                       "orders_4_count": orders_4_count,
                       "today_orders": today_orders})
    return redirect("dashboard1")