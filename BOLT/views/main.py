import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
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

        return render(request, 'user/department/dashboard.html', admin_ctx)

    elif request.user.is_staff:
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
            'kategoriya': product.kategoriya.nomi,
        } for product in products
    ]

    return JsonResponse({'products': product_list})

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
                if current_section == "Omborxona":
                    current_section = "Omborxona"
                elif current_section == "Mexanika bo'limi":
                    current_section = "Mexanika bo'limi"
                if target_section == "Omborxona":
                    target_section = "Omborxona"
                elif target_section == "Mexanika bo'limi":
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

@login_required(login_url='login_page')
def bad_request_view(request, exception=None):
    return render(request, 'user/error-404.html')
