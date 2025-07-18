from django import template
from shop.models import BlogModel, BlogTypeModel, BlogStatusTypeModel, WishListModel


register = template.Library()

@register.inclusion_tag("include/premium-blog.html", takes_context=True)
def show_premium_blog(context):
    request= context.get("request")
    premium_blog= BlogModel.objects.filter(status=BlogStatusTypeModel.publish.value, type=BlogTypeModel.premium.value).order_by("-created_date").distinct()[:5]
    return {"premium_blog":premium_blog, "request":request}

@register.inclusion_tag("include/similar_blog.html", takes_context=True)
def show_similar_blog(context, blog):
    request= context.get("request")
    similar_blog= BlogModel.objects.filter(status=BlogStatusTypeModel.publish.value, category=blog.category).order_by("-created_date").distinct()[:5]
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