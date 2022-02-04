from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

RAVEN_URI = "https://ipfs.io/ipfs/QmQcwGGf7Vn7aqdXyRMQAAiqchuRL2zFCHpfmV2oC4HTWJ?filename=0-RAV.json"


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy("Raven", "RAV", {"from": account})
    tx_create_nft = simple_collectible.createCollectible(RAVEN_URI, {"from": account})
    tx_create_nft.wait(1)
    print(
        f"You can view your NFT at {OPENSEA_URL.format(simple_collectible.address,simple_collectible.tokenCounter()-1)}"
    )
    # return simple_collectible


def main():
    deploy_and_create()
