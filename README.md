# LocalCoinSwap-API-Wrapper
Python Wrapper for the LocalCoinSwap API. This wrapper is currently incomplete and should be considered completely experimental, not ready for production, and merely a work in progress.

### **Using the Wrapper:**

1. Clone this repository into your project folder
2. Create ```.env``` file with your API key in the format ```TOKEN = "your_token"```
3. Import the modules from the wrapper directory as follows.

```from wrapper import trade, wallet, utils, notifs, offers, fiat```


### **Examples of Use:**

Send a message to your most recent trade:
```trade.send_message(trade.latest(), "Ready to Trade?")```

Get Total Portfolio Value: 
```wallet.total_value()```

Check Ethereum Wallet Balance: 
```wallet.balance("eth")```

Search Bitcoin Trade Offers for Specific User:
```offers.search(username="someone", ticker="BTC")```

... and much more, review the various modules for further possibilities


