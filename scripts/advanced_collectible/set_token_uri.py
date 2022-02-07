from brownie import network, AdvancedCollectible

from scripts.helpful_scripts import get_account, get_nft_data, OPENSEA_URL


def set_token_uri():
    print(f"Working on {network.show_active()}...")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_nfts = advanced_collectible.tokenCounter()
    print(f"You have {number_of_nfts} NFTs")
    for token_id in range(number_of_nfts):
        mha, img_uri, nft_uri = get_nft_data(
            advanced_collectible.tokenIdToMHA(token_id)
        )
        if True:  # not advanced_collectible.tokenURI(token_id).startswith("https://"):
            account = get_account()
            tx = advanced_collectible.setTokenURI(token_id, nft_uri, {"from": account})
            tx.wait(1)
            print(
                f"You can view your NFT at {OPENSEA_URL.format(advanced_collectible.address,token_id)}"
            )
            print("Please wait up to 20 minutes and refresh metadata button")


def main():
    set_token_uri()
