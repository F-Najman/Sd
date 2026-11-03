"""Independent arithmetic-cusp checks against classical endpoint formulas."""
from math import gcd
import unittest
from cusp_arithmetic import cusp_degrees
from enumeration import units


class CuspArithmeticTests(unittest.TestCase):
    def test_x0_cyclotomic_degrees(self):
        for n in range(1,65):
            expected = sorted(len(units(gcd(d,n//d)))
                              for d in range(1,n+1) if n%d==0)
            self.assertEqual(cusp_degrees(n,units(n)),expected,n)

    def test_prime_x1(self):
        for p in [5,7,11,13,17,19]:
            half = (p-1)//2
            self.assertEqual(cusp_degrees(p,[1,p-1]),[1]*half+[half])


if __name__=='__main__':
    unittest.main()
