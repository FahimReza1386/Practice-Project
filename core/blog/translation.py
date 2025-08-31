# Third Party Imports
from modeltranslation.translator import register, TranslationOptions

# Locale Imports
from .models import BlogModel, BlogCategoryModel

@register(BlogModel)
class BlogModelTranslationOptions(TranslationOptions):
    fields = ('title', 'description') 

@register(BlogCategoryModel)
class BlogModelTranslationOptions(TranslationOptions):
    fields = ('name',) 