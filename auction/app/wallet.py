from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/910777d67da84f3a892275bf6d5fc5e9'))

account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your address : {address} \n Your key: {privateKey}")