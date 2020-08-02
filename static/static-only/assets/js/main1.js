window.onload = function() {
            console.log("checking to see if this function ran")
            ();

        };

(function(){
  // Add to Cart Interaction - by CodyHouse.co
  var cart = document.getElementsByClassName('js-cd-cart');
  var product_id = document.querySelector('.javs-id').innerHTML;
  if(cart.length > 0) {
  	var cartAddBtns = document.getElementsByClassName('js-cd-add-to-cart'),
  		cartBody = cart[0].getElementsByClassName('cd-cart__body')[0],
  		cartList = cartBody.getElementsByTagName('ul')[0],
  		cartListItems = cartList.getElementsByClassName('cd-cart__product'),
  		cartTotal = cart[0].getElementsByClassName('cd-cart__checkout')[0].getElementsByTagName('span')[0],
  		cartCount = cart[0].getElementsByClassName('cd-cart__count')[0],
  		cartCountItems = cartCount.getElementsByTagName('li'),
  		cartUndo = cart[0].getElementsByClassName('cd-cart__undo')[0],
  		productId = product_id, //this is a placeholder -> use your real product ids instead
  		cartTimeoutId = false,
  		animatingQuantity = false;
		initCartEvents();

		function initCartEvents() {
			// add products to cart
			for(var i = 0; i < cartAddBtns.length; i++) {(function(i){
				cartAddBtns[i].addEventListener('click', addToCart);
			})(i);}

			// open/close cart
			cart[0].getElementsByClassName('cd-cart__trigger')[0].addEventListener('click', function(event){
				event.preventDefault();
				toggleCart();
			});

			cart[0].addEventListener('click', function(event) {
				if(event.target == cart[0]) { // close cart when clicking on bg layer
					toggleCart(true);
				} else if (event.target.closest('.cd-cart__delete-item')) { // remove product from cart
					event.preventDefault();
					removeProduct(event.target.closest('.cd-cart__product'));
				}
			});

			// update product quantity inside cart
			cart[0].addEventListener('change', function(event) {
				if(event.target.tagName.toLowerCase() == 'select') quickUpdateCart();
			});

			//reinsert product deleted from the cart
			cartUndo.addEventListener('click', function(event) {
				if(event.target.tagName.toLowerCase() == 'a') {
					event.preventDefault();
					if(cartTimeoutId) clearInterval(cartTimeoutId);
					// reinsert deleted product
					var deletedProduct = cartList.getElementsByClassName('cd-cart__product--deleted')[0];
					Util.addClass(deletedProduct, 'cd-cart__product--undo');
					deletedProduct.addEventListener('animationend', function cb(){
						deletedProduct.removeEventListener('animationend', cb);
						Util.removeClass(deletedProduct, 'cd-cart__product--deleted cd-cart__product--undo');
						deletedProduct.removeAttribute('style');
						quickUpdateCart();
					});
					Util.removeClass(cartUndo, 'cd-cart__undo--visible');
				}
			});
		};

		function addToCart(event) {
			event.preventDefault();
			if(animatingQuantity) return;
			var cartIsEmpty = Util.hasClass(cart[0], 'cd-cart--empty');
			//update cart product list
			addProduct(this);
			//update number of items
			updateCartCount(cartIsEmpty);
			//update total price
			updateCartTotal(this.getAttribute('data-price'), true);
			//show cart
			Util.removeClass(cart[0], 'cd-cart--empty');
		};

		function toggleCart(bool) { // toggle cart visibility
			var cartIsOpen = ( typeof bool === 'undefined' ) ? Util.hasClass(cart[0], 'cd-cart--open') : bool;

			if( cartIsOpen ) {
				Util.removeClass(cart[0], 'cd-cart--open');
				//reset undo
				if(cartTimeoutId) clearInterval(cartTimeoutId);
				Util.removeClass(cartUndo, 'cd-cart__undo--visible');
				removePreviousProduct(); // if a product was deleted, remove it definitively from the cart

				setTimeout(function(){
					cartBody.scrollTop = 0;
					//check if cart empty to hide it
					if( Number(cartCountItems[0].innerText) == 0) Util.addClass(cart[0], 'cd-cart--empty');
				}, 500);
			} else {
				Util.addClass(cart[0], 'cd-cart--open');
			}
		};



		function addProduct(target) {
			// this is just a product placeholder
			// you should insert an item with the selected product info
			// replace productId, productName, price and url with your real product info
			// you should also check if the product was already in the cart -> if it is, just update the quantity
			var href = document.querySelector('.javs-link').href;
			var image = document.querySelector('.javs-image').src;
			var prod_name = document.querySelector('.javs-name').innerHTML;
			var prod_price = document.querySelector('.javs-price').innerHTML;

            var ls = [];
			let products = [];
            if(localStorage.getItem('products')){
                products = JSON.parse(localStorage.getItem('products'));
                for(var g = 0; g < products.length; g++) {
                    ls.push(Number(products[g].productId));
                }
                if(ls.indexOf(Number(productId)) !== -1){
                    for(var f = 0; f < products.length; f++) {
                        if(Number(products[f].productId) === Number(productId)){
                            products[f].qty = products[f].qty + 1;
                            localStorage.setItem('products', JSON.stringify(products));
                            var updateprod = JSON.parse(localStorage.getItem('products'));
                            Array.prototype.forEach.call(updateprod, function(value, key) {
                                if(Number(value.productId) === Number(productId)){
                                    for(var i = 0; i < cartListItems.length; i++) {
    				                    if( !Util.hasClass(cartListItems[i], 'cd-cart__product--deleted') ) {
    				                        //cartListItems[i].getElementsByTagName('select')[0].options[0].innerHTML = value.qty;
    				                        var select = cartListItems[i].getElementsByTagName('select')[0];
                                            select.options[select.selectedIndex].innerHTML = value.qty;

    				                    }
                                    }
                                }
                                //var productAdded = '<li class="cd-cart__product"><div class="cd-cart__image"><a href=""><img src="'+ value.image +'" alt="placeholder"></a></div><div class="cd-cart__details"><h3 class="truncate"><a href="#0">' + value.name + '</a></h3><span class="cd-cart__price">' + value.price + '</span><div class="cd-cart__actions"><a href="#0" class="cd-cart__delete-item">Delete</a><div class="cd-cart__quantity"><label for="cd-product-'+ value.productId +'" class="cd-cart__productId">Qty</label><span class="cd-cart__select"><select class="reset" id="cd-product-'+ value.productId +'" name="quantity" data-id=" '+ value.productId +' "><option value="1">' + value.qty + '</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option></select><svg class="icon" viewBox="0 0 12 12"><polyline fill="none" stroke="currentColor" points="2,4 6,8 10,4 "/></svg></span></div></div></div></li>';
        			            //cartList.insertAdjacentHTML('beforeend', productAdded);
        			            //console.log("amount of quantity")
        			            //console.log(value.qty)
                            });
                        }
                    }
                } else {
                    products.push({'productId' : productId, image : image, name : prod_name, price: prod_price, qty:1});
                    localStorage.setItem('products', JSON.stringify(products));
                    var addednewprod = JSON.parse(localStorage.getItem('products'));
                    Array.prototype.forEach.call(addednewprod, function(value, key) {
                        var productAdded = '<li class="cd-cart__product"><div class="cd-cart__image"><a href=""><img src="'+ value.image +'" alt="placeholder"></a></div><div class="cd-cart__details"><h3 class="truncate"><a href="#0">' + value.name + '</a></h3><span class="cd-cart__price">' + value.price + '</span><div class="cd-cart__actions"><a href="#0" class="cd-cart__delete-item">Delete</a><div class="cd-cart__quantity"><label for="cd-product-'+ value.productId +'" class="cd-cart__productId">Qty</label><span class="cd-cart__select"><select class="reset" id="cd-product-'+ value.productId +'" name="quantity" data-id=" '+ value.productId +' "><option id="cd-product1-'+ value.productId +'" value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option></select><svg class="icon" viewBox="0 0 12 12"><polyline fill="none" stroke="currentColor" points="2,4 6,8 10,4 "/></svg></span></div></div></div></li>';
        			    cartList.insertAdjacentHTML('beforeend', productAdded);
        			    console.log("amount of quantity")
        			    console.log(value.qty)
                    });
                }
            } else {
                products.push({'productId' : productId, image : image, name : prod_name, price: prod_price, qty:1});
                localStorage.setItem('products', JSON.stringify(products));
                var cs = JSON.parse(localStorage.getItem('products'));
                Array.prototype.forEach.call(cs, function(value, key) {
                    var productAdded = '<li class="cd-cart__product"><div class="cd-cart__image"><a href=""><img src="'+ value.image +'" alt="placeholder"></a></div><div class="cd-cart__details"><h3 class="truncate"><a href="#0">' + value.name + '</a></h3><span class="cd-cart__price">' + value.price + '</span><div class="cd-cart__actions"><a href="#0" class="cd-cart__delete-item">Delete</a><div class="cd-cart__quantity"><label for="cd-product-'+ value.productId +'" class="cd-cart__productId">Qty</label><span class="cd-cart__select"><select class="reset" id="cd-product-'+ value.productId +'" name="quantity" data-id=" '+ value.productId +' "><option id="cd-product1-'+ value.productId +'" value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option></select><svg class="icon" viewBox="0 0 12 12"><polyline fill="none" stroke="currentColor" points="2,4 6,8 10,4 "/></svg></span></div></div></div></li>';
    			    cartList.insertAdjacentHTML('beforeend', productAdded);
    			    console.log("amount of quantity")
    			    console.log(value.qty)
                });
            }
		};


		function removeProduct(product) {
			if(cartTimeoutId) clearInterval(cartTimeoutId);
			removePreviousProduct(); // prduct previously deleted -> definitively remove it from the cart

			var topPosition = product.offsetTop,
				productQuantity = Number(product.getElementsByTagName('select')[0].value),
				productTotPrice = Number((product.getElementsByClassName('cd-cart__price')[0].innerText).replace('#', '')) * productQuantity;

			product.style.top = topPosition+'px';
			Util.addClass(product, 'cd-cart__product--deleted');

			//update items count + total price
			updateCartTotal(productTotPrice, false);
			updateCartCount(true, -productQuantity);
			Util.addClass(cartUndo, 'cd-cart__undo--visible');

			//wait 8sec before completely remove the item
			cartTimeoutId = setTimeout(function(){
				Util.removeClass(cartUndo, 'cd-cart__undo--visible');
				removePreviousProduct();
			}, 8000);
		};

		function removePreviousProduct() { // definitively removed a product from the cart (undo not possible anymore)
			var deletedProduct = cartList.getElementsByClassName('cd-cart__product--deleted');
			if(deletedProduct.length > 0 ) deletedProduct[0].remove();
		};

		function updateCartCount(emptyCart, quantity) {
			if( typeof quantity === 'undefined' ) {
			    var check = JSON.parse(localStorage.getItem('products'));
			    var lis = [];
			    for(var g = 0; g < check.length; g++) {
                    lis.push(Number(check[g].qty));
                }
                console.log("this is the content of Lis")
                console.log(lis)

			    var sum = lis.reduce(function(a, b){
                    return a + b;
                }, 0);
                console.log("this is the content of sum")
                console.log(sum)
				var actual = sum;
				var next = actual;

				if( emptyCart ) {
					cartCountItems[0].innerText = actual;
					cartCountItems[1].innerText = next;
					animatingQuantity = false;
				} else {
					Util.addClass(cartCount, 'cd-cart__count--update');

					setTimeout(function() {
						cartCountItems[0].innerText = actual;
					}, 150);

					setTimeout(function() {
						Util.removeClass(cartCount, 'cd-cart__count--update');
					}, 200);

					setTimeout(function() {
						cartCountItems[1].innerText = next;
						animatingQuantity = false;
					}, 230);
				}
			} else {
				var actual = sum;
				var next = actual;

				cartCountItems[0].innerText = actual;
				cartCountItems[1].innerText = next;
				animatingQuantity = false;
			}
		};

		function updateCartTotal(price, bool) {
			cartTotal.innerText = bool ? (Number(cartTotal.innerText) + Number(price)).toFixed(2) : (Number(cartTotal.innerText) - Number(price)).toFixed(2);
		};

		function quickUpdateCart() {
			var quantity = 0;
			var price = 0;

			for(var i = 0; i < cartListItems.length; i++) {
				if( !Util.hasClass(cartListItems[i], 'cd-cart__product--deleted') ) {
					var singleQuantity = Number(cartListItems[i].getElementsByTagName('select')[0].value);
					var prodId = Number(cartListItems[i].getElementsByTagName('select')[0].getAttribute('data-id'));
					quantity = quantity + singleQuantity;
					price = price + singleQuantity*Number((cartListItems[i].getElementsByClassName('cd-cart__price')[0].innerText).replace('#', ''));
                    products = JSON.parse(localStorage.getItem('products'));
                    for(var g = 0; g < products.length; g++) {
                        if(Number(products[g].productId) === Number(prodId)){
                            products[g].qty = singleQuantity;
                            localStorage.setItem('products', JSON.stringify(products));
                            var select = cartListItems[i].getElementsByTagName('select')[0];
                            checking = '#cd-product1-'+ productId
                            console.log("the below is The content of option tag")
                            console.log(select.options[0])
                            console.log("the below is The selected option's content of option tag")
                            console.log(select.options[select.selectedIndex].innerHTML)
                        }

                    }


				}
			}

			cartTotal.innerText = price.toFixed(2);
			cartCountItems[0].innerText = quantity;
			cartCountItems[1].innerText = quantity+1;
		};
  }
})();