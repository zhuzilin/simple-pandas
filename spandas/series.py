"""
faster version of Series
"""
import numpy as np

"""
A Series is basically a data structure with 2 numpy array: 
    one to store value and the other to store index
"""
class Series:
    # initiate with pandas Series
    def __init__(self, values, index=None, copy=True):
        if isinstance(values, dict):
            if index is None:
                index = list(values.keys())
                values = list(values.values())
            else:
                values = [values[k] if k in values else np.nan for k in index]
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
                res += ("{:>7}{:>7}\n".format(self.index[i], self.values[i]))
        else:
            for i in range(5):
                res += ("{:>7}{:>7}\n".format(self.index[i], self.values[i]))
            res += ('... ...\n')
            for i in range(5):
                res += ("{:>7}{:>7}\n".format(self.index[len(self)-5+i], self.values[len(self)-5+i]))
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
    arithmetic
    """
    # +
    def __add__(self, s):
        if isinstance(s, Series):
            tmp = self.values + s.values
        else:
            tmp = self.values + s
        return Series(tmp, self.index)
    
    # -
    def __sub__(self, s):
        if isinstance(s, Series):
            tmp = self.values - s.values
        else:
            tmp = self.values - s
        return Series(tmp, self.index)
    
    # *
    def __mul__(self, s):
        if isinstance(s, Series):
            tmp = self.values * s.values
        else:
            tmp = self.values * s
        return Series(tmp, self.index)
    
    # /
    def __truediv__(self, s):
        if isinstance(s, Series):
            tmp = self.values / s.values
        else:
            tmp = self.values / s
        return Series(tmp, self.index)
    """
    indexing
    TODO: index slice
    """
    # all get does not copy
    def __getitem__(self, key):
        return self.get_by_row(key)
    
    def get_by_row(self, key):
        # boolean
        if isinstance(key, Series):
            assert len(self) == len(key), "the length of key does not match!"
            return Series(self.values[key.values], self.index[key.values], copy=False)
        try:
            return Series(self.values[key], self.index[key], copy=False)
        except:
            return self.values[key]
    
    def get_by_index(self, key):
        if not isinstance(key, list):
            key = [key]
        row2index = dict(zip(range(len(self)), self.index))
        key_row = [r for r, i in row2index.items() if i in key]
        return self[np.array(key_row, copy=False)]
    
    def __setitem__(self, key, value):
        self.set_by_row(key, value)

    def set_by_row(self, key, value):
        if isinstance(key, Series):
            assert len(self) == len(key), "the length of key does not match!"
            self.values[key.values] = value
        elif isinstance(key, list):
            key = np.array(key, copy=False)
        self.values[key] = value

    def set_by_index(self, key, value):
        try:
            k2v = dict(zip(key, value))
        except:
            k2v = {key: value}
        row2index = dict(zip(range(len(self)), self.index))
        key_row = [r for r, i in row2index.items() if i in k2v]
        value_row = [k2v[row2index[r]] for r in key_row]
        assert len(key_row) == len(value_row)
        self[np.array(key_row, copy=False)] = value_row
        
    def __iter__(self):
        for v in self.values:
            yield v
    
    def items(self):
        return zip(iter(self.index), iter(self.values))

    def append(self, s):
        # TODO: only support list of series now
        if isinstance(s, list):
            append_values = [l.values for l in s]
            append_index = [l.index for l in s]
            return Series(np.append(self.values, append_values), np.append(self.index, append_index))
        return Series(np.append(self.values, s.values), np.append(self.index, s.index))

    def apply(self, f, type='element'):
        if type == 'element':
            vf = np.vectorize(f)
            return Series(vf(self.values), self.index)
        elif type == 'column':
            return f(self.values)
        else:
            raise "type error!"

    def head(self, l = 5):
        res = ""
        for i in range(min(l, len(self))):
            res += ("{:>7}{:>7}\n".format(self.index[i], self.values[i]))
        return res

    def map(self, d, drop=True):
        if drop:
            return Series([d[x] if x in d else np.nan for x in self.values], self.index)
        else:
            return Series([d[x] if x in d else x for x in self.values], self.index)
    
    def copy(self):
        return Series(self.values, self.index)
    
    @property
    def dict(self):
        res = dict(zip(self.index, self.values))
        assert len(res) == len(self), "index have repetitive terms"
        return res
    
    def isnull(self):
        return Series(np.isnan(self.values), self.index)
    
    