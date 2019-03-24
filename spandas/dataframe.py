from .series import Series
from collections.abc import Iterable
import numpy as np
class DataFrame:
    def __init__(self, values, index=None, columns=None, copy=True):
        self.dict = {}
        l = 0
        try:
            if columns is not None:
                for key in columns:
                    try:
                        value = values[key]
                    except:
                        continue
                    if l == 0:
                        l = len(value)
                    else:
                        assert l == len(value), "the length of each column must match!"
                    self.dict[key] = np.array(value, copy=copy)
                for key in columns:
                    if key not in self.dict:
                        self.dict[key] = np.empty(l)
                        self.dict[key][:] = np.nan
            else:
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
        res = "{:>7}".format("index")
        for k in self.keys():
            res += "{:>7}".format(k)
        res += "\n"
        if len(self) <= 10:
            for i in range(len(self)):
                res += "{:>7}".format(self.index[i])
                for key in self.keys():
                    res += ("{:>7}".format(self.dict[key][i]))
                res += "\n"
        else:
            for i in range(5):
                res += "{:>7}".format(self.index[i])
                for key in self.keys():
                    res += ("{:>7}".format(self.dict[key][i]))
                res += "\n"
            res += ('... ...\n')
            for i in range(5):
                res += "{:>7}".format(self.index[len(self) - 5 + i])
                for key in self.keys():
                    res += ("{:>7}".format(self.dict[key][len(self) - 5 + i]))
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
    
    def get_by_index(self, key):
        if not isinstance(key, list):
            key = [key]
        row2index = dict(zip(range(len(self)), self.index))
        key_row = [r for r, i in row2index.items() if i in key]
        return self[np.array(key_row, copy=False)]
    
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

    def __delitem__(self, key):
        try:
            for k in key:
                try:
                    del self.dict[k]
                except:
                    pass
        except:
            del self.dict[key]

    def head(self, l = 5):
        res = "{:>7}".format("index")
        for k in self.keys():
            res += "{:>7}".format(k)
        res += "\n"
        for i in range(min(l, len(self))):
            res += "{:>7}".format(self.index[i])
            for key in self.keys():
                res += ("{:>7}".format(self.dict[key][i]))
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
        # only support append list of DataFrame or dict now
        if isinstance(s, list):
            append_dict = {k: [] for k in self.keys()}
            append_index = []
            for d in s:
                assert d.keys() == self.keys(), "keys not conform"
                if not isinstance(d, DataFrame):
                    d = DataFrame(d)
                for k in append_dict.keys():
                    append_dict[k].append(d.dict[k])
                append_index.append(d.index)
            res_dict = {k: np.append(self.dict[k], append_dict[k]) for k in self.keys()}
            res_index = np.append(self.index, append_index)
            return DataFrame(res_dict, res_index)
        else:
            if not isinstance(s, DataFrame):
                s = DataFrame(s)
            res_dict = {k: np.append(self.dict[k], s.dict[k]) for k in self.keys()}
            res_index = np.append(self.index, s.index)
            return DataFrame(res_dict, res_index)

    def keys(self):
        return list(self.dict.keys())
    
    def copy(self):
        return DataFrame(self.dict, self.index)
    
    @property
    def columns(self):
        return list(self.dict.keys())
    
    @property
    def T(self):
        res_index = self.columns
        res_columns = self.index
        res_values = np.array([self.dict[k] for k in res_index], copy=False).T
        res_dict = dict(zip(res_columns, res_values))
        return DataFrame(res_dict, index=res_index, columns=res_columns)

    def apply(self, func, type='element'):
        if type == 'element':
            f = np.vectorize(func)
            res_dict = {k: f(v) for k, v in self.dict.items()}
            return DataFrame(res_dict, self.index)
        elif type == 'row':
            res_values = []
            for _, v in self.iterrows():
                res_values.append(func(v))
            return Series(res_values, self.index)
        elif type == 'column':
            return Series([func(v) for _, v in self.items()], self.keys())