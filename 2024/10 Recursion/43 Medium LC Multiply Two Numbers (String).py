"""

43. Multiply Strings
Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2, also represented as a string.
Note: You must not use any built-in BigInteger library or convert the inputs to integer directly.

Example 1:
Input: num1 = "2", num2 = "3"
Output: "6"

Example 2:
Input: num1 = "123", num2 = "456"
Output: "56088"


"""
from functools import reduce


def sl(vs): return [int(v) for v in vs]


def ls(vl): return ''.join([str(v) for v in vl])


def add_lls(vls):
    def add_ll(ul, vl):
        def add_llc(ul, vl, carry):
            def add(d1, d2, *args):
                rsum = d1 + d2 + sum(args)
                return rsum % 10, rsum // 10

            def add_dl(c, vl):
                if not vl: return [] if not c else [c]
                d, c = add(c, vl[0])
                return [d] + add_dl(c, vl[1:])

            if not ul: return add_dl(carry, vl)
            if not vl: return add_dl(carry, ul)
            d, c = add(ul[0], vl[0], carry)
            return [d] + add_llc(ul[1:], vl[1:], c)

        return add_llc(ul, vl, 0)

    return reduce(add_ll, vls)


def mult_lss(vss):
    def zero(vls):
        def zero(vl):
            def zero(v): return v == 0
            return not all(filter(zero, vl))
        return any(filter(zero, vls))

    def mult_lls(vls):
        def mult_ll(ul, vl):
            def mult(d1, d2, carry):
                expr = d1 * d2 + carry
                return expr % 10, expr // 10

            def mult_dl(d, vl):
                def mult_dlc(d, vl,  carry):
                    if not vl: return [] if not carry else [carry]
                    p, carry = mult(d, vl[0], carry)
                    return [p] + mult_dlc(d, vl[1:], carry)
                return mult_dlc(d, vl, 0)
            wls = [([0] * i) + mult_dl(v, ul) for i, v in enumerate(vl)]
            for wl in wls: print(wl)
            return add_lls(wls)

        if zero(vls): return [0]
        return reduce(mult_ll, vls)

    return ls(mult_lls([sl(vs[::-1]) for vs in vss])[::-1])

if __name__ == '__main__':
    vss = ['8479', '576']
    print(mult_lss(vss))