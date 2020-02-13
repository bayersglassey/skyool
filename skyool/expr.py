from typing import NamedTuple, Sequence, Optional


class Expr:
    def eval(self, db, row):
        raise NotImplementedError("Implement me!")


class Unop(Expr, NamedTuple):
    x: Expr
    def op(self, xval):
        raise NotImplementedError("Implement me!")
    def eval(self, db, row):
        xval = self.x.run(db, row)
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


class Binop(Expr, NamedTuple):
    x: Expr
    y: Expr
    def op(self, xval, yval):
        raise NotImplementedError("Implement me!")
    def eval(self, db, row):
        xval = self.x.run(db, row)
        yval = self.y.run(db, row)
        return self.op(xval, yval)

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
