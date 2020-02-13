from typing import NamedTuple, Sequence, Optional, Any


class Expr:
    def eval(self, table, row):
        raise NotImplementedError("Implement me!")

class Val(Expr, NamedTuple):
    value: Any
    def eval(self, table, row):
        return self.value

class Col(Expr, NamedTuple):
    name: str
    def eval(self, table, row):
        col_ind = table.get_col_ind(self.name)
        return row[col_ind]


class Unop(Expr, NamedTuple):
    x: Expr
    def op(self, xval):
        raise NotImplementedError("Implement me!")
    def eval(self, table, row):
        xval = self.x.eval(table, row)
        return self.op(xval)

class Neg(Unop):
    def op(self, xval):
        return -xval

class Inv(Unop):
    def op(self, xval):
        return ~xval

class Not(Unop):
    def op(self, xval):
        return not xval

class Len(Unop):
    def op(self, xval):
        return len(xval)


class Binop(Expr, NamedTuple):
    x: Expr
    y: Expr
    def op(self, xval, yval):
        raise NotImplementedError("Implement me!")
    def eval(self, table, row):
        xval = self.x.eval(table, row)
        yval = self.y.eval(table, row)
        return self.op(xval, yval)

class In(Binop):
    def op(self, xval, yval):
        return xval in yval

class Add(Binop):
    def op(self, xval, yval):
        return xval + yval

class Sub(Binop):
    def op(self, xval, yval):
        return xval - yval

class Mul(Binop):
    def op(self, xval, yval):
        return xval * yval

class Div(Binop):
    def op(self, xval, yval):
        return xval / yval

class Mod(Binop):
    def op(self, xval, yval):
        return xval % yval

class Eq(Binop):
    def op(self, xval, yval):
        return xval == yval

class Ne(Binop):
    def op(self, xval, yval):
        return xval != yval

class Lt(Binop):
    def op(self, xval, yval):
        return xval < yval

class Gt(Binop):
    def op(self, xval, yval):
        return xval > yval

class Le(Binop):
    def op(self, xval, yval):
        return xval <= yval

class Ge(Binop):
    def op(self, xval, yval):
        return xval >= yval

class And(Binop):
    def op(self, xval, yval):
        return xval and yval

class Or(Binop):
    def op(self, xval, yval):
        return xval or yval
