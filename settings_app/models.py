from django.db import models

class SiteSettings(models.Model):
    title = models.CharField(max_length=455)
    logo = models.ImageField(upload_to='logos')
    brand_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Sayt sozlamalari"

class AdminParol(models.Model):
    parol = models.BigIntegerField()

    def __str__(self):
        return str(self.parol)