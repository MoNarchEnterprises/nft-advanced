from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
    get_publish_source,
)
from brownie import AdvancedCollectible, config, network


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["vrf_fee"],
        "MyHero",
        "MHA",
        {"from": account},
        publish_source=get_publish_source(),
    )
    fund_with_link(advanced_collectible.address)
    tx_create_nft = advanced_collectible.createCollectible({"from": account})
    tx_create_nft.wait(1)
    print(
        f"You can view your NFT at {OPENSEA_URL.format(advanced_collectible.address,advanced_collectible.tokenCounter()-1)}"
    )
    return advanced_collectible, tx_create_nft


def main():
    deploy_and_create()
