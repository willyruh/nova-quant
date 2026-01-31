import threading
import time
from wrapper import IBWrapper
from client import IBClient
from contract import stock, future, options
from order import limit, BUY


class IBAPP(IBWrapper, IBClient):
    def __init__(self, ip, port, client_id):
        IBWrapper.__init__(self)
        IBClient.__init__(self, wrapper=self)
        self.connect(ip, port, client_id)
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        setattr(self, "thread", thread)


if __name__ == "__main__":
    app = IBAPP("127.0.0.1", 7497, client_id=11)
    eur = future("EUR", "CME", "202312")
    for tick in app.get_streaming_data(99, eur):
        print(tick)
    aapl = stock("AAPL", "SMART", "USD")
    gbl = future("GBL", "EUREX", "202403")
    pltr = options("PLTR", "BOX", "20240315", 20, "C")
    data = app.get_historical_data(
        request_id=99, contract=aapl, duration="2 D", bar_size="30 secs")
    data = app.get_market_data(requst_di=99, contract=aapl)
    limit_order = limit(BUY, 100, 190.00)
    time.sleep(30)
    app.disconect()
