import ccxt.pro
from asyncio import gather, run
import random

bid_prices = {}
ask_prices = {}

async def symbol_loop(exchange, symbol):
    global bid_prices
    global ask_prices
    
    print('starting the', exchange.id, 'symbol loop with', symbol)
    
    while True:
        try:
            orderbook = await exchange.watch_order_book(symbol)
            now = exchange.milliseconds()

            bid_prices[exchange.id] = orderbook['bids'][0][0]
            ask_prices[exchange.id] = orderbook['asks'][0][0]
            
            if len(bid_prices) >= 2 and len(ask_prices) >= 2:
                min_ask_ex = min(ask_prices, key=ask_prices.get)
                max_bid_ex = max(bid_prices, key=bid_prices.get)
                min_ask_price = ask_prices[min_ask_ex]
                max_bid_price = bid_prices[max_bid_ex]
                best_diff = max_bid_price - min_ask_price
                best_diff_pct = ((max_bid_price - min_ask_price) / min_ask_price) * 100
                
                if best_diff_pct > 0.001 and random.randint(0, 200) == 10:
                    print(f"{exchange.iso8601(now)}: Buy SOL/USDT on {min_ask_ex} ({min_ask_price}$), Sell SOL/USDT on {max_bid_ex} ({max_bid_price}$) / Profit: {best_diff_pct:.4f}%")
                   # print(exchange.iso8601(now), "bid prices:", bid_prices)
                   # print(exchange.iso8601(now), "ask prices:", ask_prices)
                   # print(f"Buy on {min_ask_ex} at {min_ask_price}, Sell on {max_bid_ex} at {max_bid_price}")
                 
                    
        except Exception as e:
            print(f"Error in {exchange.id}: {str(e)}")
            break

async def exchange_loop(exchange_id, symbols):
    print('starting the', exchange_id, 'exchange loop with', symbols)
    exchange = getattr(ccxt.pro, exchange_id)()
    loops = [symbol_loop(exchange, symbol) for symbol in symbols]
    await gather(*loops)
    await exchange.close()

async def main():
    exchanges = {
        'okx': ['SOL/USDT'],
        'kucoin': ['SOL/USDT'],
        'binance': ['SOL/USDT'],
        'kraken': ['SOL/USDT'],
        'bitget': ['SOL/USDT'],
        'gate': ['SOL/USDT'],
        'mexc': ['SOL/USDT'],
        'coinbase': ['SOL/USDT'],
        'dydx': ['SOL/USDT'],
        'bybit': ['SOL/USDT'],
    }
    loops = [exchange_loop(exchange_id, symbols) for exchange_id, symbols in exchanges.items()]
    await gather(*loops)

run(main())






