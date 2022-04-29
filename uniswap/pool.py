import asyncio
from web3 import Web3
from web3.eth import Contract


from constants import (
    PROVIDER,
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
        self.pool_contract = _load_contract(self.w3, abi_name="uniswap-v3/pools", address=self.pool_address)
        # w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 60}))
        # poolAddress = _str_to_addr('0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8')
        # pool_contract = _load_contract(w3, abi_name="uniswap-v3/pool", address=poolAddress)

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


if __name__ == "__main__":
    # test = get_pool_immutables()
    pool = Pool('0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8')
    test = pool.get_pool_immutables()

    print(f'{test.factory}, {test.token0}, {test.token1}, {test.tick_spacing}, {test.fee}, {test.max_liquidity_per_tick}')

    state = pool.get_pool_state()
    print(f'{state.liquidity}, {state.sqrt_price_x96}, {state.tick}, {state.observation_index}, {state.observation_cardinality}, {state.observation_cardinality_next}, {state.unlocked}')

