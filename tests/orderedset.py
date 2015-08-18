import unittest

from pykickstart.orderedset import OrderedSet

class OrderedSet_TestCase(unittest.TestCase):
    def runTest(self):
        # __eq__, __len__, etc.
        self.assertEqual(OrderedSet([]), OrderedSet([]))
        self.assertEqual(OrderedSet([1, 2, 3]), OrderedSet([1, 2, 3]))
        self.assertEqual(OrderedSet([1, 2, 3]), [1, 2, 3])

        # __reversed__
        self.assertEqual(reversed(OrderedSet([2, 4, 1, 3])), OrderedSet([3, 1, 4, 2]))

        # discard
        self.assertEqual(len(OrderedSet(["one", "two", "three"])), 3)
        os = OrderedSet(["one", "two", "three"])
        os.discard("two")
        self.assertEqual(len(os), 2)
        os = OrderedSet(["one", "two", "three"])
        os.discard("four")
        self.assertEqual(len(os), 3)

        # pop
        self.assertRaises(KeyError, OrderedSet().pop)
        self.assertEqual(OrderedSet(["one", "two", "three"]).pop(), "three")
        self.assertEqual(OrderedSet(["one"]).pop(), "one")
        os = OrderedSet(["one"])
        os.pop()
        self.assertEqual(len(os), 0)

        # __repr__
        self.assertEqual(repr(OrderedSet()), "OrderedSet()")
        self.assertEqual(repr(OrderedSet([1, 2, 3])), "OrderedSet([1, 2, 3])")

if __name__ == "__main__":
    unittest.main()
