# bash:   brownie run ./scripts/migrate_PANDAS.py main <account> 

import json
import brownie
import enum             

# ************************************************************************************************************************************************************************************
# ************************************************************************************************************************************************************************************
# ************************************************************************************************************************************************************************************
# ADJUST ONLY IN THIS SECTION !!!

# ADJUST !!! Addresses of the PANDAS Tokens to migrate. In case your PANDAS is not deployed on a specific chain, please delete the entry
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

# DO NOT ADJUST !!! List of New Pantos Hubs. Old Hubs, Old Forwarders and New Forwarders are derived directly from chains.

PANTOS_HUBS_NEW = {
    0: "0x89C8B8458A1ac9E07096770D2261634a3f13d781",         # ETHEREUM Görli
    1: "0xFB37499DC5401Dc39a0734df1fC7924d769721d5",         # BNB Chain
    3: "0xbafFb84601BeC1FCb4B842f8917E3eA850781BE7",         # AVALANCHE Fuji
    5: "0x5C4B92cd0A956dedc14AF31fD474931540D8277B",         # POLYGON MUMBAI
    6: "0x0cfb3c7c11a33bef124a9d86073e73932b9abf90",         # CRONOS
    7: "0x4BC6A71D4C3D6170d0Db849fE19b8DbA18f1a7F5",         # FANTOM
    8: "0x8389B9A7608dbf52a699b998f309883257923C0E"          # CELO ALFAJORES
    }

PANTOS_HUBS_OLD = {
    0: "0xFB37499DC5401Dc39a0734df1fC7924d769721d5",         # ETHEREUM Görli
    1: "0xc306ba335f4fcbe4178e3e033fc1a90c17e71831",         # BNB Chain
    3: "0x64B9801BB96862027698928Bfdb970e69c0a73C3",         # AVALANCHE Fuji
    5: "0x64B9801BB96862027698928Bfdb970e69c0a73C3",         # POLYGON MUMBAI
    6: "0xC892F1D09a7BEF98d65e7f9bD4642d36BC506441",         # CRONOS
    7: "0xC892F1D09a7BEF98d65e7f9bD4642d36BC506441",         # FANTOM
    8: "0xC892F1D09a7BEF98d65e7f9bD4642d36BC506441"          # CELO ALFAJORES
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
    SOLANA = 4
    POLYGON = 5
    CRONOS = 6
    FANTOM = 7
    CELO = 8

    @staticmethod
    def from_name(name: str) -> 'Blockchain':
        """Find an enumeration member by its name.

        Parameters
        ----------
        name : str
            The name to search for.

        Raises
        ------
        NameError
            If no enumeration member can be found for the given name.

        """
        name_upper = name.upper()
        for blockchain in Blockchain:
            if name_upper == blockchain.name:
                return blockchain
        raise NameError(name)






def get_external_tokens(pantos_hub, pandas_token_address):
    registered_external_tokens = {}
    for blockchain in Blockchain:
        try:
            external_token_record = pantos_hub.getExternalTokenRecord(
                pandas_token_address, blockchain.value)
        except ValueError as error:
            raw_record_data = str(error).split(' - ')[0]
            if 'True' in raw_record_data:
                external_token_record = (
                    True, raw_record_data.split('True, \'')[1].split('\')')[0])
        if external_token_record[0]:                                                # DELETED and blockchain not in INACTIVE_BLOCKCHAINS:
            registered_external_tokens[blockchain] = external_token_record[1]

    return registered_external_tokens


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
    print("***               PANDAS Token migration              ***")
    print("***                                                   ***")
    print("***   Updating Hub, Forwarder & Token registrations   ***")
    print("***                                                   ***")
    print("*********************************************************")
    print()




    brownie.network.gas_price('auto')
    brownie.network.priority_fee(PRIORITY_FEE)
    account = brownie.accounts.load(account_name)
    transaction_parameters = {'from': account}




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

                if MYTOKENS[blockchain.value]=="":
                    print(f"{pcolors.FAIL}No token deployed on {pcolors.ENDC}",blockchain)
                else:
                    print("Collecting data ...      ", end="")
                    try:
                        my_pandas_token = brownie.Contract.from_abi("PantosToken", MYTOKENS[blockchain.value], pantos_token_abi_data['abi']) 
                    except ValueError as error:
                        print(f"{pcolors.FAIL}Value Error: {pcolors.ENDC}","Invalid address")
                    else:
                        old_forwarder= brownie.Contract.from_abi("PantosForwarder", my_pandas_token.getPantosForwarder(), pantos_forwarder_abi_data['abi'])
                        old_hub = brownie.Contract.from_abi("PantosHub", old_forwarder.getPantosHub(), pantos_hub_abi_data['abi'])

                        new_hub = brownie.Contract.from_abi("PantosHub", PANTOS_HUBS_NEW[blockchain.value], pantos_hub_abi_data['abi'])
                        new_forwarder= brownie.Contract.from_abi("PantosForwarder", new_hub.getPantosForwarder(), pantos_forwarder_abi_data['abi'])
                        pantos_token = brownie.Contract.from_abi("PantosToken", old_forwarder.getPantosToken(), pantos_token_abi_data['abi'])

                        external_tokens = get_external_tokens(old_hub, MYTOKENS[blockchain.value])      

                        _MINIMUM_TOKEN_STAKE = new_hub.getMinimumTokenStake()

                        print(f"{pcolors.OKGREEN}DONE{pcolors.ENDC}")
                        
                        print("Checking Hub Status ...  ")
                        print(PANTOS_HUBS_OLD[blockchain.value])
                        print(old_hub)



                        try:
                            old_hub.paused()
                        except:
                            print("  Old Hub: Paused")
                        else:
                            print("  Old Hub: Not Paused")
                            try:
                                new_hub.paused()
                            except:
                                print("  New Hub: Paused")
                            else:
                                print("  New Hub: Not Paused")

                                print()
                                print("Account: ",account)
                                print("Owner:   ",my_pandas_token.getOwner())
                                print()


                                print("unregister Token ...     ", end="")
                                old_hub.unregisterToken(my_pandas_token.address, transaction_parameters)                       # Unregister Token on old Hubs, reverse external registrations, return staked PANs
                                print(f"{pcolors.OKGREEN}DONE{pcolors.ENDC}")
                                print("Approve PAN .......      ", end="")
                                pantos_token.approve(new_hub.address, _MINIMUM_TOKEN_STAKE, transaction_parameters)            # Approve new Stake
                                print(f"{pcolors.OKGREEN}DONE{pcolors.ENDC}")
                                print("register Token .....     ", end="")
                                new_hub.registerToken(my_pandas_token.address, _MINIMUM_TOKEN_STAKE, transaction_parameters)   # Register Token on new Hub and deposit Stake
                                print(f"{pcolors.OKGREEN}DONE{pcolors.ENDC}")


                                

                                for external_token in external_tokens:
                                    try:
                                        record = new_hub.getExternalTokenRecord(my_pandas_token.address, external_token.value)
                                    except ValueError as error:
                                        record = [True] if ('True' in str(error)) else [False]
                                    if not record[0]:
                                        print("External Registration Chain ID: ", external_token.value)
                                        new_hub.registerExternalToken(my_pandas_token.address, external_token.value, external_tokens[external_token].encode('utf-8').strip(), transaction_parameters)
                                
                                print("External registrations.. ", end="") 
                                print(f"{pcolors.OKGREEN}DONE{pcolors.ENDC}")

                                print("Set New Forwarder....... ", end="")
                                my_pandas_token.setPantosForwarder(new_forwarder.address, transaction_parameters)
                                print(f"{pcolors.OKGREEN}DONE{pcolors.ENDC}")
                                print()
                                
                            
                            
                            
                            
                                brownie.network.disconnect() 






 



