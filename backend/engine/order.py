from dataclasses import dataclass
import time

@dataclass
class Order:
    id: str
    user_id: str
    symbol: str
    side: str  # "BUY" or "SELL"
    price: float
    quantity: int
    timestamp: float = time.time()