from .series import Series
from collections.abc import Iterable
import numpy as np
class DataFrame:
    def __init__(self, values, index=None, copy=True):
        self.dict = {}
        l = 0
        try:
            for key, value in values.items():
                if l == 0:
                    l = len(value)
                else:
                    assert l == len(value), "the length of each column must match!"
                self.dict[key] = np.array(value, copy=copy)
        except:
            for key, value in values.items():
                self.dict[key] = np.array([value], copy=copy)
        if index is not None:
            assert l == len(index), "the length of each column must match!"
            self.index = np.array(index, copy=copy)
        else:
            self.index = np.array(range(l), copy=copy)

    def __str__(self):
        res = ""
        if len(self) <= 10:
            for i in range(len(self)):
                res += "{:>5}".format(self.index[i])
                for key in self.keys():
                    res += ("{:>5}".format(self.dict[key][i]))
                res += "\n"
        else:
            for i in range(5):
                res += "{:>5}".format(self.index[i])
                for key in self.keys():
                    res += ("{:>5}".format(self.dict[key][i]))
                res += "\n"
            res += ('... ...\n')
            for i in range(5):
                res += "{:>5}".format(self.index[len(self) - 5 + i])
                for key in self.keys():
                    res += ("{:>5}".format(self.dict[key][len(self) - 5 + i]))
                res += "\n"
        return res
    
    def __len__(self):
        return len(self.index)

    def __getitem__(self, key):
        # index with column name
        if isinstance(key, list):
            if len(key) == 1:
                return Series(self.dict[key[0]], self.index, copy=False)
            else:
                return DataFrame({k: self.dict[k] for k in key}, self.index, copy=False)
        # index with boolean Series
        elif isinstance(key, Series):
            assert len(key) == len(self)
            return DataFrame({k: v[key.values] for k, v in self.dict.items()}, self.index[key.values], copy=False)
        else:
            if not isinstance(key, Iterable) and not isinstance(key, slice):
                key = [key]
            return DataFrame({k: v[key] for k, v in self.dict.items()}, self.index[key], copy=False)

    # when assigning with column and row, 
    # please always use the row first and column second
    # because numpy advance indexing will return a copy instead for a view
    def __setitem__(self, key, value):
        # index with column name
        if isinstance(key, list):
            if isinstance(value, Series):
                value = value.values
            for k in key:
                if k in self.dict:
                    self.dict[k][:] = value
                else:  # add new column
                    self.dict[k] = np.empty(len(self))
                    self.dict[k][:] = value
        # index with boolean Series
        elif isinstance(key, Series):
            for k in self:
                self.dict[k][key.values] = value
        else:
            if not isinstance(key, Iterable) and not isinstance(key, slice):
                key = np.array([key])
            for k in self:
                self.dict[k][key] = value

    def head(self, l = 5):
        res = ""
        for i in range(min(l, len(self))):
            res += "{:>5}".format(self.index[i])
            for key in self.keys():
                res += ("{:>5}".format(self.dict[key][i]))
            res += "\n"
        return res

    def __iter__(self):
        for k in self.dict:
            yield k

    def items(self):
        for k, v in self.dict.items():
            yield k, v

    def iterrows(self):
        for i in range(len(self.index)):
            yield self.index[i], {k: v[i] for k, v in self.dict.items()}

    def append(self, s):
        # only support append list of DataFrame now
        if isinstance(s, list):
            res_dict = {k: list(v) for k, v in self.dict.items()}
            res_index = list(self.index)
            for d in s:
                assert d.keys() == res_dict.keys(), "key not conform"
                if isinstance(d, dict):
                    d = DataFrame(d, copy=False)
                for k in res_dict.keys():
                    res_dict[k] += list(d.dict[k])
                res_index += list(d.index)
            return DataFrame(res_dict, res_index)

    def keys(self):
        return self.dict.keys()
    
    def copy(self):
        return DataFrame(self.dict, self.index)