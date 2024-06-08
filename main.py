from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

# Client to connect to localnet
algorand = AlgorandClient.default_local_net()

# Import dispenser from KMD 
dispenser = algorand.account.dispenser()
print("Dispenser Address: ", dispenser.address)

# Create two Algorand Accounts
account1 = algorand.account.random()
account2 = algorand.account.random()
print("Account 1 Address: ", account1.address)
print("Account 2 Address: ", account2.address)

# Fund both accounts
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=account1.address,
        amount=10_000_000
    )
)
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=account2.address,
        amount=10_000_000
    )
)

# Create an Algorand Standard Asset (ASA) with account1 as the creator
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=account1.address,
        total=1000,
        asset_name="MyToken",
        unit_name="MTK",
        manager=account1.address,
        clawback=account1.address,
        freeze=account1.address
    )
)

# Extracting the confirmation and asset index of the asset creation transaction to get asset ID
asset_id = sent_txn["confirmation"]["asset-index"]
print("Asset ID: ", asset_id)

# Opt-in account2 to the ASA
algorand.send.asset_opt_in(
    AssetOptInParams(
        sender=account2.address,
        asset_id=asset_id
    )
)

# Transfer 10 units of ASA from account1 to account2
algorand.send.asset_transfer(
    AssetTransferParams(
        sender=account1.address,
        receiver=account2.address,
        asset_id=asset_id,
        amount=10
    )
)

# Print balances after transfer
account1_info = algorand.account.get_information(account1.address)
account2_info = algorand.account.get_information(account2.address)
print("Receiver Account Asset Balance (post transfer):", account2_info['assets'][0]['amount'])
print("Creator Account Asset Balance (post transfer):", account1_info['assets'][0]['amount'])

# Perform a clawback of 5 units of the asset from account2 back to account1
algorand.send.asset_transfer(
    AssetTransferParams(
        sender=account1.address,
        receiver=account1.address,
        asset_id=asset_id,
        amount=5,
        clawback_target=account2.address  # The address to clawback the asset from
    )
)

# Print balances after clawback
account1_info_post_clawback = algorand.account.get_information(account1.address)
account2_info_post_clawback = algorand.account.get_information(account2.address)
print("Receiver Account Asset Balance (post clawback):", account2_info_post_clawback['assets'][0]['amount'])
print("Creator Account Asset Balance (post clawback):", account1_info_post_clawback['assets'][0]['amount'])
