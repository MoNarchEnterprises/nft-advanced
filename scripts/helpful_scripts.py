from brownie import (
    Contract,
    network,
    accounts,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
)


from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-forked-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

DECIMALS = 8
STARTING_PRICE = 2000 * 10 ** 8

NFT_MAPPING = {0: "DEKU", 1: "TOKYAMIxASUI", 2: "DEKU_DEKUPOOL"}
NFT_IMAGE_URI_MAPPING = {
    0: "https://ipfs.io/ipfs/QmRdAfTnjTwQSc3n8gNvCz7F6sbPL5QL1aftTK27vGmVqa?filename=deku.JPG",
    1: "https://ipfs.io/ipfs/QmWf8Xc7buM5njS6i1ZamEGFitQ4YKu3V2cRXx6uNWYf8y?filename=TokyamixAsui.JPG",
    2: "https://ipfs.io/ipfs/QmfLTkhU5MaZqGJyudzFCck386m46XvnZWEmnhk13wg4sV?filename=deku_dekupool.JPG",
}
NFT_METADATA_URI_MAPPING = {
    0: "https://ipfs.io/ipfs/QmRUYjXXwnhfa8mkNoiCUDyJBUTuroZfudGsN9iHAeCFAQ",  # ?filename=0-DEKU.json",
    1: "https://ipfs.io/ipfs/QmZmqbVrG86aTzGfkuXjr4ehMoYNpv3eizQjznVSWHuR6d",  # ?filename=1-TOKYAMIxASUI.json",
    2: "https://ipfs.io/ipfs/QmdoyEVej9AyjQWN9o5gChUQqn6nt2iWt7oDE87STKaFHQ",  # ?filename=2-DEKU_DEKUPOOL.json",
}


def get_nft_data(index_number):
    return (
        NFT_MAPPING[index_number],
        NFT_IMAGE_URI_MAPPING[index_number],
        NFT_METADATA_URI_MAPPING[index_number],
    )


def get_publish_source():
    return config["networks"][network.show_active()]["Verify"]


def get_account(index=None, id=None):
    # accounts[index]
    if index:
        return accounts[index]
    # accounts.load(id) if an ID is given
    if id:
        return accounts.load(id)
    # accounts[0] if in development or FORKED_LOCAL_ENVIRONMENTS
    if (
        network.show_active() == "development"
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    # account from ganache wallet
    if network.show_active() == "ganache-local":
        return accounts.add(config["wallets"]["from_ganache_key"])

    # otherwise default to account from network wallets
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    # Grab contract addresses from brownie-config otherwise deploy a mock account

    # Args:
    #     contract_name (string)
    # Returns:
    #     brownie.network.contract.ProjectContract: The most recently deployed version

    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
    print("Aggregator deployed")
    link_token = LinkToken.deploy({"from": account})
    print(f"LINK token {link_token} deployed")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("VRF deployed")


def fund_with_link(contract_address, account=None, link_token=None, amount=10 ** 17):
    if account:
        account = account
    else:
        account = get_account()
    if link_token:
        link_token = link_token
    else:
        link_token = get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded with LINK")
    return tx
