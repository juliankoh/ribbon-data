import requests
import json
import pandas as pd
from IPython import embed

VAULT_ETH_CALL = "0x0FABaF48Bbf864a3947bdd0Ba9d764791a60467A"
VAULT_BTC_CALL = "0x8b5876f5B0Bf64056A89Aa7e97511644758c3E8c"
VAULT_ETH_PUT = "0x16772a7f4a3ca291C21B8AcE76F9332dDFfbb5Ef"
URL = 'https://api.thegraph.com/subgraphs/name/kenchangh/ribbon-finance'

def get_depositors():
    query = """query {
        vaults {
            id
            name
            symbol
            totalPremiumEarned
            depositors
        }
    }"""

    r = requests.post(URL, json={'query': query})


    if r.status_code != 200:
        return
    
    else:
        json_data = json.loads(r.text)
        vaults = json_data['data']['vaults']
        return vaults

def get_multiple_vault_depositors(num):
    vaults = get_depositors()
    vault1 = set(vaults[0]['depositors'])
    vault2 = set(vaults[1]['depositors'])
    vault3 = set(vaults[2]['depositors'])

    if num == 1:
        return vault1.union(vault2).union(vault3)
    if num == 2:
        return vault1.intersection(vault2).union(vault2.intersection(vault3)).union(vault1.intersection(vault3))
    elif num == 3:
        return vault1.intersection(vault2).intersection(vault3)

def get_all_depositor_data():
    depositors = get_multiple_vault_depositors(3)
    
    for depositor in depositors:
        query = """query {
            vaultTransactions(
            where:{address:"%s"}, 
            orderBy: timestamp, 
            orderDirection: desc
            ) {
            id
            type
            vault {
                id
                symbol
            }
            amount
            address
            txhash
            timestamp
            }
        }""" % depositor
        
        r = requests.post(URL, json={'query': query})
        print(r.status_code)
        print(r.text)

embed()