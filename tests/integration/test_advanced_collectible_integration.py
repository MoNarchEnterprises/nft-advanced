from brownie import network, AdvancedCollectible, config
import pytest
from scripts.advanced_collectible.deploy_and_create import (
    deploy_and_create,
    get_contract,
)
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
import time


def test_can_create_NFT_integration():
    # deploy the contract
    # create NFT
    # get random MHA back
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for testnet testing")
    account = get_account()
    # Act
    advanced_collectible, vrf_tx = deploy_and_create()
    time.sleep(300)
    # Assert
    assert advanced_collectible.tokenCounter() >= 1
