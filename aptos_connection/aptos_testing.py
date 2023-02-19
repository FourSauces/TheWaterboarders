from aptos_sdk.account import Account
from aptos_sdk.client import FaucetClient, RestClient
import requests
import json


NODE_URL = "https://fullnode.testnet.aptoslabs.com/v1"
FAUCET_URL = "https://faucet.testnet.aptoslabs.com"


"""
priv key 0x3e029bf76b8c2d9c15f89d81d78fa0abf8e1769c8c58ce611cdda798fc4f93a2
pub key 0x880849c2e185240235e261ca3988ec41b9fb132bd7b82677ff7574263e2a7921
address = 0x122bb03ce2fbad828339215cb406eb21e3439e6651fcd4dc8b225da17fa4958d"""

privateKey = f"3e029bf76b8c2d9c15f89d81d78fa0abf8e1769c8c58ce611cdda798fc4f93a2"

def addVersionToLogs(version):
    f = open("processedversions.txt", "a")
    f.write(str(version)+"\n")
    f.close()



def getNextDepositVersion(receivingAddress):
    f = open("processedversions.txt", "r")
    read = f.read()
    f.close()
    output = requests.get(NODE_URL+"/accounts/"+str(receivingAddress)+"/events/0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>/deposit_events").text
    outputjson = json.loads(output)
    for transaction in outputjson:
        try:
            version = transaction["version"]
            if not(version in read):
                addVersionToLogs(version)
                return version
        except:
            print("error somewhere")
            print(transaction)
    return "" #we got nothing
    


def getDepositorAddress(version, receivingAddress):
    output = requests.get(NODE_URL+"/transactions/by_version/"+str(version)).text
    outputjson = json.loads(output)
    for change in outputjson["changes"]:
        try:
            #print(change["address"])
            if change["address"] != str(receivingAddress):
                return change["address"]
        except:
            pass
    return ""

def getNextDepositorAddress(receivingAddress):
    version = getNextDepositVersion(receivingAddress)
    if version != "":
        return getDepositorAddress(version, receivingAddress)
    else:
        return ""



if __name__ == "__main__":
    # :!:>section_1
    rest_client = RestClient(NODE_URL)
    faucet_client = FaucetClient(FAUCET_URL, rest_client)  # <:!:section_1

    # :!:>section_2
    alice = Account.load("aliceee.txt")
    bob = Account.load("receiver.txt")

    print("\n=== Addresses ===")
    print(f"Alice: {alice.address()}")
    print(f"Bob: {bob.address()}")

    # :!:>section_3
    try:
        faucet_client.fund_account(alice.address(), 100_000_000)
        faucet_client.fund_account(bob.address(), 100000000000)  # <:!:section_3
    except:
        print("faucet calls rejected")

    print("\n=== Initial Balances ===")
    # :!:>section_4
    print(f"Alice: {rest_client.account_balance(alice.address())}")
    print(f"Bob: {rest_client.account_balance(bob.address())}")  # <:!:section_4

    # Have Alice give Bob 1_000 coins
    # :!:>section_5
    txn_hash = rest_client.transfer(alice, bob.address(), 1_000000)  # <:!:section_5
    # :!:>section_6
    rest_client.wait_for_transaction(txn_hash)  # <:!:section_6

    print("\n=== Intermediate Balances ===")
    print(f"Alice: {rest_client.account_balance(alice.address())}")
    print(f"Bob: {rest_client.account_balance(bob.address())}")

    # Have Alice give Bob another 1_000 coins using BCS
    #txn_hash = rest_client.bcs_transfer(alice, bob.address(), 1_000)
    #rest_client.wait_for_transaction(txn_hash)

    print("\n=== Final Balances ===")
    print(f"Alice: {rest_client.account_balance(alice.address())}")
    print(f"Bob: {rest_client.account_balance(bob.address())}")


    relevantAddress = ""
    depAddress = getNextDepositorAddress(bob.address())
    while depAddress!="":
        print(depAddress)
        depAddress = getNextDepositorAddress(bob.address())
        

    
    
    txn_hash = rest_client.create_collection(
        bob, "waterboardersss", "Bob's simple collection", "https://aptos.dev"
    )  # <:!:section_4
    rest_client.wait_for_transaction(txn_hash)
    

    tokenname = "token7"
    txn_hash = rest_client.create_token(
        bob,
        "waterboardersss",
        tokenname,
        "Bob's simple token",
        1,
        "https://aptos.dev/img/nyan.jpeg",
        0,
    )  # <:!:section_5
    rest_client.wait_for_transaction(txn_hash)

    print("token created")

    input()


    txn_hash = rest_client.offer_token(
        bob,
        alice.address(),
        bob.address(),
        "waterboardersss",
        tokenname,
        0,
        1,
    )
    rest_client.wait_for_transaction(txn_hash)

    print("offer set")

    input()


    txn_hash = rest_client.claim_token(
        alice,
        bob.address(),
        bob.address(),
        "waterboardersss",
        tokenname,
        0,
    )  
    rest_client.wait_for_transaction(txn_hash)
    alice.store("aliceee.txt")  

    """

    url = NODE_URL+"/accounts/"+str(bob.address())+"/events/0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>/withdraw_events"
    print(url)
    output = requests.get(NODE_URL+"/accounts/"+str(bob.address())+"/events/0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>/deposit_events").text
    outputjson = json.loads(output)
    print(str(outputjson))
    for tx in outputjson:
        print(tx)
    relevantversion=outputjson[2]["version"]
    print(relevantversion)
    output = output.replace(str(alice.address()), "ALICEADDY")
    output = output.replace(str(bob.address()), "BOBADDY")
    print(output)

    
    output = requests.get(NODE_URL+"/transactions/by_version/"+str(relevantversion)).text
    outputjson = json.loads(output)
    print(len(outputjson))
    print(len(outputjson["changes"]))
    print("\n\n\n")
    #print(str(outputjson["changes"]).replace(str(alice.address()), "ALICEADDY"))
    
    #for change in outputjson["changes"]:
        #print(change["address"])
    output = output.replace(str(alice.address()), "ALICEADDY")
    output = output.replace(str(bob.address()), "BOBADDY")
    #print(output)

    print("DEPOSITING ADDDRESS", getDepositorAddress(relevantversion, bob.address()))
"""
    
  
    rest_client.close()