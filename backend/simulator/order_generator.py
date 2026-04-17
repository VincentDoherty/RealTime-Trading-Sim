import random
from engine.order import Order
from .config import SimulationConfig


class OrderGenerator:
    def __init__(self):
        #make the randomness deterministic for reproducibility
        random.seed(SimulationConfig.RANDOM_SEED)

        self.current_price = SimulationConfig.STARTING_PRICE
        self.timestamp = 0
        self.traders = [
            f"user_{i}" for i in range(SimulationConfig.TRADER_COUNT)
        ]
        self.order_id = 0
        
    #simulate time
    def _next_timestamp(self):
        self.timestamp += 1
        return self.timestamp

    def _choose_side(self):
        return "BUY" if random.random() < 0.52 else "SELL"

    def _update_price(self):
        move = random.gauss(0, SimulationConfig.VOLATILITY)
        self.current_price += move
        return round(self.current_price, 2)

    def _choose_quantity(self):
        r = random.random()

        if r < 0.8:
            return random.randint(1, 10)
        elif r < 0.95:
            return random.randint(10, 50)
        else:
            return random.randint(50, SimulationConfig.MAX_QTY)

    def generate_order(self):
        self.order_id += 1

        return Order(
            id=str(self.order_id),
            user_id=random.choice(self.traders),
            symbol=SimulationConfig.SYMBOL,
            side=self._choose_side(),
            price=self._update_price(),
            quantity=self._choose_quantity(),
            timestamp=self._next_timestamp(),
        )

    def generate_orders(self, n):
        return [self.generate_order() for _ in range(n)]