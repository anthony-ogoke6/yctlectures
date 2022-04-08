from cart.cart import Cart
from cart.forms import CartAddProductForm
from django import template


register = template.Library()





@register.inclusion_tag('cart/cart-body-content.html')
def cart_detail(request):

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})


    #return render(request, 'ent/article_detail.html', context)
    return {'cart': cart}
