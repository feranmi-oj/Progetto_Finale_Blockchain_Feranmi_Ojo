from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/910777d67da84f3a892275bf6d5fc5e9'))
    address = '0xdf853B6F6B1b556c2fCa575eBe1D1f3F22ff5198'
    privateKey = '0x877839354cec6d1c922ac71a4bc8f75a41092bc0d589b18f0a7601a0d5c6696d'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)

    tx=w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId