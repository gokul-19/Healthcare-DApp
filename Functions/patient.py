from web3 import Web3

class Main:
    def __init__(self, address, compiled_contract, private_key):
        self.web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Ganache provider
        self.address = Web3.to_checksum_address(address)
        self.private_key = private_key

        self.abi = compiled_contract["abi"]
        self.bytecode = compiled_contract["bytecode"]
        self.contract_address = Web3.to_checksum_address(compiled_contract["networks"]["1337"]["address"])
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def get_my_report(self):
        return self.contract.functions.getPatientReport(self.address).call()
