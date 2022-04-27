
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
        ret += f'token0: {self.token0} \n'
        ret += f'token1: {self.token1} \n'
        ret += f'fee: {self.fee/1000000} \n'
        return ret