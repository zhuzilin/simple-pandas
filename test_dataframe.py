from spandas import DataFrame
from spandas import Series
import pandas as pd
import numpy as np

values = {'a': np.array([1, 2, 3]), 
          'b': np.array([4, 5, 6]), 
            1: np.array([6, 7, 8])}
index = np.array(['a', 'b', 'c'])
a = DataFrame(values, index)

def test_constructor():
    assert a.keys() == values.keys()
    tmp = DataFrame(values, index, copy=False)
    for k in values:
        assert id(values[k]) == id(tmp.dict[k])
    assert id(index) == id(tmp.index)

def test_copy():
    tmp = a.copy()
    for k in values:
        assert id(values[k]) != id(tmp.dict[k])
    assert id(index) != id(tmp.index)

def test_indexing():
    # column
    tmp = a[['a']]
    assert isinstance(tmp, Series)
    assert np.all(tmp.values == np.array([1, 2, 3])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))
    tmp = a[['a', 1]]
    assert isinstance(tmp, DataFrame)
    assert np.all(tmp.dict['a'] == np.array([1, 2, 3])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))
    # row
    tmp = a[2]
    assert np.all(tmp.dict['a'] == np.array([3])) and \
           np.all(tmp.dict['b'] == np.array([6])) and \
           np.all(tmp.dict[1] == np.array([8])) and \
           np.all(tmp.index == np.array(['c']))
    tmp = a[np.array([1, 2])]
    assert np.all(tmp.dict['a'] == np.array([2, 3])) and \
           np.all(tmp.dict['b'] == np.array([5, 6])) and \
           np.all(tmp.dict[1] == np.array([7, 8])) and \
           np.all(tmp.index == np.array(['b', 'c']))
    tmp = a[1:3]
    assert np.all(tmp.dict['a'] == np.array([2, 3])) and \
           np.all(tmp.dict['b'] == np.array([5, 6])) and \
           np.all(tmp.dict[1] == np.array([7, 8])) and \
           np.all(tmp.index == np.array(['b', 'c']))
    # test unchange
    tmp = a
    assert np.all(tmp.dict['a'] == np.array([1, 2, 3])) and \
           np.all(tmp.dict['b'] == np.array([4, 5, 6])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))

def test_assign():
    # column assignment
    tmp = a.copy()
    tmp[['a', 'c']] = 1
    assert np.all(tmp.dict['a'] == np.array([1, 1, 1])) and \
           np.all(tmp.dict['b'] == np.array([4, 5, 6])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8])) and \
           np.all(tmp.dict['c'] == np.array([1, 1, 1])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))
    tmp = a.copy()
    tmp[['a', 'c']] = [3, 2, 1]
    assert np.all(tmp.dict['a'] == np.array([3, 2, 1])) and \
           np.all(tmp.dict['b'] == np.array([4, 5, 6])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8])) and \
           np.all(tmp.dict['c'] == np.array([3, 2, 1])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))
    # row assignment
    tmp = a.copy()
    tmp[0] = 30
    assert np.all(tmp.dict['a'] == np.array([30, 2, 3])) and \
           np.all(tmp.dict['b'] == np.array([30, 5, 6])) and \
           np.all(tmp.dict[1] == np.array([30, 7, 8])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))
    tmp = a.copy()
    tmp[:2] = 30
    assert np.all(tmp.dict['a'] == np.array([30, 30, 3])) and \
           np.all(tmp.dict['b'] == np.array([30, 30, 6])) and \
           np.all(tmp.dict[1] == np.array([30, 30, 8])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))
    # nested assignment
    tmp = a.copy()
    tmp[['b']][:2] = 30
    assert np.all(tmp.dict['a'] == np.array([1, 2, 3])) and \
           np.all(tmp.dict['b'] == np.array([30, 30, 6])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))
    tmp = a.copy()
    tmp[['a', 'b']][:2] = 30
    assert np.all(tmp.dict['a'] == np.array([30, 30, 3])) and \
           np.all(tmp.dict['b'] == np.array([30, 30, 6])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))