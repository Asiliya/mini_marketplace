from django.db import transaction

from orders.models import Order, OrderItem, OrderStatus
from rest_framework.exceptions import ValidationError
from django.db.models import F


@transaction.atomic
def create_order(user):
    # cart = user.cart_items.all()

    items = user.cart_items.select_related("product")

    if not items.exists():
        raise ValidationError("Cart is empty")

    for item in items:
        if item.quantity > item.product.stock:
            raise ValidationError(
                f"Not enough stock for {item.product.name}"
            )

    total = sum(
        item.product.final_price * item.quantity
        for item in items
    )

    order = Order.objects.create(
        user=user,
        total_price=total
    )

    order_items = []

    for item in items:
        product = item.product

        product.stock = F("stock") - item.quantity
        product.save(update_fields=["stock"])

        order_items.append(
            OrderItem(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.final_price
            )
        )

    OrderItem.objects.bulk_create(order_items)

    items.delete()

    return order


@transaction.atomic
def cancel_order(order: Order):
    if order.status == OrderStatus.CANCELLED:
        raise ValidationError("Order is already cancelled")

    if order.status != OrderStatus.PENDING:
        raise ValidationError(
            "Only pending orders can be cancelled."
        )
    
    if order.status in (
            OrderStatus.SHIPPED,
            OrderStatus.DELIVERED,
    ):
        raise ValidationError(
            "This order cannot be cancelled."
        )

    for item in order.items.select_related("product"):
        item.product.stock = F("stock") + item.quantity
        item.product.save(update_fields=["stock"])

    order.status = OrderStatus.CANCELLED
    order.save(update_fields=["status"])

    return order