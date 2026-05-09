from app.business.cart_service import CartService


def test_compute_totals_returns_subtotal():
    result = CartService._compute_totals(
        "user-1",
        [
            {"item_id": "a", "unit_price": 10.0, "quantity": 2},
            {"item_id": "b", "unit_price": 5.5, "quantity": 1},
        ],
    )
    assert result["user_id"] == "user-1"
    assert len(result["items"]) == 2
    assert result["subtotal"] == 25.5
