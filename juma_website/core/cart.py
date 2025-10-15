
from decimal import Decimal
from .models import Producto
CART_SESSION_ID = "cart"
class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(CART_SESSION_ID, {})
        self.session.setdefault(CART_SESSION_ID, self.cart)
    def add(self, product_id, quantity=1, update_quantity=False):
        product = Producto.objects.get(id=product_id, activo=True)
        pid = str(product_id)
        if pid not in self.cart:
            self.cart[pid] = {"quantity": 0, "price": str(product.precio), "name": product.nombre, "slug": product.slug}
        self.cart[pid]["quantity"] = quantity if update_quantity else self.cart[pid]["quantity"] + quantity
        if self.cart[pid]["quantity"] <= 0: del self.cart[pid]
        self.save()
    def remove(self, product_id):
        pid = str(product_id); 
        if pid in self.cart: del self.cart[pid]; self.save()
    def clear(self):
        self.session[CART_SESSION_ID] = {}; self.save()
    def __iter__(self):
        ids = self.cart.keys()
        products = Producto.objects.filter(id__in=ids)
        for p in products:
            item = self.cart[str(p.id)]
            item["product"] = p
            item["quantity"] = int(item["quantity"])
            item["price"] = Decimal(item["price"])
            item["subtotal"] = item["price"] * item["quantity"]
            yield item
    def __len__(self): return sum(int(i["quantity"]) for i in self.cart.values())
    def get_total_price(self): return sum(Decimal(i["price"]) * int(i["quantity"]) for i in self.cart.values())
    def save(self): self.session.modified = True
