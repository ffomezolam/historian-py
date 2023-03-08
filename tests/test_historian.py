#!python

from context import Historian, HistorianMixin

import unittest

class TestHistorian(unittest.TestCase):
    def setUp(self):
        self.H = Historian()
        self.a = 0

    def test(self):
        def inc(n):
            self.a += n
            self.H.register(dec, n)

        def dec(n):
            self.a -= n
            self.H.register(inc, n)

        inc(2)
        inc(2)
        inc(2)
        inc(2)
        inc(2)
        dec(3)
        dec(2)
        dec(2)
        dec(2)

        with self.subTest("size should be 9"):
            self.assertEqual(self.H.size(), 9)

        with self.subTest("var should be 1"):
            self.assertEqual(self.a, 1)

        with self.subTest("first undo should leave var at 3"):
            self.H.undo()
            self.assertEqual(self.a, 3)

        with self.subTest("should be able to undo multiple levels"):
            self.H.undo(5)
            self.assertEqual(self.a, 6)

        with self.subTest("first redo from 6 should leave var at 8"):
            self.H.redo()
            self.assertEqual(self.a, 8)

        with self.subTest("should be able to redo multiple levels"):
            self.H.redo(2)
            self.assertEqual(self.a, 7)

        with self.subTest("should be able to clear undo/redo history"):
            self.H.clear()
            self.assertEqual(self.H.size(), 0)

class TestClass(HistorianMixin):
    def __init__(self, a):
        HistorianMixin.__init__(self)
        self.a = a

    def inc(self, n):
        self.a += n
        self._undomgr.register(self.dec, n)
        return self

    def dec(self, n):
        self.a -= n
        self._undomgr.register(self.inc, n)
        return self

class TestHistorianMixin(unittest.TestCase):
    def setUp(self):
        self.C = TestClass(0)

    def test(self):
        self.C.inc(2).inc(2).inc(2).inc(2).inc(2) # incs to 10
        self.C.dec(3).dec(2).dec(2).dec(2) # decs to 1

        with self.subTest("size should be 9"):
            self.assertEqual(self.C._undomgr.size(), 9)

        with self.subTest("var should be 1"):
            self.assertEqual(self.C.a, 1)

        with self.subTest("first undo should leave var at 3"):
            self.C.undo()
            self.assertEqual(self.C.a, 3)

        with self.subTest("should be able to undo multiple levels"):
            self.C.undo(5)
            self.assertEqual(self.C.a, 6)

        with self.subTest("first redo from 6 should leave var at 8"):
            self.C.redo()
            self.assertEqual(self.C.a, 8)

        with self.subTest("should be able to redo multiple levels"):
            self.C.redo(2)
            self.assertEqual(self.C.a, 7)

        with self.subTest("should be able to clear undo/redo history"):
            self.C._undomgr.clear()
            self.assertEqual(self.C._undomgr.size(), 0)

if __name__ == '__main__':
    unittest.main()
