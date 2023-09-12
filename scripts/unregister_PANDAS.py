# bash:   brownie run ./scripts/unregister_PANDAS.py main <account> 

import json
import brownie
import enum             

# ************************************************************************************************************************************************************************************
# ************************************************************************************************************************************************************************************
# ************************************************************************************************************************************************************************************
# ADJUST ONLY IN THIS SECTION !!!

# Set initial token supply and minimum token stake
INITIAL_SUPPLY = 100 * 10 ** 18                         # initial supply is 100 Token with 18 decimals     # <-- UPDATE

# Addresses of the deployed tokens. Copy addresses from mytoken.txt or paste manually from explorers
MYTOKENS = {
0: "0x8ffB1672Eb4C54F4d92A8B33548aEAfB3E673208",
1: "0x182d8b756A0249c506c4967a82050B3A35DAc531",
3: "0xf6940fBa20d23E3ef0b0Fc1740e40aa5D87AFE7B",
5: "0xb9f2f6C97182fe6670c604Df5da35D5C38F078F6",
6: "0x5ceCc8CfE5CCd7b00F5c8c2EA4F4ae21789822bD",
7: "0x811263E1B76b359b4f693A2A088F8521084e1C5E",
8: "0xDDaB737E6be36f44dDe9d7Dc5CA33deE8FC325Ab"
    }

# ADJUST !!! List of Networks to connect. Please adjust the entries to match your values in network-config.yaml. You can get the list using command "brownie networks list"
MYNETWORKS = {

    0: "goerli-test",       # ETHEREUM Görli        
    1: "bnb-test",          # BNB Chain             
    3: "avax-test",         # AVALANCHE Fuji        
    5: "polygon-test",      # POLYGON MUMBAI        
    6: "cronos-test",       # CRONOS                
    7: "fantom-test",       # FANTOM                
    8: "celo-test"          # CELO ALFAJORES        
    }


PRIORITY_FEE = '50 gwei' 

# END OF ADJUSTMENT SECTION
# ************************************************************************************************************************************************************************************
# ************************************************************************************************************************************************************************************
# ************************************************************************************************************************************************************************************

# DO NOT ADJUST !!! List of New Pantos Hubs. Forwarders are derived directly from chains.

PANTOS_HUBS = {
    0: "0x89C8B8458A1ac9E07096770D2261634a3f13d781",         # ETHEREUM Görli
    1: "0xFB37499DC5401Dc39a0734df1fC7924d769721d5",         # BNB Chain
    3: "0xbafFb84601BeC1FCb4B842f8917E3eA850781BE7",         # AVALANCHE Fuji
    5: "0x5C4B92cd0A956dedc14AF31fD474931540D8277B",         # POLYGON MUMBAI
    6: "0x0cfb3c7c11a33bef124a9d86073e73932b9abf90",         # CRONOS
    7: "0x4BC6A71D4C3D6170d0Db849fE19b8DbA18f1a7F5",         # FANTOM
    8: "0x8389B9A7608dbf52a699b998f309883257923C0E"          # CELO ALFAJORES
    }

# Colors for Output
class pcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Blockchain IDs according Pantos IDs

class Blockchain(enum.IntEnum):
    ETHEREUM = 0
    BNB_CHAIN = 1
    AVALANCHE = 3
    # SOLANA = 4
    POLYGON = 5
    CRONOS = 6
    FANTOM = 7
    CELO = 8



def main(account_name: str) -> None:
 
     # loading Hub abi data
    with open('./ABI/pantos_hub_abi.json', 'r') as f:
        pantos_hub_abi_data = json.loads(f.read())

    ### loading Forwarder abi data
    with open('./ABI/pantos_forwarder_abi.json', 'r') as f:
        pantos_forwarder_abi_data = json.loads(f.read())

    # loading Pantos Token abi data
    with open('./ABI/pantos_token_abi.json', 'r') as f:
        pantos_token_abi_data = json.loads(f.read())
 
    print("*********************************************************")
    print("***                                                   ***")
    print("***               PANDAS Token unregister             ***")
    print("***                                                   ***")
    print("*********************************************************")
    print()




    brownie.network.gas_price('auto')
    brownie.network.priority_fee(PRIORITY_FEE)
    # Load the specified account
    account = brownie.accounts.load(account_name)
    transaction_parameters = {'from': account}

    for blockchain in Blockchain:

        if brownie.network.is_connected()==True:
            brownie.network.disconnect()
        # Check if network is in MYNETWORKS list before connecting 
        if MYNETWORKS.get(blockchain.value)==None or MYNETWORKS.get(blockchain.value)=='':
            print("Network for ",f"{pcolors.FAIL}",blockchain,f"{pcolors.ENDC}"," not available")
        else:
            try:
                brownie.network.connect(MYNETWORKS[blockchain.value])
            except ValueError as error:
                print(f"{pcolors.FAIL}Value Error: {pcolors.ENDC}",blockchain)
            if brownie.network.is_connected()==False:
                print(f"{pcolors.FAIL}Failed to connect to {pcolors.ENDC}",blockchain)
            else:
                print("Connected to: ",f"{pcolors.OKBLUE}",brownie.network.show_active()," (",brownie.web3.chain_id,")",f"{pcolors.ENDC}")
 
                # get token contracts
                if MYTOKENS[blockchain.value]=="":
                    print(f"{pcolors.FAIL}No token deployed on {pcolors.ENDC}",blockchain)
                else:
                    print("Collecting data ...      ", end="")
                    try:
                        my_pandas_token = brownie.Contract.from_abi("PantosToken", MYTOKENS[blockchain.value], pantos_token_abi_data['abi']) 
                    except ValueError as error:
                        print(f"{pcolors.FAIL}Value Error: {pcolors.ENDC}","Invalid address")
                    else:

                        # Connect to the Pantos Hub of the connected chain
                        PantosHub = brownie.Contract.from_abi("PantosHub", PANTOS_HUBS[blockchain.value], pantos_hub_abi_data['abi'])

                        # Unregister Token on old Hubs, reverse external registrations, return staked PANs
                        PantosHub.unregisterToken(my_pandas_token.address, transaction_parameters) 
         
    print("*** FINISHED ***")
            
    if brownie.network.is_connected()==True:
            brownie.network.disconnect()
                        

