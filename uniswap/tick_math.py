
def mulShift(val: int, mulBy: str):
    return (val * int(mulBy, 16)) >> 128

Q32 = 2 ** 32
MAX_INT_HEX = "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
MAX_INT = int(MAX_INT_HEX, 16)

def get_powers_of_2():
    map_of_2 = {}
    for pow in [128, 64, 32, 16, 8, 4, 2, 1]:
        map_of_2[pow] = 2 ** pow
    return map_of_2

def most_significant_bit(num):
    assert(num > 0, 'ZERO')
    assert(num < MAX_INT, 'MAX')
    
    powers_of_2 = get_powers_of_2()

    msb = 0
    for power, value in powers_of_2.items():
        if num >= value:
            num = num >> power
            msb += power
    return msb

class TickMath:

    # The minimum tick that can be used on any pool.
    MIN_TICK = -887272

    # The maximum tick that can be used on any pool.
    MAX_TICK = -MIN_TICK

    # The sqrt ratio corresponding to the minimum tick that could be used on any pool.
    MIN_SQRT_RATIO = 4295128739

    # The sqrt ratio corresponding to the maximum tick that could be used on any pool.
    MAX_SQRT_RATIO = 1461446703485210103287273052203988822378723970342

    def get_sqrt_ratio_at_tick(self, tick):
        # TODO: write assert check here

        absTick = tick * -1 if tick < 0 else tick

        ratio = int('0xfffcb933bd6fad37aa2d162d1a594001', 16) if (absTick & 0x1) != 0 else int('0x100000000000000000000000000000000', 16)
        if ((absTick & 0x2) != 0): ratio = mulShift(ratio, '0xfff97272373d413259a46990580e213a')
        if ((absTick & 0x4) != 0): ratio = mulShift(ratio, '0xfff2e50f5f656932ef12357cf3c7fdcc')
        if ((absTick & 0x8) != 0): ratio = mulShift(ratio, '0xffe5caca7e10e4e61c3624eaa0941cd0')
        if ((absTick & 0x10) != 0): ratio = mulShift(ratio, '0xffcb9843d60f6159c9db58835c926644')
        if ((absTick & 0x20) != 0): ratio = mulShift(ratio, '0xff973b41fa98c081472e6896dfb254c0')
        if ((absTick & 0x40) != 0): ratio = mulShift(ratio, '0xff2ea16466c96a3843ec78b326b52861')
        if ((absTick & 0x80) != 0): ratio = mulShift(ratio, '0xfe5dee046a99a2a811c461f1969c3053')
        if ((absTick & 0x100) != 0): ratio = mulShift(ratio, '0xfcbe86c7900a88aedcffc83b479aa3a4')
        if ((absTick & 0x200) != 0): ratio = mulShift(ratio, '0xf987a7253ac413176f2b074cf7815e54')
        if ((absTick & 0x400) != 0): ratio = mulShift(ratio, '0xf3392b0822b70005940c7a398e4b70f3')
        if ((absTick & 0x800) != 0): ratio = mulShift(ratio, '0xe7159475a2c29b7443b29c7fa6e889d9')
        if ((absTick & 0x1000) != 0): ratio = mulShift(ratio, '0xd097f3bdfd2022b8845ad8f792aa5825')
        if ((absTick & 0x2000) != 0): ratio = mulShift(ratio, '0xa9f746462d870fdf8a65dc1f90e061e5')
        if ((absTick & 0x4000) != 0): ratio = mulShift(ratio, '0x70d869a156d2a1b890bb3df62baf32f7')
        if ((absTick & 0x8000) != 0): ratio = mulShift(ratio, '0x31be135f97d08fd981231505542fcfa6')
        if ((absTick & 0x10000) != 0): ratio = mulShift(ratio, '0x9aa508b5b7a84e1c677de54f3e99bc9')
        if ((absTick & 0x20000) != 0): ratio = mulShift(ratio, '0x5d6af8dedb81196699c329225ee604')
        if ((absTick & 0x40000) != 0): ratio = mulShift(ratio, '0x2216e584f5fa1ea926041bedfe98')
        if ((absTick & 0x80000) != 0): ratio = mulShift(ratio, '0x48a170391f7dc42444e8fa2')

        if tick > 0:
            ratio = MAX_INT // ratio

        # Back to Q96.
        if ratio % Q32 > 0:
            return ratio // Q32 + 1
        return ratio // Q32


    def get_tick_at_sqrt_ratio(self, sqrtRatioX96):
        """
        Returns the tick corresponding to a given sqrt ratio, s.t. #getSqrtRatioAtTick(tick) <= sqrtRatioX96
        and #getSqrtRatioAtTick(tick + 1) > sqrtRatioX96
        @param sqrtRatioX96 the sqrt ratio as a Q64.96 for which to compute the tick
        """

        ## TODO code check

        sqrtRatioX128 = sqrtRatioX96 << 32
        msb = most_significant_bit(sqrtRatioX128)

        r = sqrtRatioX128 >> (msb - 127) if msb >= 128 else sqrtRatioX128 << (127 - msb)
        
        log_2 = (msb - 128) << 64

        for i in range(14):
            r = (r * r) >> 127
            f = r >> 128
            log_2 = log_2 | (f << (63 - i))
            r = r >> f

        log_sqrt10001 = log_2 * 255738958999603826347141

        tick_low = (log_sqrt10001 - 3402992956809132418596140100660247210) >> 128
        tick_high = (log_sqrt10001 + 291339464771989622907027621153398088495) >> 128

        if tick_low == tick_high:
            return tick_high
        else: 
            if self.get_sqrt_ratio_at_tick(tick_high) <= sqrtRatioX96:
                return tick_high
            return tick_low


 
if __name__ == "__main__":
    tick = TickMath()
    # print(tick.MAX_TICK)
    # print(tick.get_sqrt_ratio_at_tick(tick.MAX_TICK) == tick.MAX_SQRT_RATIO)
    # print(tick.get_sqrt_ratio_at_tick(tick.MIN_TICK) == tick.MIN_SQRT_RATIO)
    print(tick.get_tick_at_sqrt_ratio(tick.MAX_SQRT_RATIO) == tick.MAX_TICK)
    print(tick.get_tick_at_sqrt_ratio(tick.MIN_SQRT_RATIO) == tick.MIN_TICK)

    # print(round(tick.getSqrtRatioAtTick(tick.MIN_TICK)) == tick.MIN_SQRT_RATIO)