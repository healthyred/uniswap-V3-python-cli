from re import I
import tick_math

def msb_test():
    for i in range(1,256):
        x = 2 ** i
        assert(tick_math.most_significant_bit(x) == i)

if __name__ == "__main__":
    msb_test()