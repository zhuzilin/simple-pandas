from spandas import Series
import pandas as pd
import numpy as np

values = np.arange(5)
index = np.array(['a', 'b', 'c', 'd', 'e'])
a = Series(values, index)

def test_constructor():
    tmp = a
    assert np.all(tmp.values == np.arange(5)) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    # default as copy
    assert id(a.values) != id(values) and id(a.index) != id(index)
    tmp = Series(values, index, copy=False)
    assert id(tmp.values) == id(values) and id(tmp.index) == id(index)

def test_indexing():
    tmp = a[3]
    assert tmp == 3
    tmp = a[np.array([1, 2, 3])]
    assert np.all(tmp.values == np.array([1, 2, 3])) and \
           np.all(tmp.index == np.array(['b', 'c', 'd']))
    tmp = a[1:3]
    assert np.all(tmp.values == np.array([1, 2])) and \
           np.all(tmp.index == np.array(['b', 'c']))
    tmp = a[a > 2]
    assert np.all(tmp.values == np.array([3, 4])) and \
           np.all(tmp.index == np.array(['d', 'e']))
    # index with index label
    tmp = a[a.index == 'e']
    assert np.all(tmp.values == np.array([4])) and \
           np.all(tmp.index == np.array(['e']))
    tmp = a[np.isin(a.index, ['b', 'c'])]
    assert np.all(tmp.values == np.array([1, 2])) and \
           np.all(tmp.index == np.array(['b', 'c']))
    # test unchange
    assert np.all(a.values == np.arange(5)) and \
           np.all(a.index == np.array(['a', 'b', 'c', 'd', 'e']))

def test_copy():
    tmp = a.copy()
    assert np.all(tmp.values == a.values) and \
           np.all(tmp.index == a.index)
    # test unchange
    tmp.values[3] = 10
    assert np.all(a.values == np.arange(5)) and \
           np.all(a.index == np.array(['a', 'b', 'c', 'd', 'e']))

def test_assign():
    tmp = a.copy()
    tmp[1] = 10
    assert np.all(tmp.values == np.array([0, 10, 2, 3, 4])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    tmp = a.copy()
    tmp[np.array([1, 2, 3])] = 10
    assert np.all(tmp.values == np.array([0, 10, 10, 10, 4])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    tmp = a.copy()
    tmp[0:2] = 10
    assert np.all(tmp.values == np.array([10, 10, 2, 3, 4])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    tmp = a.copy()
    tmp[a.index == 'e'] = 10
    assert np.all(tmp.values == np.array([0, 1, 2, 3, 10])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    # test unchange
    assert np.all(a.values == np.arange(5)) and \
           np.all(a.index == np.array(['a', 'b', 'c', 'd', 'e']))

def test_iterative():
    tmp = ""
    for i, v in a.items():
        tmp += "{}{}".format(i, v)
    assert tmp == "a0b1c2d3e4"
    tmp = 0
    for v in a:
        tmp += v
    assert tmp == 10
    
def test_len():
    assert len(a) == len(a.values) and len(a) == len(a.index)