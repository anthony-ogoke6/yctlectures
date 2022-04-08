
from cart.cart import Cart
from cart.forms import CartAddProductForm

from django import template


register = template.Library()


from voting.models import Department


@register.simple_tag
def courses_students_is_in(user):
	qs = Department.objects.all()
	courses_students_is_in = None
	if user:
			courses_students_is_in = qs.filter(students__in=[user])
			print(user)
	return courses_students_is_in





@register.inclusion_tag('cart/cart-body-content.html')
def cart_detail(request):

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})


    #return render(request, 'ent/article_detail.html', context)
    return {'cart': cart}

