from brownie import AdvancedCollectible
from scripts.helpful_scripts import fund_with_link, get_account


def create_collectible():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    token_tx = advanced_collectible.createCollectible({"from": account})
    token_tx.wait(1)
    print("New NFT created!")


def main():
    create_collectible()
