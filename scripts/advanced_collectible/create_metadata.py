import json
from brownie import AdvancedCollectible, network
from metadata.metadata_template import metadata_template
from scripts.helpful_scripts import get_nft_data
from pathlib import Path


def create_metadata():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_nfts = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_nfts} NFT")
    for token_id in range(number_of_nfts):
        mha, img_uri = get_nft_data(advanced_collectible.tokenIdToMHA(token_id))
        metadata_filename = f"./metadata/{network.show_active()}/{token_id}-{mha}.json"
        nft_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists")
        else:
            print(f"{metadata_filename} saving...")
            nft_metadata["name"] = mha
            nft_metadata["description"] = f"My Hero Academia prom picture of {mha}"
            nft_metadata["image_uri"] = img_uri
            print(nft_metadata)
            with open(metadata_filename, "w") as file:
                json.dump(nft_metadata, file)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()


def main():
    create_metadata()
