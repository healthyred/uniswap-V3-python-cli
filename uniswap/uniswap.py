from web3 import Web3

PROVIDER='https://mainnet.infura.io/v3/49d9273a4f5c446697ee32b9af8bc7cc'


class UniswapV3:
    """
    Wrapper around UniswapV3 contracts.
    """

    w3: Web3

    def __init__(self, web3: Web3 = None) -> None:
        if web3:
            self.w3 = web3

