# bash:   brownie run ./scripts/deploy_PANDAS.py main <account> 

import json
import brownie
import enum             

from brownie import PANDASTOKEN     # Import your token with contract name "PANDASTOKEN" (Solidity script in folder /contracts/***.sol )

# ************************************************************************************************************************************************************************************
# ************************************************************************************************************************************************************************************
# ************************************************************************************************************************************************************************************
# ADJUST ONLY IN THIS SECTION !!!

# Set initial token supply and minimum token stake
INITIAL_SUPPLY = 100 * 10 ** 18                         # initial supply is 100 Token with 18 decimals     # <-- UPDATE

# Addresses of the deployed tokens. Filled during Deployment
MYTOKENS = {
    0: "0x0000000000000000000000000000000000000000",    # ETHEREUM Görli
    1: "0x0000000000000000000000000000000000000000",    # BNB Chain
    3: "0x0000000000000000000000000000000000000000",    # AVALANCHE Fuji 
    5: "0x0000000000000000000000000000000000000000",    # POLYGON MUMBAI
    6: "0x0000000000000000000000000000000000000000",    # CRONOS
    7: "0x0000000000000000000000000000000000000000",    # FANTOM
    8: "0x0000000000000000000000000000000000000000"     # CELO ALFAJORES
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
    print("***               PANDAS Token Deployment             ***")
    print("***                                                   ***")
    print("***   Deploy, Configure & Register Pandas Tokens      ***")
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

                # Connect to the Pantos Hub of the connected chain
                PantosHub = brownie.Contract.from_abi("PantosHub", PANTOS_HUBS[blockchain.value], pantos_hub_abi_data['abi'])
                # Get the Address of the PantosForwarder from the Hub
                PantosForwarder= brownie.Contract.from_abi("PantosForwarder", PantosHub.getPantosForwarder(), pantos_forwarder_abi_data['abi'])
                # Get the Address of the Pantos token from the Forwrder
                PantosToken = brownie.Contract.from_abi("PantosToken", PantosForwarder.getPantosToken(), pantos_token_abi_data['abi'])

                # Get the minimum Pantos Stake from the Pantos Hub.
                _MINIMUM_TOKEN_STAKE = PantosHub.getMinimumTokenStake()

                # Deploy the custom token contract and verify 
                myToken = PANDASTOKEN.deploy(INITIAL_SUPPLY, transaction_parameters) #, publish_source=True)    # <- publish_source = Verify Contract
                MYTOKENS[blockchain.value] = myToken.address

                # Set the Pantos forwarder address in the custom token contract
                myToken.setPantosForwarder(PantosForwarder.address, transaction_parameters)

                # Approve the PantosHub to spend the required minimum token stake
                PantosToken.approve(PantosHub.address, _MINIMUM_TOKEN_STAKE, transaction_parameters)

                # Register the custom token on the PantosHub
                PantosHub.registerToken(MYTOKENS[blockchain.value], _MINIMUM_TOKEN_STAKE, transaction_parameters)

    print("Deployed contracts (please also check myTokens.txt):")
    with open("myTokens.txt", 'w') as f: 
        for key, value in MYTOKENS.items(): 
            f.write(f"{key}: \"{value}\",\n")
            print(f"{key}: \"{value}\",\n")
            
    print("Finished Deployment ...      ")
    print("")
    print("Start External Registering ...      ")

    for blockchain in Blockchain:
        if brownie.network.is_connected()==True:
            brownie.network.disconnect()
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

                PantosHub = brownie.Contract.from_abi("PantosHub", PANTOS_HUBS[blockchain.value], pantos_hub_abi_data['abi'])
                for x in Blockchain:
                    if x == blockchain:
                        print("ID ",x.value,": *** IGNORED ***")
                    else:
                        PantosHub.registerExternalToken(MYTOKENS[blockchain.value], x.value, MYTOKENS[x].encode('utf-8').strip(), transaction_parameters)
                        print(MYTOKENS[blockchain.value]," --- ", x.value," --- ", MYTOKENS[x])
                                                
                print(f"{pcolors.OKGREEN}DONE{pcolors.ENDC}")
                print()
            
            
    print("*** FINISHED ***")
            
    if brownie.network.is_connected()==True:
            brownie.network.disconnect()
                        

