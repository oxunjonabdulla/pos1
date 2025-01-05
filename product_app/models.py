from django.db import models
from user_app.models import User


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

class Kategoriya(models.Model):
    nomi = models.CharField(max_length=255)
    image = models.ImageField(upload_to='kategoriya', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)  # Link to Department

    def __str__(self):
        return self.nomi

class Maxsulot(models.Model):
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE, null=True, blank=True)
    nomi = models.CharField(max_length=455)
    rasm = models.ImageField(upload_to='maxsulotlar')
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)
    razmer = models.CharField(max_length=255)
    qoshimcha = models.TextField(null=True, blank=True)
    ball = models.BigIntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)  # New field


    def __str__(self):
        return self.nomi

    class Meta:
        ordering = ['-ball']
        verbose_name_plural = "Maxsulotlar"


class CartItems(models.Model):
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    soni = models.BigIntegerField(default=1)
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.maxsulot.nomi} x {self.soni}"

    class Meta:
        verbose_name_plural = "Foydalanuvchi savatchasi"

class OrderItems(models.Model):
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)
    soni = models.BigIntegerField(default=1)
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.maxsulot.nomi}({self.maxsulot.razmer}) x {self.soni}"

    class Meta:
        verbose_name_plural = "Buyurtma maxsulotlari"

STATUS_CHOICES = (
    ('1', 'Buyurtma berildi'),
    ('2', 'Bajarildi'),
    ('3', 'Bekor qilindi'),
)

ADMIN_CHOICES = (
    ('1', 'Mexanika bo\'limi'),
    ('2', 'Omborxona'),
)

class Order(models.Model):
    maxsulotlar = models.ManyToManyField(OrderItems)
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE)
    jami_maxsulot = models.BigIntegerField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='1')
    bekor_qilish_sababi = models.TextField(null=True, blank=True)
    qoshimcha_rasm = models.ImageField(upload_to='qoshimcha-rasmlar', null=True, blank=True)
    qoshimcha_matn = models.TextField(null=True, blank=True)
    kimga = models.CharField(max_length=255, choices=ADMIN_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        order_item = self.maxsulotlar.all().first()
        if order_item:
            return f"{order_item.maxsulot.nomi} x {order_item.soni}"
        return "Mahsulot topilmadi"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Buyurtmalar"

