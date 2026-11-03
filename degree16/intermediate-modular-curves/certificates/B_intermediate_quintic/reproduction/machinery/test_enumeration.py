"""Fast standard-library tests; run python3 -m unittest -v."""
import unittest
from itertools import combinations
from enumeration import units, generated, subgroups, signature


class EnumerationTests(unittest.TestCase):
    def test_complete_against_powerset(self):
        # Exponential and deliberately different enumeration, at small levels.
        for n in range(1, 19):
            u = units(n)
            if len(u) > 10:
                continue
            expected = set()
            for size in range(1, len(u)+1):
                for subset in combinations(u, size):
                    if (-1) % n not in subset or 1 % n not in subset:
                        continue
                    if all(a*b % n in subset for a in subset for b in subset):
                        expected.add(subset)
            self.assertEqual(set(subgroups(n)), expected)

    def test_level_one(self):
        row = signature(1, (0,))
        self.assertEqual((row['index'], row['genus'], row['cusps']), (1, 0, 1))

    def test_classical_examples(self):
        for n, g0, g1 in [(11, 1, 1), (13, 0, 2), (17, 1, 5), (23, 2, 12)]:
            self.assertEqual(signature(n, units(n))['genus'], g0)
            self.assertEqual(signature(n, generated(n, [-1]))['genus'], g1)

    def test_invalid_groups(self):
        with self.assertRaises(ValueError):
            generated(12, [2])
        with self.assertRaises(ValueError):
            signature(13, (1,))


if __name__ == '__main__':
    unittest.main()
