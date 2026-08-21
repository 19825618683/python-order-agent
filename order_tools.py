import json
from pathlib import Path


ORDERS_FILE = Path(__file__).with_name("orders.json")


def load_orders() -> list[dict]:
    try:
        with ORDERS_FILE.open(encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise RuntimeError(f"找不到订单数据文件：{ORDERS_FILE}")
    except json.JSONDecodeError as error:
        raise RuntimeError(f"订单数据文件格式错误：{ORDERS_FILE}") from error


ORDERS = load_orders()


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