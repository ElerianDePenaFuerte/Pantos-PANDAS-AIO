# PANTOS PANDAS All-in-One scripts

![version](https://img.shields.io/badge/version-1.0.0-blue)

This package includes scripts to deploy, register, unregister and migrate PANDAS tokens not created with the Pantos Tokencreator. These scripts can be used for any PANDAS token you are a registered owner.

## 1. Prerequisites
  * _python_ (version `3.6 or later`) including _package installer for python (pip)_
  * _brownie_
  * added _private keys_ to brownie
  * insure that the testnetworks Goerli, BNB, Fuji, Mumbai, Cronos, Fantom and Alfajores are included in your _network-config.yaml_
  * enough _Test coins_ on each chain for gas
  * _1.000 PAN_ per chain in case you wish to deploy/register tokens with the Pantos Hub

  For detailed instructions, please also check the step-by-step instructions of @kurzi2704 https://github.com/kurzi2704/pantos-pandas-creator/tree/main

## 2. Deploy PANDAS tokens
### 2.1 Adjust PANDASTOKEN.sol in /contracts folder

You need to set `_NAME` `_SYMBOL` and `_DECIMALS` for your token.
```solidity
...
contract PANDASTOKEN is PantosBaseToken, ERC20Burnable, ERC20Pausable {
    string private constant _NAME = "PANDAS";
    string private constant _SYMBOL = "PANDAS";
    uint8 private constant _DECIMALS = 18;
...
```

### 2.2 Adjust deploy_PANDAS.py in /scripts folder

The initial supply (number of topkens minted on each chain) can be set in the `_INITIAL_SUPPLY_` variable. Decimals depend on the settings of your token contract.
You need to copy/paste the network names of the Pantos compatible chains from your `_network-config.yaml_` in the MYNETWORKS directory (line 30ff)
Please do not change the index keys, since these are fixed assigned by Pantos as ChainIDs. 

```python
...
INITIAL_SUPPLY = 100 * 10 ** 18                         # initial supply is 100 Token with 18 decimals     # <-- UPDATE
...
MYNETWORKS = {

    0: "goerli-test",       # ETHEREUM Görli        
    1: "bnb-test",          # BNB Chain             
    3: "avax-test",         # AVALANCHE Fuji        
    5: "polygon-test",      # POLYGON MUMBAI        
    6: "cronos-test",       # CRONOS                
    7: "fantom-test",       # FANTOM                
    8: "celo-test"          # CELO ALFAJORES        
    }
...
```
### 2.3 Deploy

```shell 
brownie run ./scripts/deploy_PANDAS.py main <account> 
```

You will be asked for a password and the script will deploy the token on each chain defined in the `MYNETWORKS` directory.
The entire deploy process includes:
* mint of the token on each chain
* approve of PAN tokens for the PantosHub on each chain
* registration of the token with the PantosHub on each chain including PAN stake (1.000 PAN per chain and token)
* setPantosForwarder on each chain
* external registrations on each chain

After the script is finished your tokens are fully PANDAS enabled and can be used for multichain transfers immediately.

The contract addresses of your tokens will be saved in a 'myTokens.txt' file

## 3. External Registration of PANDAS tokens 

In case you are facing troubles with the external registrations, you can use the script `register_external_PANDAS.py` 

You just need to adjust the MYTOKENS directory in the script, containing the addresses your tokens are deployed at (i.e. from the myTokens.txt)

```shell 
brownie run ./scripts/register_external_PANDAS.py main <account> 
```

## 4. De-Registration of PANDAS tokens 

This step will unregister your tokens from the PantosHub. As a consequence, all external registrations are deleted as well and your PAN stake is returned to your wallet.

You just need to adjust the MYTOKENS directory in the script, containing the addresses your tokens are deployed at (i.e. from the myTokens.txt)

```shell 
brownie run ./scripts/unregister_PANDAS.py main <account> 
```

## 4. Migration of PANDAS tokens 

In case the Pantos contracts change (i.e. Forwarder, Hub, Token), this script can be used to migrate your PANDAS token to the new contracts. The script will
* un-register your token on the old contracts & release the PAN stake
* register your token again with the new contracts. 

You just need to adjust the MYTOKENS directory in the script, containing the addresses your tokens are deployed at (i.e. from the myTokens.txt)

```shell 
brownie run ./scripts/migrate_PANDAS.py main <account> 
```
