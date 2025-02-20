from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from BOLT.forms import ProductForm
from product_app.models import Maxsulot, CartItems, Order, Kategoriya, Department
from user_app.models import User


@login_required(login_url='login_page')
def dashboard_page(request):
    today = timezone.now().date()

    if request.user.is_superuser and request.user.username != "superadmin":
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
        else:
            orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))

        # Add pagination for orders
        paginator = Paginator(orders.filter(created_at__date=today, status='1'), 10)  # Show 10 orders per page
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
        return render(request, 'user/department/dashboard.html', admin_ctx)

    elif request.user.is_staff and not request.user.is_superuser:
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)
        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today, foydalanuvchi=request.user)
        if cart_items.exists():
            current_section = cart_items.first().maxsulot.kategoriya.department.name
            if current_section != "Mexanika bo'limi":
                return redirect("warehouse_page")
        departments = Department.objects.annotate(category_count=Count('kategoriya'))
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

        # Get the Mechanic department
        try:
            mechanic_department = Department.objects.get(name="Mexanika bo'limi")
        except Department.DoesNotExist:
            return render(request, "user/error-404.html")  # Handle the case where the department doesn't exist

        department_id = mechanic_department.id
        categories = Kategoriya.objects.filter(department_id=department_id).annotate(maxsulot_count=Count('maxsulot'))
        products = Maxsulot.objects.filter(kategoriya__in=categories)
        return render(request, "user/department/pos-mechanic.html", {
            'departments': departments,
            'products': products,
            'cart_items': cart_items,
            'cart_items_count': cart_items.count(),
            'active_department': department_id,
            'categories': categories,
            'search_url': 'mechanic_search_products',
            'today_orders': today_orders.filter(status__in=['2', '3'])
        })

    elif request.user.username == "superadmin":
        return redirect("super_admin_products")

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
        if current_section != "Omborxona":
            return redirect("mechanic_page")
    # Annotate each department with the count of its related categories
    departments = Department.objects.annotate(category_count=Count('kategoriya'))
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

    # Get the Mechanic department
    try:
        mechanic_department = Department.objects.get(name="Omborxona")
    except Department.DoesNotExist:
        return render(request, "user/error-404.html")  # Handle the case where the department doesn't exist

    department_id = mechanic_department.id
    categories = Kategoriya.objects.filter(department_id=department_id).annotate(maxsulot_count=Count('maxsulot'))
    products = Maxsulot.objects.filter(kategoriya__in=categories)
    users = User.objects.all()

    return render(request, "user/department/pos-warehouse.html", {
        'departments': departments,
        'products': products,
        'cart_items': cart_items,
        'cart_items_count': cart_items.count(),
        'active_department': department_id,
        'categories': categories,
        'search_url': 'warehouse_search_products',
        'users': users,
        "today_orders": today_orders.filter(status__in=['2', '3'])
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
        if current_section != "Mexanika bo'limi":
            return redirect("warehouse_page")
    departments = Department.objects.annotate(category_count=Count('kategoriya'))
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

    # Get the Mechanic department
    try:
        mechanic_department = Department.objects.get(name="Mexanika bo'limi")
    except Department.DoesNotExist:
        return render(request, "user/error-404.html")  # Handle the case where the department doesn't exist

    department_id = mechanic_department.id
    categories = Kategoriya.objects.filter(department_id=department_id).annotate(maxsulot_count=Count('maxsulot'))
    products = Maxsulot.objects.filter(kategoriya__in=categories)
    return render(request, "user/department/pos-mechanic.html", {
        'departments': departments,
        'products': products,
        'cart_items': cart_items,
        'cart_items_count': cart_items.count(),
        'active_department': department_id,
        'categories': categories,
        'search_url': 'mechanic_search_products',
        'today_orders': today_orders.filter(status__in=['2', '3'])
    })


@login_required(login_url="login_page")
def admin_warehouse_page(request):
    # Restrict access to superusers only
    if not request.user.is_superuser or request.user.username == "sklad":
        return redirect("dashboard1")
    if request.user.is_superuser:
        if request.user.username == "sklad":
            orders = Order.objects.filter(kimga="2")
        else:
            orders = Order.objects.filter(Q(kimga="1") | Q(kimga=None))
    # Get today's date
    today = timezone.now().date()

    # Fetch user's orders for today with specific statuses
    today_orders = orders.filter(
        created_at__date=today,
        # foydalanuvchi=request.user,
        status="1"
    )

    # Fetch all departments with the count of related categories
    departments = Department.objects.annotate(category_count=Count('kategoriya'))

    # Fetch cart items for the current user
    cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

    # Get the warehouse department or return a 404 error if not found
    warehouse_department = get_object_or_404(Department, name="Omborxona")

    # Fetch categories related to the warehouse department with product counts
    categories = Kategoriya.objects.filter(department=warehouse_department).annotate(
        maxsulot_count=Count('maxsulot')
    )

    # Fetch products that belong to these categories
    products = Maxsulot.objects.filter(kategoriya__in=categories).select_related("kategoriya")

    # Fetch all users
    users = User.objects.all()

    # Render the template with context data
    return render(request, "user/department/admin-warehouse.html", {
        'departments': departments,
        'products': products,
        'cart_items': cart_items,
        'cart_items_count': cart_items.count(),
        'active_department': warehouse_department.id,
        'categories': categories,
        'search_url': 'warehouse_search_products',
        'users': users,
        'today_orders': today_orders,
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
                'razmer': product.razmer,

            }
            for product in products
        ]
        # Return products and their details as JSON
        return JsonResponse({'products': product_list}, status=200)

    return JsonResponse({"error": _("Hech qanday kategoriya identifikatori berilmagan")}, status=400)


@login_required(login_url="login_page")
def search_products(request):
    query = request.GET.get('query', '').strip()

    # Determine the department based on the resolved URL name
    department_name = None
    if request.resolver_match.url_name == 'warehouse_search_products':
        department_name = 'Omborxona'
    elif request.resolver_match.url_name == 'mechanic_search_products':
        department_name = 'Mexanika bo\'limi'

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
            'razmer': product.razmer,
        } for product in products
    ]

    return JsonResponse({'products': product_list})


@login_required(login_url='login_page')
def check_section(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        target_section = data.get("section")

        # Get cart items for the current user
        cart_items = CartItems.objects.filter(foydalanuvchi=request.user)

        if cart_items.exists():
            # Get the current section from the first cart item
            current_section = cart_items.first().maxsulot.kategoriya.department.name

            # Map section names for comparison
            section_map = {
                "Omborxona": "Warehouse",
                "Mexanika bo'limi": "Mechanic"
            }
            reverse_map = {v: k for k, v in section_map.items()}

            # Convert sections for consistency
            current_section_en = section_map.get(current_section, current_section)
            target_section_uz = reverse_map.get(target_section, target_section)

            # If sections don't match, send error response
            if current_section_en != target_section:
                return JsonResponse({
                    "success": False,
                    "message": _(
                        "<span style='color: #007bff; font-weight: bold;'>%(target_section)s</span> "
                        "bo'limga o'tish uchun avval "
                        "<span style='color: #dc3545; font-weight: bold;'>%(current_section)s</span> "
                        "savatidagi mahsulotlarni o'chiring yoki buyurtma bering."
                    ) % {
                                   "target_section": target_section_uz,
                                   "current_section": current_section,
                               }
                }, status=400)

        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": _("Noto'g'ri so'rov usuli.")}, status=405)


@login_required(login_url='login_page')
def bad_request_view(request, exception=None):
    return render(request, 'user/error-404.html')


from django.core.paginator import Paginator
from django.utils.translation import gettext as _


@login_required(login_url='login_page')
def products_page(request):
    today = timezone.now().date()

    if request.user.is_superuser and request.user.username == "sklad":
        orders = Order.objects.filter(kimga="2")

        # Pagination setup
        products_list = Maxsulot.objects.order_by("-created_at").filter(kategoriya__department__name="Omborxona")
        paginator = Paginator(products_list, 10)  # Show 10 products per page
        page_number = request.GET.get("page")
        products = paginator.get_page(page_number)
        categories = Kategoriya.objects.filter(department__name="Omborxona")

        orders_1_count = orders.filter(status='1').count()
        orders_2_count = orders.filter(status='2').count()
        orders_3_count = orders.filter(status='3').count()

        user_ctx = {
            "orders_1_count": orders_1_count,
            "orders_2_count": orders_2_count,
            "orders_3_count": orders_3_count,
            "today_orders": orders.filter(created_at__date=today, status='1'),
            "products": products,  # Paginated product list
            "categories": categories
        }
        return render(request, "user/products.html", user_ctx)

    return redirect("mechanic_page")


@login_required(login_url='login_page')
def add_product(request):
    if request.user.is_superuser and request.user.username == "sklad":
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                user = request.user
                product = form.save(commit=False)
                product.foydalanuvchi = user
                product.save()
                return JsonResponse({"success": True, "message": _("Mahsulot muvaffaqiyatli qo'shildi")}, status=200)
            else:
                return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"success": False, "message": "Ruxsat etilmagan foydalanuvchi!"}, status=403)


def update_product(request, product_id):
    product = get_object_or_404(Maxsulot, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            return JsonResponse({
                "success": True,
                "message": "Mahsulot muvaffaqiyatli yangilandi!",
                "product": {
                    "id": product.id,
                    "nomi": product.nomi,
                    "kategoriya": product.kategoriya.id if product.kategoriya else None,
                    "razmer": product.razmer,
                    "count": product.count,
                    "rasm": product.rasm.url if product.rasm else None
                }
            })
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    return JsonResponse({"success": False, "message": "Noto'g'ri so'rov usuli."})


@login_required(login_url='login_page')
def get_product(request, product_id):
    product = get_object_or_404(Maxsulot, id=product_id)
    return JsonResponse({
        "success": True,
        "product": {
            "id": product.id,
            "nomi": product.nomi,
            "kategoriya": product.kategoriya.id if product.kategoriya else "",
            "razmer": product.razmer,
            "count": product.count,
            "rasm": product.rasm.url if product.rasm else None
        }
    })


@login_required(login_url="login_page")
def super_admin_products(request):
    if request.user.is_superuser and request.user.username == "superadmin":
        products_list = Maxsulot.objects.order_by("-created_at").filter(kategoriya__department__name="Omborxona")
        paginator = Paginator(products_list, 10)  # Show 10 products per page
        page_number = request.GET.get("page")
        products = paginator.get_page(page_number)
        today_orders = Order.objects.filter(created_at__date=timezone.now().date(), status='1')
        return render(
            request,
            "user/superadmin-mahsulotlar.html",
            {
                "products": products,
                "today_orders": today_orders
            }
        )
    return redirect("dashboard1")


from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation


def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response
