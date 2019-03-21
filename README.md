# simple pandas

 ![travis](https://travis-ci.com/zhuzilin/simple-pandas.svg?branch=master)

 ![](https://66.media.tumblr.com/decf9e4a17b56f692c929088e519f032/tumblr_p2q1ak7m3G1uaogmwo9_250.png)

[pandas](http://pandas.pydata.org/pandas-docs/stable/) is a powerful library for data science. However, it it really complex... Most of the time, I only need to make some small change of our data, but the indexing(`loc`, `iloc`, `at`, `ix`...) is 😭😭😭. If this happens to you as well, then feel free to try my solution to simplify pandas!

## Contents

- Installation
- How simpel can it be
- Interact with pandas
- Indexing
- Assignment
- Boost

## Installation

```bash
pip install simple-pandas
```

## How simple can it be?

In simple pandas, the Series is only two numpy array, one for values and one for index. And a DataFrame is only a dictionary and an index. In any time during the manipulation, you could use:

```python
series.values, series.index
dataframe.dict, dataframe.index
```

to visit and modify them directly!

Also, simple pandas have much easier indexing and assignment system! Easy to remember and easy to use!

For a simple exploratory, see [here](https://github.com/zhuzilin/simple-pandas/blob/master/introduction.ipynb)

## Interact with pandas

And to make it simple, this library does not include some method like `read_csv` and we may need to cast from simple pandas to pandas. To turn a pandas Series or DataFrame into a simple pandas Series or DataFrame, we only need:

```python
import spandas as spd
ps = spd.Series(s, s.index)
pdf = spd.DataFrame(df, df.index)
```

And to convert back, only:

```python
import pandas as pd
s = pd.Series(ps.values, ps.index)
df = pd.DataFrame(pdf.dict, pdf.idnex)
```

## Indexing

And now the indexing! 

Notice all indexing **will not return a copy**. And to get a copy, please use `.copy()` method.

### Series

```python
>>> a = spd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
>>> print(a)
      a      1
      b      2
      c      3
      d      4
      e      5
dtype: int32
```

The default index for a Series is the **row number**.

```python
>>> a[3]
4
>>> print(a[1:3])
    b    2
    c    3
dtype: int32
```

And of course, we could index with a boolean Series

```python
>>> print(a[a>2])
      c      3
      d      4
      e      5
dtype: int32
```

And to index with the index label, we need to:

```python
>>> print(a[a.index == 'e'])
      e      5
dtype: int32
>>> print(a.get_by_index('e'))
      e      5
dtype: int32
>>> print(a[np.isin(a.index, ['b', 'c'])])
      b      2
      c      3
dtype: int32
>>> print(a.get_by_index(['c', 'b']))
      b      2
      c      3
dtype: int32
```

### DataFrame

```python
>>> values = {'a': np.array([1, 2, 3]),
...           'b': np.array([4, 5, 6]),
...             1: np.array([6, 7, 8])}
>>> index = np.array(['a', 'b', 'c'])
>>> a = spd.DataFrame(values, index)
>>> print(a)
  index      a      b      1
      a      1      4      6
      b      2      5      7
      c      3      6      8
```

The default index for a DataFrame is also  the **row number**.

```python
>>> print(a[2])
  index      a      b      1
      c      3      6      8
>>> print(a[np.array([1, 2])])
  index      a      b      1
      b      2      5      7
      c      3      6      8
>>> print(a[1:3])
  index      a      b      1
      b      2      5      7
      c      3      6      8
>>> print(a.get_by_index(['a', 'c']))
  index      a      b      1
      a      1      4      6
      c      3      6      8
```

And to index with the column, we could use double square bracket:

``` python
>>> print(a[['a']])
    a    1
    b    2
    c    3
dtype: int32
>>> print(a[['a', 1]])
  index      a      1
      a      1      6
      b      2      7
      c      3      8
```

## Assignment

Because we only return view of the original data when indexing, it is very easy to assign new values.

### Series

```python
>>> tmp = a.copy()
>>> tmp[1] = 10
>>> print(tmp)
      a      1
      b     10
      c      3
      d      4
      e      5
dtype: int32
>>> tmp = a.copy()
>>> tmp[np.array([1, 2, 3])] = 10
>>> print(tmp)
      a      1
      b     10
      c     10
      d     10
      e      5
dtype: int32
>>> tmp = a.copy()
>>> tmp[a.index == 'e'] = 10
>>> print(tmp)
      a      1
      b      2
      c      3
      d      4
      e     10
dtype: int32
>>> tmp = a.copy()
>>> tmp.set_by_index(['e', 'd'], [10, 9])
>>> print(tmp)
      a      1
      b      2
      c      3
      d      9
      e     10
dtype: int32
```

### DataFrame

We could update rows:

```python
>>> tmp = a.copy()
>>> tmp[0] = 30
>>> print(tmp)
  index      a      b      1
      a     30     30     30
      b      2      5      7
      c      3      6      8
>>> tmp = a.copy()
>>> tmp[:2] = 30
>>> print(tmp)
  index      a      b      1
      a     30     30     30
      b     30     30     30
      c      3      6      8
>>> tmp = a.copy()
>>> tmp[np.array([0, 2])] = 30
>>> print(tmp)
  index      a      b      1
      a     30     30     30
      b      2      5      7
      c     30     30     30
>>> tmp = a.copy()
>>> tmp.set_by_index(['a', 'c'], [20, 30])
>>> print(tmp)
  index      a      b      1
      a     20     20     20
      b      2      5      7
      c     30     30     30
```

We could update the whole column or append new rows.

```python
>>> tmp = a.copy()
>>> tmp[['a', 'c']] = 1
>>> print(tmp)
  index      a      b      1      c
      a      1      4      6    1.0
      b      1      5      7    1.0
      c      1      6      8    1.0
>>> tmp = a.copy()
>>> tmp[['a', 'c']] = [3, 2, 1]
>>> print(tmp)
  index      a      b      1      c
      a      3      4      6    3.0
      b      2      5      7    2.0
      c      1      6      8    1.0
```

And finally, the nested assignment

```python
>>> tmp = a.copy()
>>> tmp[['b']][:2] = 30
>>> print(tmp)
  index      a      b      1
      a      1     30      6
      b      2     30      7
      c      3      6      8
>>> tmp = a.copy()
>>> tmp[['a', 'b']][np.array([0, 2])] = 30
>>> print(tmp)
  index      a      b      1
      a     30     30      6
      b      2      5      7
      c     30     30      8
>>> tmp = a.copy()
>>> tmp[['a', 'b']].set_by_index('c', 30)
>>> print(tmp)
  index      a      b      1
      a      1      4      6
      b      2      5      7
      c     30     30      8
```

Notice: because that all advance indexing for a numpy array will create a copy, you must put the column index before row index to achieve correct nested assignment.

## Boost

Apart from a simple indexing mechanism, I have changed some of the method for pandas Series and DataFrame to make it faster. The test result will be update here soon. And notice if some function is not listed below, the pandas version may be better.

### Series

The test for Series is [here](https://github.com/zhuzilin/simple-pandas/blob/master/series_time.ipynb)

| method  | boost |
| :------ | ----- |
| append  | 10x   |
| apply   | 1.5x  |
| replace | 100x  |

### DataFrame

The test for DataFrame is [here](https://github.com/zhuzilin/simple-pandas/blob/master/dataframe_time.ipynb)

| method  | boost |
| ------- | ----- |
| append  | 20x   |
| iterrow | 30x   |

