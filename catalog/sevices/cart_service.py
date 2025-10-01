from ..models import Cart, CartItem, Product

class CartService:
    @staticmethod
    def get_or_create_cart(user):
        return Cart.objects.get_or_create(user=user)

    @staticmethod
    def add_item(user, product_id, quantity=1):
        product = Product.objects.get(product_id=product_id)
        cart, _ = CartService.get_or_create_cart(user)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return item

    @staticmethod
    def update_item(user, product_id, quantity):
        cart, _ = CartService.get_or_create_cart(user)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return None

        if quantity <= 0:
            item.delete()
            return None
        else:
            item.quantity = quantity
            item.save()
            return item

    @staticmethod
    def clear_cart(user):
        cart, _ = CartService.get_or_create_cart(user)
        cart.items.all().delete()
