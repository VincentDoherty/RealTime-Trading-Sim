from engine.order import Order
from engine.trade import Trade
from copy import deepcopy


class OrderBook:
    """
    Maintain a simple limit-order book for a single trading symbol and match orders
    using price-time priority.

    The order book stores active buy and sell orders separately, keeps them sorted
    for best execution, and records executed trades. Buy orders are sorted by
    descending price then earliest timestamp; sell orders are sorted by ascending
    price then earliest timestamp.

    When a new order is added, it is copied into the book and immediately matched
    against the opposite side while the best bid crosses or equals the best ask.
    Trades are executed at the resting sell price, and partial fills are supported
    by decrementing order quantities until one or both orders are fully filled.

    Attributes:
        symbol: Trading symbol handled by this order book.
        buy_orders: List of active buy orders sorted by best price/time priority.
        sell_orders: List of active sell orders sorted by best price/time priority.
        trades: List of executed trades in the order they occurred.

    Methods:
        add_order(order): Add an order to the book and trigger matching.
        match_orders(): Match the top buy and sell orders while they are crossable.

    Notes:
        This implementation assumes order objects provide at least the following
        fields: id, side, price, quantity, and timestamp. Trade objects are created
        with an incrementing identifier based on the number of recorded trades.
    """
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.buy_orders = []
        self.sell_orders = []
        self.trades = []

    def add_order(self, order: Order):
        if order.side == "BUY":
            self.buy_orders.append(deepcopy(order))
            self.buy_orders.sort(key=lambda x: (-x.price, x.timestamp))
        else:
            self.sell_orders.append(deepcopy(order))
            self.sell_orders.sort(key=lambda x: (x.price, x.timestamp))

        self.match_orders()

    def match_orders(self):
        i = 0

        while self.buy_orders and self.sell_orders:
            buy = self.buy_orders[0]
            sell = self.sell_orders[0]

            if buy.price < sell.price:
                break

            trade_qty = min(buy.quantity, sell.quantity)

            trade = Trade(
                id=f"trade_{len(self.trades)+1}",
                buy_order_id=buy.id,
                sell_order_id=sell.id,
                symbol=self.symbol,
                price=sell.price,
                quantity=trade_qty
            )

            self.trades.append(trade)

            # update quantities safely
            buy.quantity -= trade_qty
            sell.quantity -= trade_qty

            # remove fully filled orders
            if buy.quantity == 0:
                self.buy_orders.pop(0)
            if sell.quantity == 0:
                self.sell_orders.pop(0)
                
    def get_recent_trades(self, limit=None):
        if limit is None:
            return self.trades.copy()
        
        return self.trades[-limit:].copy()
    
    def get_last_trade_price(self):
        if not self.trades:
            return None
        return self.trades[-1].price
    
    def get_trade_count(self):
        return len(self.trades)