from brownie import network, AdvancedCollectible, config
import pytest
from scripts.advanced_collectible.deploy_and_create import (
    deploy,
    create,
    get_contract,
)
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)


def test_can_create_NFT():
    # deploy the contract
    # create NFT
    # get random MHA back
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    # Act
    deploy()
    advanced_collectible, vrf_tx = create(-1)
    requestId = vrf_tx.events["requestedCollectible"]["requestId"]
    vrf_coordinator = get_contract("vrf_coordinator")
    random_number = 42069
    vrf_coordinator.callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": account}
    )
    # Assert
    assert advanced_collectible.tokenCounter() >= 1
    assert advanced_collectible.tokenIdToMHA(0) == random_number % 3
