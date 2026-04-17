import time

from engine.order_book import OrderBook
from .config import SimulationConfig
from .order_generator import OrderGenerator
from .metrics import Metrics


class MarketSimulator:
    def __init__(self):
        self.orderbook = OrderBook(SimulationConfig.SYMBOL)
        self.generator = OrderGenerator()
        self.metrics = Metrics()

    def run(self):
        print("Starting simulation...")

        orders = self.generator.generate_orders(
            SimulationConfig.NUM_ORDERS
        )

        for order in orders:
            start = time.perf_counter()

            self.orderbook.add_order(order)

            end = time.perf_counter()
            self.metrics.record_latency(start, end)

        self._validate()

        results = self.metrics.summary(self.orderbook)

        print("\n=== Simulation Results ===")
        for k, v in results.items():
            print(f"{k}: {v}")

    # --------------------------
    # Correctness Checks
    # --------------------------

    def _validate(self):
        self._check_no_negative_quantity()
        self._check_no_crossed_book()
        self._check_volume_conservation()

    def _check_no_negative_quantity(self):
        for o in (
            self.orderbook.buy_orders + self.orderbook.sell_orders
        ):
            assert o.quantity >= 0, "Negative quantity detected"

    def _check_no_crossed_book(self):
        if self.orderbook.buy_orders and self.orderbook.sell_orders:
            best_buy = max(o.price for o in self.orderbook.buy_orders)
            best_sell = min(o.price for o in self.orderbook.sell_orders)

            assert best_buy < best_sell, "Order book crossed!"

    def _check_volume_conservation(self):
        executed = sum(t.quantity for t in self.orderbook.trades)
        remaining = sum(
            o.quantity
            for o in self.orderbook.buy_orders
            + self.orderbook.sell_orders
        )

        assert executed + remaining > 0, "Volume mismatch"
        
if __name__ == "__main__":
    simulator = MarketSimulator()
    simulator.run()