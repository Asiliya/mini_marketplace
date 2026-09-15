from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from carts.models import CartItem
from orders.models import Order, OrderItem, OrderStatus
from products.models import Category, Product
from wishlist.models import WishListItem


User = get_user_model()


class Command(BaseCommand):
    help = "Create test data for the marketplace"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating test data...")

        # -------------------------
        # Users
        # -------------------------

        users_data = [
            {
                "username": "noadmin",
                "email": "noadmin@example.com",
                "password": "noadmin123",
            },
            {
                "username": "john",
                "email": "john@example.com",
                "password": "john123",
            },
            {
                "username": "alice",
                "email": "alice@example.com",
                "password": "alice123",
            },
            {
                "username": "bob",
                "email": "bob@example.com",
                "password": "bob123",
            },
        ]

        users = {}

        for data in users_data:
            password = data.pop("password")

            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults=data,
            )

            if created:
                user.set_password(password)
                user.save()

            users[user.username] = user

        # -------------------------
        # Categories
        # -------------------------

        category_names = [
            "Electronics",
            "Books",
            "Clothing",
            "Home",
            "Sports",
        ]

        categories = {}

        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name)
            categories[name] = category

        # -------------------------
        # Products
        # -------------------------

        products_data = [
            {
                "name": "Wireless Headphones",
                "description": "High quality wireless headphones",
                "price": Decimal("99.99"),
                "discount_price": Decimal("79.99"),
                "sku": "ELEC-001",
                "stock": 20,
                "category": categories["Electronics"],
                "author": users["john"],
            },
            {
                "name": "Mechanical Keyboard",
                "description": "Mechanical keyboard for work and gaming",
                "price": Decimal("129.99"),
                "sku": "ELEC-002",
                "stock": 15,
                "category": categories["Electronics"],
                "author": users["john"],
            },
            {
                "name": "USB-C Cable",
                "description": "Durable USB-C charging cable",
                "price": Decimal("19.99"),
                "sku": "ELEC-003",
                "stock": 50,
                "category": categories["Electronics"],
                "author": users["alice"],
            },
            {
                "name": "Python Programming Book",
                "description": "Learn Python programming from beginner to advanced",
                "price": Decimal("49.99"),
                "sku": "BOOK-001",
                "stock": 10,
                "category": categories["Books"],
                "author": users["alice"],
            },
            {
                "name": "Django for Beginners",
                "description": "Practical introduction to Django web development",
                "price": Decimal("54.99"),
                "discount_price": Decimal("44.99"),
                "sku": "BOOK-002",
                "stock": 12,
                "category": categories["Books"],
                "author": users["bob"],
            },
            {
                "name": "Clean Code",
                "description": "A handbook of agile software craftsmanship",
                "price": Decimal("39.99"),
                "sku": "BOOK-003",
                "stock": 8,
                "category": categories["Books"],
                "author": users["john"],
            },
            {
                "name": "Basic T-Shirt",
                "description": "Comfortable cotton t-shirt",
                "price": Decimal("24.99"),
                "sku": "CLOTH-001",
                "stock": 30,
                "category": categories["Clothing"],
                "author": users["alice"],
            },
            {
                "name": "Hoodie",
                "description": "Warm everyday hoodie",
                "price": Decimal("59.99"),
                "discount_price": Decimal("49.99"),
                "sku": "CLOTH-002",
                "stock": 18,
                "category": categories["Clothing"],
                "author": users["bob"],
            },
            {
                "name": "Jeans",
                "description": "Classic blue jeans",
                "price": Decimal("69.99"),
                "sku": "CLOTH-003",
                "stock": 14,
                "category": categories["Clothing"],
                "author": users["john"],
            },
            {
                "name": "Coffee Maker",
                "description": "Automatic coffee maker for home",
                "price": Decimal("89.99"),
                "sku": "HOME-001",
                "stock": 7,
                "category": categories["Home"],
                "author": users["alice"],
            },
            {
                "name": "Desk Lamp",
                "description": "LED desk lamp with adjustable brightness",
                "price": Decimal("34.99"),
                "discount_price": Decimal("29.99"),
                "sku": "HOME-002",
                "stock": 25,
                "category": categories["Home"],
                "author": users["bob"],
            },
            {
                "name": "Office Chair",
                "description": "Ergonomic office chair",
                "price": Decimal("199.99"),
                "sku": "HOME-003",
                "stock": 5,
                "category": categories["Home"],
                "author": users["john"],
            },
            {
                "name": "Football",
                "description": "Professional size football",
                "price": Decimal("29.99"),
                "sku": "SPORT-001",
                "stock": 20,
                "category": categories["Sports"],
                "author": users["john"],
            },
            {
                "name": "Running Shoes",
                "description": "Lightweight running shoes",
                "price": Decimal("119.99"),
                "discount_price": Decimal("99.99"),
                "sku": "SPORT-002",
                "stock": 11,
                "category": categories["Sports"],
                "author": users["alice"],
            },
            {
                "name": "Yoga Mat",
                "description": "Non-slip yoga mat",
                "price": Decimal("29.99"),
                "sku": "SPORT-003",
                "stock": 22,
                "category": categories["Sports"],
                "author": users["bob"],
            },
        ]

        products = {}

        for data in products_data:
            product, _ = Product.objects.get_or_create(
                sku=data["sku"],
                defaults=data,
            )

            products[data["sku"]] = product

        # -------------------------
        # Cart items
        # -------------------------

        CartItem.objects.get_or_create(
            user=users["john"],
            product=products["ELEC-001"],
            defaults={"quantity": 2},
        )

        CartItem.objects.get_or_create(
            user=users["alice"],
            product=products["BOOK-002"],
            defaults={"quantity": 1},
        )

        CartItem.objects.get_or_create(
            user=users["bob"],
            product=products["SPORT-002"],
            defaults={"quantity": 1},
        )

        # -------------------------
        # Wishlist
        # -------------------------

        WishListItem.objects.get_or_create(
            user=users["john"],
            product=products["ELEC-002"],
        )

        WishListItem.objects.get_or_create(
            user=users["alice"],
            product=products["HOME-003"],
        )

        WishListItem.objects.get_or_create(
            user=users["bob"],
            product=products["BOOK-001"],
        )

        # -------------------------
        # Orders
        # -------------------------

        orders_data = [
            {
                "user": users["john"],
                "status": OrderStatus.PENDING,
                "items": [
                    ("ELEC-001", 1),
                    ("ELEC-003", 2),
                ],
            },
            {
                "user": users["alice"],
                "status": OrderStatus.PROCESSING,
                "items": [
                    ("BOOK-002", 1),
                    ("BOOK-003", 1),
                ],
            },
            {
                "user": users["bob"],
                "status": OrderStatus.SHIPPED,
                "items": [
                    ("CLOTH-002", 1),
                    ("SPORT-001", 1),
                ],
            },
            {
                "user": users["john"],
                "status": OrderStatus.DELIVERED,
                "items": [
                    ("HOME-001", 1),
                ],
            },
            {
                "user": users["alice"],
                "status": OrderStatus.CANCELLED,
                "items": [
                    ("SPORT-002", 1),
                ],
            },
        ]

        for order_data in orders_data:
            total_price = Decimal("0.00")

            for sku, quantity in order_data["items"]:
                product = products[sku]
                total_price += product.final_price * quantity

            order, created = Order.objects.get_or_create(
                user=order_data["user"],
                status=order_data["status"],
                defaults={
                    "total_price": total_price,
                },
            )

            if created:
                for sku, quantity in order_data["items"]:
                    product = products[sku]

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.final_price,
                    )

        self.stdout.write(
            self.style.SUCCESS("Test data created successfully!")
        )