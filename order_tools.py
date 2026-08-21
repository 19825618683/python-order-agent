ORDERS = [
    {"id": 101, "amount": 59.9, "user": "小王"},
    {"id": 102, "amount": 235.5, "user": "小李"},
    {"id": 103, "amount": 500, "user": "小张"},
]


def get_order_summary(minimum_amount: float) -> dict:
    """返回金额不少于指定门槛的订单统计信息。"""
    matched_orders = [order for order in ORDERS if order["amount"] >= minimum_amount]

    return {
        "minimum_amount": minimum_amount,
        "count": len(matched_orders),
        "total": sum(order["amount"] for order in matched_orders),
        "users": [order["user"] for order in matched_orders],
    }

def get_order_by_id(order_id: int) -> dict:
    for order in ORDERS:
        if order["id"] == order_id:
            return order

    return {"error": f"未找到编号为 {order_id} 的订单"}