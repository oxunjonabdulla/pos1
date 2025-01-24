from modeltranslation.translator import TranslationOptions,register

from product_app.models import Kategoriya, Maxsulot


@register(Kategoriya)
class KategoriyaTranslationOptions(TranslationOptions):
    fields = ("nomi",)


@register(Maxsulot)
class MaxsulotTranslationOptions(TranslationOptions):
    fields = ("nomi", )