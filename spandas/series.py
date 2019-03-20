"""
faster version of Series
"""
import numpy as np
import pandas as pd
"""
A Series is basically a data structure with 2 numpy array: 
    one to store value and the other to store index
"""
class Series:
    # initiate with pandas Series
    def __init__(self, values, index=None, copy=True):
        # try to convert values into a np array
        try:
            self.values = np.array(values, copy=copy)
        except:
            raise valuesError("values is not good")
        if index is not None:
            assert len(values) == len(index), \
                "length of values and index not match!"
            self.index = np.array(index, copy=copy)
        else:
            self.index = np.arange(len(values))

    def __str__(self):
        res = ""
        if len(self) <= 10:
            for i in range(len(self)):
                res += ("{:>5}{:>5}\n".format(self.index[i], self.values[i]))
        else:
            for i in range(5):
                res += ("{:>5}{:>5}\n".format(self.index[i], self.values[i]))
            res += ('... ...\n')
            for i in range(5):
                res += ("{:>5}{:>5}\n".format(self.index[len(self)-5+i], self.values[len(self)-5+i]))
        res += "dtype: {}".format(self.values.dtype)
        return res

    # len()
    def __len__(self):
        return len(self.values)

    """
    comparing operator
    just use the one for numpy
    """
    # >
    def __gt__(self, s):
        if isinstance(s, Series):
            tmp = self.values > s.values
        else:
            tmp = self.values > s
        return Series(tmp, self.index)

    # >=
    def __ge__(self, s):
        if isinstance(s, Series):
            tmp = self.values >= s.values
        else:
            tmp = self.values >= s
        return Series(tmp, self.index)

    # <
    def __lt__(self, s):
        if isinstance(s, Series):
            tmp = self.values < s.values
        else:
            tmp = self.values < s
        return Series(tmp, self.index)

    # <=
    def __le__(self, s):
        if isinstance(s, Series):
            tmp = self.values <= s.values
        else:
            tmp = self.values <= s
        return Series(tmp, self.index)

    # ==
    def __eq__(self, s):
        if isinstance(s, Series):
            tmp = self.values == s.values
        else:
            tmp = self.values == s
        return Series(tmp, self.index)

    # !=
    def __ne__(self, s):
        if isinstance(s, Series):
            tmp = self.values != s.values
        else:
            tmp = self.values != s
        return Series(tmp, self.index)

    """
    indexing
    TODO: index slice
    """
    # all get does not copy
    def __getitem__(self, key):
        # boolean
        if isinstance(key, Series):
            assert len(self) == len(key), "the length of key does not match!"
            return Series(self.values[key.values], self.index[key.values], copy=False)
        try:
            return Series(self.values[key], self.index[key], copy=False)
        except:
            return self.values[key]

    # TODO: assign a number to a series
    def __setitem__(self, key, value):
        if isinstance(key, Series):
            assert len(self) == len(key), "the length of key does not match!"
            self.values[key.values] = value
        elif isinstance(key, list):
            key = np.array(key, copy=False)
        self.values[key] = value

    def __iter__(self):
        for v in self.values:
            yield v
    
    def items(self):
        return zip(iter(self.index), iter(self.values))

    def append(self, s):
        # TODO: only support list of series now
        if isinstance(s, list):
            res_values, res_index = list(self.values), list(self.index)
            for l in s:
                res_values += list(l.values)
                res_index += list(l.index)
            assert len(res_values) == len(res_index), \
                "length of result values and index does not match"
            return Series(res_values, res_index)
        return Series(list(self.values) + list(s.values), list(self.index) + list(s.index))

    def apply(self, f):
        vf = np.vectorize(f)
        return Series(vf(self.values), self.index)

    def head(self, l = 5):
        res = ""
        for i in range(min(l, len(self))):
            res += ("{:>5}{:>5}\n".format(self.index[i], self.values[i]))
        return res

    def replace(self, d):
        return Series([d[x] for x in self.values])
    
    def copy(self):
        return Series(self.values, self.index)