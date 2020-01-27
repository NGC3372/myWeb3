from  web3 import Web3 ,HTTPProvider


class myWeb3:
    #对象初始化
    def __init__(self , web3Provider = None , chainID = None):
        if web3Provider is None:
            web3Provider = 'https://ropsten.infura.io/v3/83b3315113a246e88abb1268847b4a5b'
            chainID = 3
        self.chainID = chainID
        self.w3 = Web3(HTTPProvider(web3Provider))
        self.ETH = self.w3.eth
        self.defaultGasPrice = self.ETH.gasPrice
        self.initAccount()
    #初始化账户     
    def initAccount(self , address = None , privateKey = None):
        if address is None:
            self.address = '0x76e0eC050466c4dddBbAA25C3f069C18F026AF95'
            self.privateKey = 'DDA1EC2A2312151AC7D82CB9842B72C93EDCAD903B44A185387CD53FD2C29625'
        else:
            self.address = address
            self.privateKey = privateKey 
    #发起交易        
    def makeTransaction(self , to_ : str, value : int, gasPrice = None):
        if gasPrice is None:
            gasPrice = self.defaultGasPrice
        nonce = self.ETH.getTransactionCount(self.address)
        transaction = {
            'to': to_,
            'value': value,
            'gas': 200000,
            'gasPrice': gasPrice,
            'chainId': 3,
            'nonce': nonce
        }
        signedTx = self.ETH.account.sign_transaction(transaction , self.privateKey)
        hashTx = self.ETH.sendRawTransaction(signedTx.rawTransaction).hex()
        return hashTx
    #部署合约
    def deployContract(self , byteCode : str, gasPrice = None):
        if gasPrice is None :
            gasPrice = self.defaultGasPrice
        nonce = self.ETH.getTransactionCount(self.address)
        transaction = {
            'nonce':nonce,
            'gasPrice': gasPrice,
            'gas': 3000000,
            'data':byteCode
        }   
        signedTx = self.ETH.account.signTransaction(transaction, self.privateKey)
        hashTx = self.ETH.sendRawTransaction(signedTx.rawTransaction).hex()
        contractAddress =  self.ETH.waitForTransactionReceipt(hashTx)['contractAddress']
        return {'hashTx' : hashTx , 'contractAddress':contractAddress}
    #获取合内置函数
    def getContractFunction(self , contractAddress , ABI , functionName : str):
        contract = self.ETH.contract(address=contractAddress ,abi=ABI)
        function = contract.functions[functionName]
        return function
    #调用合约内置函数
    def runContractFunction(self , useGas : bool , function , gasPrice = None):
        if useGas :
            if gasPrice is None:
                gasPrice = self.defaultGasPrice
            nonce = self.ETH.getTransactionCount(self.address)
            function_txn = function.buildTransaction({
                'chainId':3,
                'gas': 70000,
                'gasPrice': gasPrice,
                'nonce': nonce
            })
            signed_txn = self.ETH.account.sign_transaction(function_txn, private_key = self.privateKey)
            hashTx = self.ETH.sendRawTransaction(signed_txn.rawTransaction).hex()
            return hashTx
        else:
            result = function.call()
            return result
    #获取账户余额
    def getBalance(self , address = None):
        if address is None:
            address = self.address
        balance = self.ETH.getBalance(address)    
        return balance 
    #获取交易收据的详细信息
    def getReceiptInfoFromHash(self , hashTx : str):
        info = self.ETH.getTransactionReceipt(hashTx)
        return info   
    #获取交易详细信息     
    def getTransactionInfoFromHash(self , hashTx : str):
        info = self.ETH.getTransaction(hashTx)
        return info
