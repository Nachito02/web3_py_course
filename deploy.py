from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os


load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# compilar
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]


provider = os.getenv("HTTPProvider")

w3 = Web3(Web3.HTTPProvider(provider))
chain_id = 11155111

my_adress = "0xCb5751E0bC332373597D5945e2E0E625FAfB1346"


private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

print(SimpleStorage)


# Nonce
nonce = w3.eth.get_transaction_count(my_adress)

# 1. Construir la transaccion

transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_adress,
        "nonce": nonce,
    }
)

# 2. Firmar la transaccion

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print(signed_txn)

# 3. Enviar la transaccion

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("Waitin for transaction to finish....")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# print(tx_receipt.contractAddress)

# Working with deployed contracts

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simula un llamado para obtener un valor.
print(simple_storage.functions.retrieve().call())

# Transact

store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_adress,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

print("Updating stored value")

t_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(t_hash)

print(simple_storage.functions.retrieve().call())
