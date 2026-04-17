import time


class Metrics:
    def __init__(self):
        self.latencies = []
        self.total_orders = 0

    def record_latency(self, start, end):
        self.latencies.append(end - start)
        self.total_orders += 1

    def summary(self, orderbook):
        executed_volume = sum(t.quantity for t in orderbook.trades)

        remaining_volume = sum(
            o.quantity for o in orderbook.buy_orders + orderbook.sell_orders
        )

        total_volume = executed_volume + remaining_volume

        avg_latency = (
            sum(self.latencies) / len(self.latencies)
            if self.latencies else 0
        )

        return {
            "orders_processed": self.total_orders,
            "trades": len(orderbook.trades),
            "executed_volume": executed_volume,
            "remaining_volume": remaining_volume,
            "total_volume": total_volume,
            "avg_latency_ms": avg_latency * 1000,
        }