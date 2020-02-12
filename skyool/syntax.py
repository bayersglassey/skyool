from typing import NamedTuple, Sequence, Optional

from skyool.database import Row, ColDefn


class Expr(NamedTuple):
    pass

class Select(NamedTuple):

    table: str
    cols: Optional[Sequence[str]] = None
    where: Optional[Expr] = None
    groupby: Optional[Expr] = None
    having: Optional[Expr] = None
    orderby: Optional[Expr] = None
    distinct: bool = False
    offset: int = 0
    fetchfirst: Optional[int] = None

    def run(self, db):
        table = db.tables[self.table]
        cols = self.cols
        if cols is None:
            cols = list(table.col_names)
        col_inds = [table.col_names.index(col) for col in cols]
        values = [
            Row(row[ind] for ind in col_inds)
            for row in table.rows]
        return values

class Insert(NamedTuple):
    table: str
    cols: Optional[Sequence[str]] = None
    values: Optional[Sequence[Row]] = None

class Create(NamedTuple):
    table: str
    cols: Sequence[ColDefn]

class Update(NamedTuple):
    table: str
    set: Expr
    where: Expr

class Delete(NamedTuple):
    table: str
    where: Expr

class Drop(NamedTuple):
    table: str

