from spandas import DataFrame
from spandas import Series
import pandas as pd
import numpy as np
import math

values = {'a': np.array([1, 2, 3]), 
          'b': np.array([4, 5, 6]), 
            1: np.array([6, 7, 8])}
index = np.array(['a', 'b', 'c'])
a = DataFrame(values, index)

def test_constructor():
    assert a.keys() == list(values.keys())
    tmp = DataFrame(values, index, copy=False)
    for k in values:
        assert id(values[k]) == id(tmp.dict[k])
    assert id(index) == id(tmp.index)
    # initialize with pd.DataFrame
    tmp_df = pd.DataFrame(values, index)
    tmp = DataFrame(tmp_df, tmp_df.index)
    for k in values:
        assert np.all(values[k] == tmp.dict[k])
    assert np.all(index == tmp.index)

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
    # get by index
    tmp = a.get_by_index(['a', 'c'])
    assert np.all(tmp.dict['a'] == np.array([1, 3])) and \
           np.all(tmp.dict['b'] == np.array([4, 6])) and \
           np.all(tmp.dict[1] == np.array([6, 8])) and \
           np.all(tmp.index == np.array(['a', 'c']))
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
    tmp = a.copy()
    tmp.set_by_index(['a', 'c'], [20, 30])
    assert np.all(tmp.dict['a'] == np.array([20, 2, 30])) and \
           np.all(tmp.dict['b'] == np.array([20, 5, 30])) and \
           np.all(tmp.dict[1] == np.array([20, 7, 30])) and \
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
    tmp = a.copy()
    tmp[['a', 'b']].set_by_index('c', 30)
    assert np.all(tmp.dict['a'] == np.array([1, 2, 30])) and \
           np.all(tmp.dict['b'] == np.array([4, 5, 30])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c']))

def test_transpose():
    tmp = a.T
    assert np.all(tmp.dict['a'] == np.array([1, 4, 6])) and \
           np.all(tmp.dict['b'] == np.array([2, 5, 7])) and \
           np.all(tmp.dict['c'] == np.array([3, 6, 8])) and \
           np.all(tmp.index == np.array(['a', 'b', 1]))

def test_len():
    assert len(a) == 3

def test_columns():
    assert a.columns == ['a', 'b', 1]

def test_append():
    tmp_append = DataFrame({'a': [0], 'b': [1], 1: [2]})
    tmp = a.append(tmp_append)
    assert np.all(tmp.dict['a'] == np.array([1, 2, 3, 0])) and \
           np.all(tmp.dict['b'] == np.array([4, 5, 6, 1])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8, 2])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 0]))
    tmp = a.append([tmp_append, tmp_append])
    assert np.all(tmp.dict['a'] == np.array([1, 2, 3, 0, 0])) and \
           np.all(tmp.dict['b'] == np.array([4, 5, 6, 1, 1])) and \
           np.all(tmp.dict[1] == np.array([6, 7, 8, 2, 2])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 0, 0]))

def test_iter():
    tmp = ""
    for k in a:
        tmp += str(k)
    assert tmp == "ab1"
    tmp = ""
    tmp_sum = 0
    for k, v in a.items():
        tmp += str(k)
        tmp_sum += v.sum()
    assert tmp == "ab1" and tmp_sum == 42
    tmp = ""
    tmp_sum = 0
    for k, v in a.iterrows():
        tmp += str(k)
        tmp_sum += v['b']
    assert tmp == "abc" and tmp_sum == 15

def test_apply():
    grade = DataFrame({'A': [100, 90, 80, 60],
                           'B': [90, 85, 85, 100],
                           'C': [70, 100, 100, 80]},
                          index=['a', 'b', 'c', 'd'])
    # element-wise
    tmp = grade.apply(lambda x: int(math.sqrt(x)*10))
    assert np.all(tmp.dict['A'] == np.array([100, 94, 89, 77])) and \
           np.all(tmp.dict['B'] == np.array([94, 92, 92, 100])) and \
           np.all(tmp.dict['C'] == np.array([83, 100, 100, 89])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd']))
    # row-wise
    tmp = grade.apply(lambda x: x['A']+x['B']+x['C'], type='row')
    assert np.all(tmp.values == np.array([260, 275, 265, 240])) and \
           np.all(tmp.index == np.array(['a', 'b', 'c', 'd']))
    # column wise
    tmp = grade.apply(lambda x: int(x.mean()), type='column')
    assert np.all(tmp.values == np.array([82, 90, 87])) and \
           np.all(tmp.index == np.array(['A', 'B', 'C']))
    # test unchanged
    assert np.all(grade.dict['A'] == np.array([100, 90, 80, 60])) and \
           np.all(grade.dict['B'] == np.array([90, 85, 85, 100])) and \
           np.all(grade.dict['C'] == np.array([70, 100, 100, 80])) and \
           np.all(grade.index == np.array(['a', 'b', 'c', 'd']))