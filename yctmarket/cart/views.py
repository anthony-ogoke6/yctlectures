from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.http import require_POST
from ent.models import Post
from .cart import Cart
from .forms import CartAddProductForm
from django.template.loader import render_to_string
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

#csrf_exempt
def show_cart(request):
	return redirect("cart:cart_detail")


@require_POST
def cart_add(request):
	if request.is_ajax():
		cart = Cart(request)
		post_id = request.POST['post_id']
		post_slug = request.POST['post_slug']
		quantity = int((request.POST['quantity']))
		update = request.POST['update']
		session = request.session
		print("items in session")
		print(session)
		post = get_object_or_404(Post, id=post_id, slug=post_slug)

		cart.add(post=post, quantity=quantity, update_quantity=update)
		return JsonResponse({'message': 'product(s) added to cart successfully'}, status=200)




csrf_exempt
def cart_remove(request, post_id):
    cart = Cart(request)
    post = get_object_or_404(Post, id=post_id)
    cart.remove(post)
    return redirect('cart:cart_detail')


def cart_detail(request):

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})
    print(cart)
    for i in cart:
        print(i['post'])
        print(i)
    context = {'cart': cart}
    html = render_to_string('cart/detail.html', context, request=request)
    return JsonResponse({'cart': html})



def cart_detail2(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})

    return render(request, 'cart/detail.html', {'cart': cart})


