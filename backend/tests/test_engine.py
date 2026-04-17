import unittest
from engine.order import Order
from engine.order_book import OrderBook


class TestMatchingEngine(unittest.TestCase):

    def setUp(self):
        self.book = OrderBook("AAPL")

    # ----------------------------
    # 1. BASIC MATCHING TEST
    # ----------------------------
    def test_simple_match(self):
        buy = Order("1", "user1", "AAPL", "BUY", 100, 10)
        sell = Order("2", "user2", "AAPL", "SELL", 100, 10)

        self.book.add_order(buy)
        self.book.add_order(sell)

        self.assertEqual(len(self.book.trades), 1)

        trade = self.book.trades[0]
        self.assertEqual(trade.quantity, 10)
        self.assertEqual(trade.price, 100)

    # ----------------------------
    # 2. PRICE PRIORITY TEST
    # ----------------------------
    def test_price_priority(self):
        buy = Order("1", "user1", "AAPL", "BUY", 105, 10)
        sell1 = Order("2", "user2", "AAPL", "SELL", 100, 10)
        sell2 = Order("3", "user3", "AAPL", "SELL", 99, 10)

        self.book.add_order(buy)
        self.book.add_order(sell1)
        self.book.add_order(sell2)

        # should match best (lowest price sell first)
        self.assertLessEqual(self.book.trades[0].price, 100)

    # ----------------------------
    # 3. PARTIAL FILL TEST
    # ----------------------------
    def test_partial_fill(self):
        buy = Order("1", "user1", "AAPL", "BUY", 100, 10)
        sell = Order("2", "user2", "AAPL", "SELL", 100, 4)

        self.book.add_order(buy)
        self.book.add_order(sell)

        self.assertEqual(len(self.book.trades), 1)

        trade = self.book.trades[0]
        self.assertEqual(trade.quantity, 4)

        # buy order should still have remaining quantity
        remaining_buy = self.book.buy_orders[0]
        self.assertEqual(remaining_buy.quantity, 6)

    # ----------------------------
    # 4. NO MATCH WHEN PRICE DOESN'T CROSS
    # ----------------------------
    def test_no_match(self):
        buy = Order("1", "user1", "AAPL", "BUY", 95, 10)
        sell = Order("2", "user2", "AAPL", "SELL", 100, 10)

        self.book.add_order(buy)
        self.book.add_order(sell)

        self.assertEqual(len(self.book.trades), 0)
        self.assertEqual(len(self.book.buy_orders), 1)
        self.assertEqual(len(self.book.sell_orders), 1)

    # ----------------------------
    # 5. PRICE-TIME PRIORITY TEST
    # ----------------------------
    def test_time_priority(self):
        buy1 = Order("1", "user1", "AAPL", "BUY", 100, 10)
        buy2 = Order("2", "user2", "AAPL", "BUY", 100, 10)

        sell = Order("3", "user3", "AAPL", "SELL", 100, 10)

        self.book.add_order(buy1)
        self.book.add_order(buy2)
        self.book.add_order(sell)

        # first order should fill first (buy1)
        self.assertEqual(self.book.trades[0].buy_order_id, "1")


if __name__ == "__main__":
    unittest.main()