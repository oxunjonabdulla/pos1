import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _  # Import for translation
from product_app.models import Maxsulot, CartItems


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


@csrf_exempt  # In production, remove this and use CSRF middleware properly
@login_required
def update_cart_quantity(request, cart_item_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_quantity = data.get("new_quantity")

            if new_quantity is None:
                return JsonResponse({"success": False, "message": _("Yaroqsiz ma’lumotlar")})

            # Fetch the cart item
            cart_item = CartItems.objects.get(id=cart_item_id, foydalanuvchi=request.user)
            cart_item.soni = int(new_quantity)
            cart_item.save()

            return JsonResponse(
                {"success": True, "message": _("Soni muvaffaqiyatli yangilandi"), "new_quantity": cart_item.soni})
        except CartItems.DoesNotExist:
            return JsonResponse({"success": False, "message": _("Mahsulot savatda mavjud emas")})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": _("Yaroqsiz ma’lumotlar")})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Xatolik: {str(e)}"})
    return JsonResponse({"success": False, "message": _("Noto'g'ri so'rov usuli.")})


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
                return JsonResponse({"success": False, "message": _("Mahsulot savatda mavjud!")})

            # Set the quantity and save
            cart_item.soni = quantity
            cart_item.save()

            # Get the updated cart item count
            cart_count = CartItems.objects.filter(foydalanuvchi=request.user).count()

            return JsonResponse({
                "success": True,
                "message": _("Mahsulot savatga qo'shildi!"),
                "cart_items_count": cart_count,
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Xatolik yuz berdi: {str(e)}"})

    return JsonResponse({"success": False, "message": _("Noto'g'ri so'rov usuli.")})


# Update cart

# Remove from cart
@login_required(login_url='login_page')
def remove_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItems, id=item_id)
        cart_item.delete()
        return JsonResponse({"success": True, "message": _("Muvaffaqiyatli o'chirildi!")})
    return JsonResponse({"success": False, "message": _("Xatolik yuz berdi.")})


# Remove all cart
@login_required(login_url='login_page')
def remove_all_cart(request):
    if request.method == "POST":
        CartItems.objects.filter(foydalanuvchi=request.user).delete()

        return JsonResponse({"success": True, "message": _("Savatcha muvaffaqiyatli tozalandi!")})
    return JsonResponse({"success": False, "message": _("Xatolik yuz berdi.")})
