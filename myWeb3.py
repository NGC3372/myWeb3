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
    def initAccount(self , privateKey = None):
        if privateKey is None:
            self.account = self.ETH.account.privateKeyToAccount('DDA1EC2A2312151AC7D82CB9842B72C93EDCAD903B44A185387CD53FD2C29625')
        else:
            self.account = self.ETH.account.privateKeyToAccount(privateKey)
    #发起交易
    def makeTransaction(self , to_: str, value: int, gasPrice = None , gasLimit = None):
        if gasPrice is None:
            gasPrice = self.defaultGasPrice
        if gasLimit is None:
            gasLimit = 200000
        nonce = self.ETH.getTransactionCount(self.account.address)
        transaction = {
            'to': to_,
            'value': value,
            'gas': gasLimit,
            'gasPrice': gasPrice,
            'chainId': self.chainID,
            'nonce': nonce
        }
        signedTx = self.account.sign_transaction(transaction)
        hashTx = self.ETH.sendRawTransaction(signedTx.rawTransaction).hex()
        return hashTx
    #建立合约  web3.contract.ContractConstructor
    def createContract(self , byteCode:str , ABI:str ,*constructArgs):
        CONTRACT = self.ETH.contract(abi=ABI, bytecode=byteCode).constructor(constructArgs)
        return CONTRACT
    #部署合约
    def deployContract(self ,contract , gasPrice = None ,gasLimit = None ):
        if gasPrice is None :
            gasPrice = self.defaultGasPrice
        if gasLimit is None:
            gasLimit = 3000000
        nonce = self.ETH.getTransactionCount(self.account.address)
        transaction = contract.buildTransaction({
            'nonce':nonce,
            'gasPrice': gasPrice,
            'gas': gasLimit,
        })
        signedTx = self.account.signTransaction(transaction)
        hashTx = self.ETH.sendRawTransaction(signedTx.rawTransaction).hex()
        contractAddress =  self.ETH.waitForTransactionReceipt(hashTx)['contractAddress']
        return {'hashTx' : hashTx , 'contractAddress':contractAddress}
    #获取合内置函数
    def getContractFunction(self , contractAddress:str , ABI:str , functionName : str):
        contract = self.ETH.contract(address=contractAddress ,abi=ABI)
        function = contract.find_functions_by_name(functionName)[0]
        return function
    #调用合约内置函数transcation
    def transcationContractFunction(self , function , gasPrice = None , value = None , gasLimit = None):
        if gasPrice is None:
            gasPrice = self.defaultGasPrice
        if value is None:
            value = 0
        if gasLimit is None:
            gasLimit = 200000
        nonce = self.ETH.getTransactionCount(self.account.address)
        function_txn = function.buildTransaction({
            'gas': gasLimit,
            'gasPrice': gasPrice,
            'nonce': nonce,
            'value': value
        })
        signed_txn = self.account.sign_transaction(function_txn)
        hashTx = self.ETH.sendRawTransaction(signed_txn.rawTransaction).hex()
        return hashTx
    #调用合约内置函数call  
    def callContractFunction(self , function):
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
