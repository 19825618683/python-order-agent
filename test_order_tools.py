import unittest

from order_tools import get_order_by_id, get_order_summary


class OrderToolsTest(unittest.TestCase):
    def test_query_existing_order(self):
        order = get_order_by_id(102)

        self.assertEqual(order["user"], "小李")
        self.assertEqual(order["amount"], 235.5)

    def test_query_missing_order(self):
        result = get_order_by_id(999)

        self.assertIn("error", result)

    def test_order_summary(self):
        result = get_order_summary(200)

        self.assertEqual(result["count"], 2)
        self.assertEqual(result["users"], ["小李", "小张"])


if __name__ == "__main__":
    unittest.main()
