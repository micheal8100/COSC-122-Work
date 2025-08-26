
def quick_power(x, n):
    """
    Computes x ^ n where n is an integer and is >= 0
    Feel free to raise an exception if n is not valid.
    NOTES:
    - You need to write the doc test for the base case.
    - You shouldn't use the ** operator in your function
    - You shouldn't use the slow_power function either
    - Remember n squared is simply n * n
        + quick_power should only call itself once...
    >>> quick_power(2,3)
    8
    >>> quick_power(2, 8)
    256
    >>> quick_power(2, 16)
    65536
    >>> quick_power(2, 64)
    18446744073709551616
    >>> quick_power(2, 128)
    340282366920938463463374607431768211456
    >>> quick_power(4, 64)
    340282366920938463463374607431768211456
    >>> quick_power(10, 32)
    100000000000000000000000000000000
    >>> quick_power(8, 32)
    79228162514264337593543950336
    """
    # ---start student section---
    if n < 0:
        raise ValueError("Exponent must be non-negative")
    if n == 0:
        return 1
    half = quick_power(x, n // 2)
    if n % 2 == 0:
        return half * half
    else:
        return x * half * half
    # ===end student section===
quick_power(x, 9)