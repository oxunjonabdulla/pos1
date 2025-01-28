from django.db import models


class SiteSettings(models.Model):
    title = models.CharField(max_length=455)
    logo = models.ImageField(upload_to='logos')
    brand_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Sayt sozlamalari"


class SectionChoices(models.TextChoices):
    MECHANICS = '1', 'Mexanika bo\'limi'
    WAREHOUSE = '2', 'Omborxona'


class AdminParol(models.Model):
    section = models.CharField(max_length=255, choices=SectionChoices.choices,
                               default=SectionChoices.MECHANICS,null=True, blank=True)
    parol = models.BigIntegerField()

    def __str__(self):
        return str(self.parol)

    class Meta:
        verbose_name = "Admin Parol"
        verbose_name_plural = "Admin Parollari"
        ordering = ['section']