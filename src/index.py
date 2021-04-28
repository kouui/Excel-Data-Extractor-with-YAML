
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

_col_index = {letters[i]:i+1 for i in range(len(letters))}
_col_index2 = {}
for c1 in letters:
    for c2 in letters:
        _col_index2[c1+c2] = _col_index[c1] * 26 + _col_index[c2]

def C(c):
    length = len(c)
    if length == 1:
        return _col_index[c] - 1
    elif length == 2:
        return _col_index2[c] - 1
    else:
        raise ValueError("Only A-Z, AA-ZZ are supported.")

def R(r):
    try:
        return r-1
    except TypeError:
        return int(r) - 1
