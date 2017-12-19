#! /usr/bin/python3
 
import json
from web3 import Web3, RPCProvider
from operator import itemgetter
import time
import sys
import datetime
import math
 
//////////////////////// CONFIGURE//////////////////////////
markets = ["0x3aa927a97594c3ab7d7bf0d47c71c3877d1de4a1"]  //INSERT OASIS CONTRACT ADDRESS
acct_owner = "0x00Be16b62218AaF6f147D805A047B22D63B2DF71" //INSERT ADDRESS OF ACCOUNT TO USE HERE
////////////////////////////////////////////////////////////
 
web3rpc = Web3(RPCProvider(port=8545))
web3rpc.eth.defaultAccount = acct_owner
web3rpc.eth.defaultBlock = "latest"
 
with open('SimpleMarket.abi', 'r') as abi_file:
  abi_json = abi_file.read().replace('\n','')
abi = json.loads(abi_json)
 
for market in markets:
 
  print("Looking for orders in: %s" % (market), end="\r")
  market_contract = web3rpc.eth.contract(abi=abi, address=market)
 
  last_offer_id = market_contract.call().last_offer_id()
 
  if last_offer_id == 0:
    print("No orders found in market %s" % market)
    continue
 
  id = 0
 
  offers = []
  while id <  last_offer_id + 1:
    offers.append(market_contract.call().offers(id))
    id = id + 1
 
  id = 0
 
  for offer in offers:
    valid = offer[5]
    if valid:
      print("Canceling order id: %s from market %s" % (id, market), end="")
      result = market_contract.transact().cancel(id=id)
 
      while web3rpc.eth.getTransactionReceipt(result) is None:
       print(".", end='', flush=True)
       time.sleep(2)
      print("")
    id = id + 1