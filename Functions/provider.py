from web3 import Web3

class Provider:
    def __init__(self, address, compiled_contract, private_key):
        self.web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Ganache
        self.address = Web3.to_checksum_address(address)
        self.private_key = private_key

        self.abi = compiled_contract["abi"]
        self.bytecode = compiled_contract["bytecode"]
        self.contract_address = Web3.to_checksum_address(compiled_contract["networks"]["1337"]["address"])
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def register_patient_record(self, patient_address, report_hash):
        nonce = self.web3.eth.get_transaction_count(self.address)

        txn = self.contract.functions.registerPatientRecord(
            patient_address,
            report_hash
        ).build_transaction({
            "chainId": 1337,
            "gas": 300000,
            "gasPrice": self.web3.to_wei("20", "gwei"),
            "nonce": nonce
        })

        signed_txn = self.web3.eth.account.sign_transaction(txn, self.private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
        return receipt

    def get_patient_record(self, patient_address):
        return self.contract.functions.getPatientReport(patient_address).call()
