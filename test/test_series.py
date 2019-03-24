import sys
sys.path.append('../')
from spandas import Series
import pandas as pd
import numpy as np
import math

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
    tmp = Series({'a': 1, 'b': 2})
    assert np.all(tmp.values == np.array([1, 2])) and \
           np.all(tmp.index == np.array(['a', 'b']))
    # initialize with pd.Series
    tmp_s = pd.Series(values, index)
    tmp = Series(tmp_s, tmp_s.index)
    assert np.all(tmp.values == np.arange(5)) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))

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
    # get by index
    tmp = a[a.index == 'e']
    assert np.all(tmp.values == np.array([4])) and \
           np.all(tmp.index == np.array(['e']))
    tmp = a.get_by_index('e')
    assert np.all(tmp.values == np.array([4])) and \
           np.all(tmp.index == np.array(['e']))
    tmp = a.get_by_index(['b', 'c'])
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
    # set by index
    tmp[a.index == 'e'] = 10
    assert np.all(tmp.values == np.array([0, 1, 2, 3, 10])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    tmp = a.copy()
    tmp.set_by_index('e', 10)
    assert np.all(tmp.values == np.array([0, 1, 2, 3, 10])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    tmp = a.copy()
    tmp.set_by_index(['e', 'd'], [10, 9])
    assert np.all(tmp.values == np.array([0, 1, 2, 9, 10])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    # test unchange
    assert np.all(a.values == np.arange(5)) and \
           np.all(a.index == np.array(['a', 'b', 'c', 'd', 'e']))

def test_iter():
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

def test_comp_op():
    tmp = a > 2
    assert np.all(tmp.values == np.array([False, False, False, True, True])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    tmp = a < 2
    assert np.all(tmp.values == np.array([True, True, False, False, False])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    tmp = a == Series([0, 1, 2, 2, 3])
    assert np.all(tmp.values == np.array([True, True, True, False, False])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))

def test_arithmetic_op():
    tmp = a + 1
    assert np.all(tmp.values == np.array([1, 2, 3, 4, 5])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    tmp = a - Series([1, 2, 3, 4, 5])
    assert np.all(tmp.values == np.array([-1, -1, -1, -1, -1])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
           
def test_dict():
    tmp = a.dict
    assert tmp == {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    
def test_append():
    tmp_append = Series([5])
    tmp = a.append(tmp_append)
    assert np.all(tmp.values == np.array([0, 1, 2, 3, 4, 5])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e', 0]))
    tmp = a.append([tmp_append, tmp_append])
    assert np.all(tmp.values == np.array([0, 1, 2, 3, 4, 5, 5])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e', 0, 0]))
    # test unchange
    assert np.all(a.values == np.arange(5)) and \
           np.all(a.index == np.array(['a', 'b', 'c', 'd', 'e']))

def test_apply():
    grade = Series([100, 90, 80, 60], index=['a', 'b', 'c', 'd'])
    tmp = grade.apply(lambda x: int(math.sqrt(x)*10))
    assert np.all(tmp.values == np.array([100, 94, 89, 77])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd']))
    tmp = grade.apply(np.mean)
    assert tmp == 82.5
    # test unchange
    assert np.all(grade.values == np.array([100, 90, 80, 60])) and \
           np.all(grade.index == np.array(['a', 'b', 'c', 'd']))

def test_map():
    tmp = a.map({i: i+3 for i in range(5)})
    assert np.all(tmp.values == np.array([3, 4, 5, 6, 7])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd', 'e']))
    # test unchange
    assert np.all(a.values == np.arange(5)) and \
           np.all(a.index == np.array(['a', 'b', 'c', 'd', 'e']))