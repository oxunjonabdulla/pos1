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
    return render(request=request,
                  template_name="user/tutorial.html")


@login_required(login_url="login_page")
def admin_tutorial_page(request):
    if request.user.is_superuser:
        today = timezone.now().date()
        if request.user.is_superuser:
            if request.user.username == "sklad":
                orders = Order.objects.filter(kimga="2")
            else:
                orders = Order.objects.all()

            orders_1_count = orders.filter(status='1').count()
            orders_2_count = orders.filter(status='2').count()
            orders_3_count = orders.filter(status='3').count()

            user_ctx = {
                "orders_1_count": orders_1_count,
                "orders_2_count": orders_2_count,
                "orders_3_count": orders_3_count,
                "today_orders": orders.filter(created_at__date=today, status='1')
            }
            return render(request=request,
                          template_name="user/admin-tutor.html",
                          context=user_ctx)
    else:
        return redirect("tutorial_page")


@login_required(login_url="login_page")
def orders_page(request):
    if request.user.is_superuser:
        return redirect("dashboard1")
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

    orders_1_count = Order.objects.filter(status='1').count()
    orders_2_count = Order.objects.filter(status='2').count()
    orders_3_count = Order.objects.filter(status='3').count()

    user_ctx = {
        "order_id": order_id,
        "user_orders": paginated_orders,  # Use paginated orders here
        "orders_1_count": orders_1_count,
        "orders_2_count": orders_2_count,
        "orders_3_count": orders_3_count,
        "today_orders": today_orders
    }
    return render(request, 'user/orders.html', user_ctx)


@login_required(login_url='login_page')
def check_section(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        target_section = data.get("section")

        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

        if cart_items.exists():
            current_section = cart_items.first().maxsulot.kategoriya.department.name
            if current_section != target_section:
                if current_section == "Warehouse":
                    current_section = "Omborxona"
                elif current_section == "Mechanic":
                    current_section = "Mexanika bo'limi"
                if target_section == "Warehouse":
                    target_section = "Omborxona"
                elif target_section == "Mechanic":
                    target_section = "Mexanika bo'limi"
                return JsonResponse({
                    "success": False,
                    "message": (
                        f"<span style='color: #007bff; font-weight: bold;'>{target_section}</span> "
                        "bo'limga o'tish uchun avval "
                        f"<span style='color: #dc3545; font-weight: bold;'>{current_section}</span> "
                        "savatidagi mahsulotlarni o'chiring yoki buyurtma bering."
                    )
                }, status=400)

        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Noto'g'ri so'rov turi"}, status=405)


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required(login_url='login_page')
def dashboard_page(request):
    today = timezone.now().date()

    if request.user.is_superuser:
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
        else:
            orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

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

        today_orders = orders.filter(created_at__date=today, status='1')
        today_orders_1 = today_orders.filter(status='1')
        today_orders_2 = today_orders.filter(status='2')

        users = User.objects.all()

        admin_ctx = {
            'user_orders': paginated_orders,
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
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today, foydalanuvchi=request.user)
        if cart_items.exists():
            current_section = cart_items.first().maxsulot.kategoriya.department.name
            if current_section != "Mechanic":
                return redirect("warehouse_page")
        departments = Department.objects.annotate(category_count=Count('kategoriya'))
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

        # Get the Mechanic department
        try:
            mechanic_department = Department.objects.get(name="Mechanic")
        except Department.DoesNotExist:
            return render(request, "user/error-404.html")  # Handle the case where the department doesn't exist

        department_id = mechanic_department.id
        categories = Kategoriya.objects.filter(department_id=department_id).annotate(maxsulot_count=Count('maxsulot'))
        products = Maxsulot.objects.filter(kategoriya__in=categories)
        return render(request, "user/pos-mechanic.html", {
            'departments': departments,
            'products': products,
            'cart_items': cart_items,
            'cart_items_count': cart_items.count(),
            'active_department': department_id,
            'categories': categories,
            'search_url': 'mechanic_search_products',
            'today_orders': today_orders.filter(status__in=['2', '3'])
        })

    else:
        return redirect('login_page')


@login_required(login_url='login_page')
def warehouse_page(request):
    if request.user.is_superuser:
        return redirect("dashboard1")
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today, foydalanuvchi=request.user)
    # Check if cart contains items from another section
    if cart_items.exists():
        current_section = cart_items.first().maxsulot.kategoriya.department.name
        if current_section != "Warehouse":
            return redirect("mechanic_page")
    # Annotate each department with the count of its related categories
    departments = Department.objects.annotate(category_count=Count('kategoriya'))
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

    # Get the Mechanic department
    try:
        mechanic_department = Department.objects.get(name="Warehouse")
    except Department.DoesNotExist:
        return render(request, "user/error-404.html")  # Handle the case where the department doesn't exist

    department_id = mechanic_department.id
    categories = Kategoriya.objects.filter(department_id=department_id).annotate(maxsulot_count=Count('maxsulot'))
    products = Maxsulot.objects.filter(kategoriya__in=categories)
    users = User.objects.all()

    return render(request, "user/pos-warehouse.html", {
        'departments': departments,
        'products': products,
        'cart_items': cart_items,
        'cart_items_count': cart_items.count(),
        'active_department': department_id,
        'categories': categories,
        'search_url': 'warehouse_search_products',
        'users': users,
        'today_orders': today_orders
    })


@login_required(login_url='login_page')
def mechanic_page(request):
    if request.user.is_superuser:
        return redirect("dashboard1")
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today, foydalanuvchi=request.user)
    if cart_items.exists():
        current_section = cart_items.first().maxsulot.kategoriya.department.name
        if current_section != "Mechanic":
            return redirect("warehouse_page")
    departments = Department.objects.annotate(category_count=Count('kategoriya'))
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

    # Get the Mechanic department
    try:
        mechanic_department = Department.objects.get(name="Mechanic")
    except Department.DoesNotExist:
        return render(request, "user/error-404.html")  # Handle the case where the department doesn't exist

    department_id = mechanic_department.id
    categories = Kategoriya.objects.filter(department_id=department_id).annotate(maxsulot_count=Count('maxsulot'))
    products = Maxsulot.objects.filter(kategoriya__in=categories)
    return render(request, "user/pos-mechanic.html", {
        'departments': departments,
        'products': products,
        'cart_items': cart_items,
        'cart_items_count': cart_items.count(),
        'active_department': department_id,
        'categories': categories,
        'search_url': 'mechanic_search_products',
        'today_orders': today_orders.filter(status__in=['2', '3'])
    })


@login_required(login_url='login_page')
def filter_products(request):
    category_id = request.GET.get('category_id')
    if category_id:
        # Filter products by category ID
        products = Maxsulot.objects.filter(kategoriya_id=category_id)
        product_list = [
            {
                "id": product.id,
                "name": product.nomi,
                "image": product.rasm.url,
                "category": product.kategoriya.nomi,
            }
            for product in products
        ]
        # Return products and their details as JSON
        return JsonResponse({'products': product_list}, status=200)

    return JsonResponse({"error": "No category ID provided"}, status=400)


@login_required(login_url="login_page")
def search_products(request):
    query = request.GET.get('query', '').strip()
    print(f"Request path : {request.path}")

    # Determine the department based on the resolved URL name
    department_name = None
    if request.resolver_match.url_name == 'warehouse_search_products':
        department_name = 'warehouse'
    elif request.resolver_match.url_name == 'mechanic_search_products':
        department_name = 'mechanic'

    # Filter products by query and department
    products = Maxsulot.objects.all()
    if department_name:
        products = products.filter(kategoriya__department__name__iexact=department_name)
    if query:
        products = products.filter(nomi__icontains=query)

    product_list = [
        {
            'id': product.id,
            'nomi': product.nomi,
            'rasm': product.rasm.url if product.rasm else '',
            'kategoriya': product.kategoriya.nomi,
        } for product in products
    ]

    return JsonResponse({'products': product_list})


@login_required(login_url='login_page')
def get_cart_items(request):
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
    data = {
        "cart_items": [
            {
                "id": item.id,
                "maxsulot_nomi": item.maxsulot.nomi,
                "maxsulot_rasm": item.maxsulot.rasm.url,
                "soni": item.soni
            }
            for item in cart_items
        ]
    }
    return JsonResponse(data)


# @login_required(login_url='login_page')
# def order1_page(request):
#     order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1
#     user_orders = Order.objects.filter(foydalanuvchi=request.user)
#     today = timezone.now().date()
#     today_orders = Order.objects.filter(created_at__date=today, foydalanuvchi=request.user)
#     # Add pagination
#     paginator = Paginator(user_orders, 10)  # Show 10 orders per page
#     page_number = request.GET.get('page', 1)
#     try:
#         paginated_orders = paginator.page(page_number)
#     except PageNotAnInteger:
#         paginated_orders = paginator.page(1)
#     except EmptyPage:
#         paginated_orders = paginator.page(paginator.num_pages)
#
#     orders_1_count = Order.objects.filter(status='1').count()
#     orders_2_count = Order.objects.filter(status='2').count()
#     orders_3_count = Order.objects.filter(status='3').count()
#
#     user_ctx = {
#         "order_id": order_id,
#         "user_orders": paginated_orders,  # Use paginated orders here
#         "orders_1_count": orders_1_count,
#         "orders_2_count": orders_2_count,
#         "orders_3_count": orders_3_count,
#         "today_orders": today_orders
#     }
#     return render(request, 'user/orders.html', user_ctx)


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
        }

        # Find matching status keys for partial matches
        matching_status_keys = [
            key for name, key in status_mapping.items()
            if query.lower() in name.lower()
        ]

        # Filter orders
        filtered_orders = Order.objects.filter(
            Q(foydalanuvchi=request.user) & (
                    Q(id__icontains=query) |
                    Q(maxsulotlar__maxsulot__nomi__icontains=query) |
                    Q(status__in=matching_status_keys)  # Match status keys for partial matches
            )
        ).distinct() if query else Order.objects.filter(foydalanuvchi=request.user)

        paginator = Paginator(filtered_orders, 10)  # Paginate results
        try:
            paginated_orders = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_orders = paginator.page(1)
        except EmptyPage:
            paginated_orders = paginator.page(paginator.num_pages)

        # Render only the table rows
        html = render_to_string('user/partials/order_list.html', {
            'user_orders': paginated_orders,
            'query': query  # Pass query to template for pagination links
        }, request=request)

        return JsonResponse({'html': html})
    return JsonResponse({'error': 'Invalid request type'}, status=400)


@csrf_exempt
def submit_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == "POST":
        data = json.loads(request.body)
        password = data.get("password")

        # Check if password is not None and is a valid integer
        try:
            password = int(password)  # Try to convert the password to an integer
        except (TypeError, ValueError):  # Catch invalid type or value errors
            return JsonResponse({"success": False, "message": "Noto'g'ri parol!"})

        parol = AdminParol.objects.last()
        if parol and password == int(parol.parol):
            order.status = '2'
            order.save()
            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "message": "Noto'g'ri parol!"})

    return JsonResponse({"success": False, "message": "Noto'g'ri so'rov turi."})


@csrf_exempt
def cancel_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == "POST":
        data = json.loads(request.body)
        reason = data.get("reason")
        if reason:
            order.status = '3'
            order.bekor_qilish_sababi = reason
            order.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "message": "Bekor qilish sababi talab qilinadi!"})
    return JsonResponse({"success": False, "message": "Noto'g'ri so'rov turi."})


@login_required(login_url='login_page')
def order1_details(request, pk):
    if not request.user.is_superuser:
        return redirect('mechanic_page')

    # Filter orders based on user type
    if request.user.username == "sklad":
        orders = Order.objects.filter(kimga="2")
    else:
        orders = Order.objects.all()

    # Filter today's orders with status '1'
    today_orders = orders.filter(created_at__date=timezone.now().date(), status='1')

    # Get the specific order or return 404
    order = get_object_or_404(Order, id=pk)

    context = {
        'order': order,
        'today_orders': today_orders
    }

    return render(request, 'user/order-details.html', context)


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

        return render(request, 'user/user-order-detail.html', user_ctx)


@login_required(login_url='login_page')
def bad_request_view(request, exception=None):
    return render(request, 'user/error-404.html')


@csrf_exempt  # In production, remove this and use CSRF middleware properly
@login_required
def update_cart_quantity(request, cart_item_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_quantity = data.get("new_quantity")

            if new_quantity is None:
                return JsonResponse({"success": False, "message": "Yaroqsiz ma’lumotlar"})

            # Fetch the cart item
            cart_item = CartItems.objects.get(id=cart_item_id, foydalanuvchi=request.user)
            cart_item.soni = int(new_quantity)
            cart_item.save()

            return JsonResponse(
                {"success": True, "message": "Soni muvaffaqiyatli yangilandi", "new_quantity": cart_item.soni})
        except CartItems.DoesNotExist:
            return JsonResponse({"success": False, "message": "Mahsulot savatda mavjud emas"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Yaroqsiz ma’lumotlar"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Xatolik: {str(e)}"})
    return JsonResponse({"success": False, "message": "Noto'g'ri so'rov usuli."})


@login_required(login_url='login_page')
def home_page(request):
    today = timezone.now().date()

    if request.user.is_superuser:
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
            orders_1 = orders.filter(status='1')
            orders_2 = orders.filter(status='2')
            orders_3 = orders.filter(status='3')

            today_orders = orders.filter(created_at__date=today)
            today_orders_1 = today_orders.filter(status='1')
            today_orders_2 = today_orders.filter(status='2')

            users = User.objects.all()
        else:
            orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))
            orders_1 = orders.filter(status='1')
            orders_2 = orders.filter(status='2')
            orders_3 = orders.filter(status='3')

            today_orders = orders.filter(created_at__date=today)
            today_orders_1 = today_orders.filter(status='1')
            today_orders_2 = today_orders.filter(status='2')

            users = User.objects.all()

        admin_ctx = {
            'orders': orders,
            'top_orders': orders[:10],
            'orders_1': orders_1,
            'orders_2': orders_2,
            'orders_3': orders_3,
            'today_orders': today_orders,
            'today_orders_1': today_orders_1,
            'today_orders_2': today_orders_2,
            'users': users,
        }

        return render(request, 'admin-home.html', admin_ctx)

    elif request.user.is_staff:
        kategoriya = get_object_or_404(Kategoriya, id=1)
        maxsulotlar = Maxsulot.objects.filter(Q(kategoriya=kategoriya) | Q(kategoriya__isnull=True))
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1
        user_ctx = {
            'maxsulotlar': maxsulotlar,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
        }

        return render(request, 'user-home.html', user_ctx)

    else:
        return redirect('login_page')


@login_required(login_url='login_page')
def user_sklad(request):
    if request.user.is_staff:
        site_settings = SiteSettings.objects.last()
        kategoriya = get_object_or_404(Kategoriya, pk=2)
        maxsulotlar = Maxsulot.objects.filter(kategoriya=kategoriya)
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

        return render(request, 'user-sklad.html', user_ctx)

    else:
        return redirect('home_page')


@login_required(login_url='login_page')
def superadmin_product_page(request):
    if request.user.is_superuser:
        maxsulotlar = Maxsulot.objects.all()

        user_ctx = {
            'maxsulotlar': maxsulotlar,
        }

        return render(request, 'user-home.html', user_ctx)

    else:
        return redirect('home_page')


@login_required(login_url='login_page')
def profile_page(request):
    if request.user.is_superuser:
        return redirect('home_page')
    elif request.user.is_staff:
        site_settings = SiteSettings.objects.last()
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1
        user_orders = Order.objects.filter(foydalanuvchi=request.user)

        user_orders_1 = user_orders.filter(status='1')
        user_orders_2 = user_orders.filter(status='2')
        user_orders_3 = user_orders.filter(status='3')

        # Pagination logic for all orders
        page_number = request.GET.get('page')
        paginator = Paginator(user_orders, 10)
        page_obj = paginator.get_page(page_number)

        # Pagination logic for status '1'
        page_number_1 = request.GET.get('page_1')
        paginator_1 = Paginator(user_orders_1, 10)
        page_obj_1 = paginator_1.get_page(page_number_1)

        # Pagination logic for status '2'
        page_number_2 = request.GET.get('page_2')
        paginator_2 = Paginator(user_orders_2, 10)
        page_obj_2 = paginator_2.get_page(page_number_2)

        # Pagination logic for status '3'
        page_number_3 = request.GET.get('page_3')
        paginator_3 = Paginator(user_orders_3, 10)
        page_obj_3 = paginator_3.get_page(page_number_3)

        user_ctx = {
            'site_settings': site_settings,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
            'user_orders': page_obj,
            'user_orders_1': page_obj_1,
            'user_orders_2': page_obj_2,
            'user_orders_3': page_obj_3,
        }

        return render(request, 'user-profile.html', user_ctx)


@login_required(login_url='login_page')
def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            quantity = int(data.get("qty", 1))

            # Fetch the product or raise a 404 error
            product = get_object_or_404(Maxsulot, id=product_id)

            # Create or update cart item
            cart_item, created = CartItems.objects.get_or_create(
                maxsulot=product,
                foydalanuvchi=request.user
            )

            if not created:
                return JsonResponse({"success": False, "message": "Mahsulot savatda mavjud!"})

            # Set the quantity and save
            cart_item.soni = quantity
            cart_item.save()

            # Get the updated cart item count
            cart_count = CartItems.objects.filter(foydalanuvchi=request.user).count()

            return JsonResponse({
                "success": True,
                "message": "Mahsulot savatga qo'shildi!",
                "cart_items_count": cart_count,
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Xatolik yuz berdi: {str(e)}"})

    return JsonResponse({"success": False, "message": "Noto'g'ri so'rov usuli."})


# Update cart

# Remove from cart
@login_required(login_url='login_page')
def remove_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItems, id=item_id)
        cart_item.delete()
        return JsonResponse({"success": True, "message": "Muvaffaqiyatli o'chirildi!"})
    return JsonResponse({"success": False, "message": "Xatolik yuz berdi."})


# Remove all cart
@login_required(login_url='login_page')
def remove_all_cart(request):
    if request.method == "POST":
        CartItems.objects.filter(foydalanuvchi=request.user).delete()

        return JsonResponse({"success": True, "message": "Savatcha muvaffaqiyatli tozalandi!"})
    return JsonResponse({"success": False, "message": "Xatolik yuz berdi."})


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
                return JsonResponse({'success': False, 'message': "Bo'lim tanlanmadi."}, status=400)
            if to_field == "Mexanika bo'limi":
                to_field = "1"
            elif to_field == "Omborxona":
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

                return JsonResponse({'success': True, 'message': "Buyurtma muvaffaqiyatli jo'natildi"}, status=200)

            return JsonResponse({'success': False, 'message': "Savatda mahsulot mavjud emas."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': "Noto'g'ri so'rov yuborildi."}, status=400)

    return render(request, 'user/pos-mechanic.html', user_ctx)


@login_required(login_url='login_page')
def order_detail_page(request, pk):
    if request.user.is_superuser:
        return redirect('home_page')
    elif request.user.is_staff:
        order = get_object_or_404(Order, id=pk)
        site_settings = SiteSettings.objects.last()
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        cart_item_count = cart_items.count()
        order_id = (Order.objects.first().id + 1) if Order.objects.first() else 1

        user_ctx = {
            'site_settings': site_settings,
            'order_id': order_id,
            'cart_items': cart_items,
            'cart_item_count': cart_item_count,
            'order': order,
        }

        return render(request, 'order-detail.html', user_ctx)


@login_required(login_url='login_page')
def superadmin_all_orders_page(request):
    if request.user.is_superuser:
        site_settings = SiteSettings.objects.last()

        if request.user.username == "sklad":
            all_orders = Order.objects.filter(kimga="2")
        else:
            all_orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))
        orders = all_orders.filter(status='1')  # Only orders with status '1'
        orders_1_count = all_orders.filter(status='1').count()
        orders_2_count = all_orders.filter(status='2').count()
        orders_3_count = all_orders.filter(status='3').count()
        admin_ctx = {
            'site_settings': site_settings,
            'orders': orders,
            'orders_1': orders_1_count,
            'orders_2': orders_2_count,
            'orders_3': orders_3_count,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)

    else:
        return redirect('home_page')


@login_required(login_url='login_page')
def superadmin_orders_1_page(request):
    if request.user.is_superuser:
        site_settings = SiteSettings.objects.last()

        # Retrieve all relevant orders based on `kimga` and `username`
        if request.user.username == "sklad":
            all_orders = Order.objects.filter(kimga="2")
        else:
            all_orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        # Filter for each status
        orders = all_orders.filter(status='1')  # Only orders with status '1'
        orders_1_count = all_orders.filter(status='1').count()
        orders_2_count = all_orders.filter(status='2').count()
        orders_3_count = all_orders.filter(status='3').count()

        paginator = Paginator(orders, 10)  # Show 10 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        admin_ctx = {
            'site_settings': site_settings,
            'orders': page_obj,
            'orders_1': orders_1_count,
            'orders_2': orders_2_count,
            'orders_3': orders_3_count,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        return redirect('home_page')


@login_required(login_url='login_page')
def superadmin_orders_2_page(request):
    if request.user.is_superuser:
        site_settings = SiteSettings.objects.last()

        # Retrieve all relevant orders based on `kimga` and `username`
        if request.user.username == "sklad":
            all_orders = Order.objects.filter(kimga="2")
        else:
            all_orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        # Filter for each status
        orders = all_orders.filter(status='2')  # Only orders with status '2'
        orders_1_count = all_orders.filter(status='1').count()
        orders_2_count = all_orders.filter(status='2').count()
        orders_3_count = all_orders.filter(status='3').count()

        # Pagination logic
        paginator = Paginator(orders, 10)  # Show 10 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        admin_ctx = {
            'site_settings': site_settings,
            'orders': page_obj,  # Pass paginated orders
            'orders_1': orders_1_count,
            'orders_2': orders_2_count,
            'orders_3': orders_3_count,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        return redirect('home_page')


@login_required(login_url='login_page')
def superadmin_orders_3_page(request):
    if request.user.is_superuser:
        site_settings = SiteSettings.objects.last()

        # Retrieve all relevant orders based on `kimga` and `username`
        if request.user.username == "sklad":
            all_orders = Order.objects.filter(kimga="2")
        else:
            all_orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        # Filter for each status
        orders = all_orders.filter(status='3')  # Only orders with status '3'
        orders_1_count = all_orders.filter(status='1').count()
        orders_2_count = all_orders.filter(status='2').count()
        orders_3_count = all_orders.filter(status='3').count()
        paginator = Paginator(orders, 10)  # Show 10 orders per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        admin_ctx = {
            'site_settings': site_settings,
            'orders': page_obj,
            'orders_1': orders_1_count,
            'orders_2': orders_2_count,
            'orders_3': orders_3_count,
        }

        return render(request, 'admin-all-orders.html', admin_ctx)
    else:
        return redirect('home_page')


@login_required(login_url='login_page')
def superadmin_edit_order_page(request, pk):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)

        if request.method == "POST":
            if 'sabab' in request.POST:
                order.status = '3'
                order.bekor_qilish_sababi = request.POST.get('sabab')
                order.save()
            elif 'parol' in request.POST:
                parol_input = request.POST.get('parol')
                parol = AdminParol.objects.last()
                if parol and int(parol_input) == int(parol.parol):
                    order.status = '2'
                    order.save()

        site_settings = SiteSettings.objects.last()
        orders_1_count = Order.objects.filter(status='1').count()
        orders_2_count = Order.objects.filter(status='2').count()
        orders_3_count = Order.objects.filter(status='3').count()

        admin_ctx = {
            'site_settings': site_settings,
            'order': order,
            "orders_1": orders_1_count,
            "orders_2": orders_2_count,
            "orders_3": orders_3_count
        }

        return render(request, 'admin-order-edit.html', admin_ctx)

    else:
        return redirect('home_page')


@login_required(login_url='login_page')
def superadmin_order_status_2(request, pk):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)
        order.status = '2'
        order.save()
        return redirect('superadmin_edit_order_page', pk=pk)
    else:
        return redirect('home_page')
