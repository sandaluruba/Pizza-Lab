import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import get_settings


async def seed() -> None:
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.mongo_db]

    categories = [
        {
            "_id": "classic",
            "name": "Classic",
            "description": "Traditional favorites crafted with rich tomato sauce.",
            "thumbnail": "/images/categories/classic.svg",
        },
        {
            "_id": "signature",
            "name": "Signature",
            "description": "Chef specials packed with premium toppings.",
            "thumbnail": "/images/categories/signature.svg",
        },
        {
            "_id": "veggie",
            "name": "Veggie",
            "description": "Fresh garden picks and bold herb flavors.",
            "thumbnail": "/images/categories/veggie.svg",
        },
    ]
    sizes = [
        {"code": "S", "label": "Small (8\")", "multiplier": 1.0},
        {"code": "M", "label": "Medium (12\")", "multiplier": 1.35},
        {"code": "L", "label": "Large (16\")", "multiplier": 1.7},
    ]
    pizzas = [
        {
            "_id": "margherita",
            "category_id": "classic",
            "name": "Margherita",
            "description": "San Marzano tomato, mozzarella, basil and olive oil.",
            "image": "/images/pizzas/margherita.svg",
            "thumbnail": "/images/pizzas/margherita.svg",
            "base_price": 8.99,
            "sizes": sizes,
            "tags": ["vegetarian", "best seller"],
        },
        {
            "_id": "pepperoni",
            "category_id": "classic",
            "name": "Pepperoni Blast",
            "description": "Double pepperoni, mozzarella and oregano crunch.",
            "image": "/images/pizzas/pepperoni.svg",
            "thumbnail": "/images/pizzas/pepperoni.svg",
            "base_price": 9.99,
            "sizes": sizes,
            "tags": ["spicy"],
        },
        {
            "_id": "bbq-chicken",
            "category_id": "signature",
            "name": "Smoky BBQ Chicken",
            "description": "BBQ chicken, caramelized onion, smoked cheddar.",
            "image": "/images/pizzas/bbq-chicken.svg",
            "thumbnail": "/images/pizzas/bbq-chicken.svg",
            "base_price": 11.49,
            "sizes": sizes,
            "tags": ["signature"],
        },
        {
            "_id": "truffle-mushroom",
            "category_id": "signature",
            "name": "Truffle Mushroom",
            "description": "Wild mushrooms, garlic cream sauce, truffle drizzle.",
            "image": "/images/pizzas/truffle-mushroom.svg",
            "thumbnail": "/images/pizzas/truffle-mushroom.svg",
            "base_price": 12.49,
            "sizes": sizes,
            "tags": ["premium"],
        },
        {
            "_id": "garden-fresh",
            "category_id": "veggie",
            "name": "Garden Fresh",
            "description": "Bell peppers, onions, olives, sweetcorn and basil.",
            "image": "/images/pizzas/garden-fresh.svg",
            "thumbnail": "/images/pizzas/garden-fresh.svg",
            "base_price": 10.49,
            "sizes": sizes,
            "tags": ["vegetarian"],
        },
        {
            "_id": "paneer-tikka",
            "category_id": "veggie",
            "name": "Paneer Tikka",
            "description": "Tandoori paneer, onion, capsicum, mint yogurt drizzle.",
            "image": "/images/pizzas/paneer-tikka.svg",
            "thumbnail": "/images/pizzas/paneer-tikka.svg",
            "base_price": 11.19,
            "sizes": sizes,
            "tags": ["spicy", "vegetarian"],
        },
    ]

    await db.categories.delete_many({})
    await db.pizzas.delete_many({})
    await db.carts.delete_many({})
    await db.orders.delete_many({})

    await db.categories.insert_many(categories)
    await db.pizzas.insert_many(pizzas)
    client.close()
    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
