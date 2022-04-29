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

w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 60}))
poolAddress = _str_to_addr('0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8')
pool_contract = _load_contract(w3, abi_name="uniswap-v3/pool", address=poolAddress)


async def get_pool_immutables():
    """
    Should turn this into an async function later.
    """
    test = await asyncio.gather(
        pool_contract.functions.factory().call(),
        pool_contract.functions.token0().call(),
        pool_contract.functions.token1().call(),
        pool_contract.functions.fee().call(),
        pool_contract.functions.tickSpacing().call(),
        pool_contract.functions.maxLiquidityPerTick().call()
    )

    print(test)
    # factory = pool_contract.functions.factory().call()
    # token0 = pool_contract.functions.token0().call()
    # token1 = pool_contract.functions.token1().call()
    # fee = pool_contract.functions.fee().call()
    # tickSpacing = pool_contract.functions.tickSpacing().call()
    # maxLiquidityPerTick = pool_contract.functions.maxLiquidityPerTick().call()

    # return Immutables(factory, token0, token1, fee, tickSpacing, maxLiquidityPerTick)

if __name__ == "__main__":
    get_pool_immutables()