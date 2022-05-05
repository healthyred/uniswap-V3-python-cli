import asyncio
from web3 import Web3
from web3.eth import Contract
from price import Price

from constants import (
    PROVIDER,
    Q192
)
from util import (
    _str_to_addr,
    _addr_to_str,
    _validate_address,
    _load_contract,
    _load_contract_erc20,
    parse_nft_response_into_object,
    is_same_address,
)

class Immutables:
    def __init__(
        self,
        factory: str,
        token0: str,
        token1: str, 
        fee: int,
        tick_spacing: int,
        max_liquidity_per_tick: int
    ) -> None:
        
        self.factory = factory
        self.token0 = token0
        self.token1 = token1
        self.fee = fee
        self.tick_spacing = tick_spacing
        self.max_liquidity_per_tick = max_liquidity_per_tick
    
    def __str__(self) -> str:
        #TODO: 
        pass


class State:

    def __init__(
        self,
        liquidity,
        sqrt_price_x96,
        tick,
        observation_index,
        observation_cardinality,
        observation_cardinality_next,
        fee_protocol,
        unlocked
    ) -> None:
        self.liquidity = liquidity
        self.sqrt_price_x96 = sqrt_price_x96
        self.tick = tick
        self.observation_index = observation_index
        self.observation_cardinality = observation_cardinality
        self.observation_cardinality_next = observation_cardinality_next
        self.fee_protocol = fee_protocol
        self.unlocked = unlocked

    def __str__(self) -> str:
        #TODO: 
        pass


class Pool:

    def __init__(
        self,
        pool_address_str
    ):
        self.w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 60}))
        self.pool_address = _str_to_addr(pool_address_str)
        self.pool_contract = _load_contract(self.w3, abi_name="uniswap-v3/pool", address=self.pool_address)

    def get_pool_immutables(self):
        """
        We write this function as an async func so that we don't have sequential calls
        to the blockchain where our data becomes out of sync by some number of blocks.
        TODO: turn this function async.
        """
        factory = self.pool_contract.functions.factory().call()
        token0 = self.pool_contract.functions.token0().call()
        token1 = self.pool_contract.functions.token1().call()
        fee = self.pool_contract.functions.fee().call()
        tickSpacing = self.pool_contract.functions.tickSpacing().call()
        maxLiquidityPerTick = self.pool_contract.functions.maxLiquidityPerTick().call()

        return Immutables(factory, token0, token1, fee, tickSpacing, maxLiquidityPerTick)

    def get_pool_state(self):
        """
        Grabs the state of a given pool.
        """
        liquidity = self.pool_contract.functions.liquidity().call()
        slot = self.pool_contract.functions.slot0().call()
        return State(
            liquidity, 
            sqrt_price_x96=slot[0],
            tick=slot[1],
            observation_index=slot[2],
            observation_cardinality=slot[3],
            observation_cardinality_next=slot[4],
            fee_protocol=slot[5],
            unlocked=slot[6]
            )

    def get_token0_price(self): 
        """
        Returns the price for token 0 of the pool.
        """
        immutables = self.get_pool_immutables()
        state = self.get_pool_state()
        price = Price(immutables.token0, immutables.token1, Q192, state.sqrt_price_x96 * state.sqrt_price_x96)
        if price:
            return price
        return None

    def get_token1_price(self):
        """
        Returns the current mid-price of the pool in terms of token1, i.e. the ratio of token0 over token1.
        """
        immutables = self.get_pool_immutables()
        state = self.get_pool_state()
        price = Price(immutables.token1, immutables.token0, state.sqrt_price_x96 * state.sqrt_price_x96, Q192)
        if price:
            return price
        return None

if __name__ == "__main__":
    # test = get_pool_immutables()
    USDC_WETH_POOL = Pool('0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8')
    DAI_USDC_POOL = Pool('0x5777d92f208679DB4b9778590Fa3CAB3aC9e2168')
    WBTC_USDC_POOL = Pool('0x99ac8ca7087fa4a2a1fb6357269965a2014abc35')
    print(f'wbtc price: {WBTC_USDC_POOL.get_token0_price().quotient()}')
    price_x96 = USDC_WETH_POOL.get_pool_state().sqrt_price_x96 ** 2
    # print(2 ** 192)
    # print(price_x96)
    # print(USDC_WETH_POOL.get_pool_state().sqrt_price_x96)
    # print((USDC_WETH_POOL.get_pool_state().sqrt_price_x96 ** 2) / (2 ** 192))
    # print(2 ** 192 / USDC_WETH_POOL.get_pool_state().sqrt_price_x96 ** 2)

    # print(USDC_WETH_POOL.get_token1_price().quotient())
    # print(f'Dai/usdc price: {(DAI_USDC_POOL.get_pool_state().sqrt_price_x96 ** 2) / (2 ** 192)}')
    # print(f'Dai/usdc price: {DAI_USDC_POOL.get_token0_price().quotient()}')

    test = USDC_WETH_POOL.get_pool_immutables()

    print(f'{test.factory}, {test.token0}, {test.token1}, {test.tick_spacing}, {test.fee}, {test.max_liquidity_per_tick}')

    state = USDC_WETH_POOL.get_pool_state()
    print(f'{state.liquidity}, sqrt_price_x96: {state.sqrt_price_x96}, {state.tick}, {state.observation_index}, {state.observation_cardinality}, {state.observation_cardinality_next}, {state.unlocked}')

    print(state.sqrt_price_x96 ** 2 // (2 ** 192))