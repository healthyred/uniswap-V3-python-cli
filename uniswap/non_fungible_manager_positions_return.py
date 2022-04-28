from tokens import (
    INVERSE_TOKENS,
    TOKENS
)

class NonFungibleManagerPositionsReseponse:

    def __init__(
        self,
        nonce,
        operator,
        token0,
        token1,
        fee,
        tickLower,
        tickUpper,
        liquidity,
        feeGrowthInside0LastX128,
        feeGrowthInside1LastX128,
        tokensOwed0,
        tokensOwed1,
    ) -> None:
        self.nonce = nonce
        self.operator = operator
        self.token1 = token1
        self.token0 = token0
        self.fee = fee
        self.tickLower = tickLower
        self.tickUpper = tickUpper
        self.liquidity = liquidity
        self.feeGrowthInside0LastX128 = feeGrowthInside0LastX128
        self.feeGrowthInside1LastX128 = feeGrowthInside1LastX128
        self.tokensOwed0 = tokensOwed0
        self.tokensOwed1 = tokensOwed1        

    def __str__(self) -> str:
        ret = ""
        ret += f'operator: {self.operator} \n'
        ret += f'token0: {INVERSE_TOKENS[self.token0]} \n'
        ret += f'token1: {INVERSE_TOKENS[self.token1]} \n'
        ret += f'fee: {self.fee/1000000} \n'
        ret += f'liquidity: {self.liquidity} \n'
        ret += f'tickLower: {self.tickLower} \n'
        ret += f'tickUpper: {self.tickUpper} \n'

        return ret