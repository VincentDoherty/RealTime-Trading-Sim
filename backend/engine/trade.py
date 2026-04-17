from dataclasses import dataclass
import time

@dataclass
class Trade:
    id: str
    buy_order_id: str
    sell_order_id: str
    symbol: str
    price: float
    quantity: int
    timestamp: float = time.time()