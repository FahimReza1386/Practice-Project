# Django Imports

from django import template
from jalali_date import datetime2jalali

# Third Party

from blog.models import BlogModel, WishListModel
from review.models import ReviewModel


register = template.Library()

@register.inclusion_tag("include/premium-blog.html", takes_context=True)
def show_premium_blog(context):
    request= context.get("request")
    premium_blog= BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value, type=BlogModel.BlogTypeModel.premium.value).order_by("-created_date").distinct()[:5]
    return {"premium_blog":premium_blog, "request":request}

@register.inclusion_tag("include/similar_blog.html", takes_context=True)
def show_similar_blog(context, blog):
    request= context.get("request")
    similar_blog= BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value, category=blog.category).order_by("-created_date").distinct()[:5]
    return {"similar_blog":similar_blog, "request":request}

@register.simple_tag(takes_context=True)
def is_in_wishlist(context, blog_id):
    request=context.get("request")
    user= request.user
    blog= WishListModel.objects.filter(user=user, blog__id=blog_id).exists()
    if blog is True:
        is_wishlist= True
    else:
        is_wishlist= False
    
    return is_wishlist

@register.simple_tag()
def show_jalali_date(review_id):
    review_obj=ReviewModel.objects.get(id=review_id)
    review_date=datetime2jalali(review_obj.created_date).strftime('%y/%m/%d')
    return review_date