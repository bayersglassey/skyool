from typing import NamedTuple, Sequence, List, Tuple, Optional

from skyool.database import Database, Row, ColDefn, TableDefn, Table, Type
from skyool.expr import Expr


class Command:
    def run(self, db: Database) -> Optional[List[Table]]:
        raise NotImplementedError("Implement me!")


class Select(Command, NamedTuple):

    table: str
    cols: Optional[Sequence[str]] = None
    where: Optional[Expr] = None
    groupby: Optional[Expr] = None
    having: Optional[Expr] = None
    orderby: Optional[Expr] = None
    distinct: bool = False
    offset: int = 0
    fetchfirst: Optional[int] = None

    def run(self, db: Database) -> Optional[List[Table]]:
        table = db.tables[self.table]
        col_inds = table.get_col_inds(self.cols)
        col_defns = table.defn.cols
        rows = table.rows

        # Filter columns
        if self.where is not None:
            rows = [row for row in rows
                if self.where.eval(table, row)]

        # Reorder columns
        col_defns = [col_defns[ind] for ind in col_inds]
        rows = [
            Row(row[ind] for ind in col_inds)
            for row in rows]

        # Build & return new table
        new_table_defn = TableDefn(table.defn.name, col_defns)
        new_table = Table(new_table_defn, rows)
        return new_table

class Create(Command, NamedTuple):
    table: str
    cols: Sequence[Tuple[str, Type]]
    def run(self, db: Database) -> Optional[List[Table]]:
        col_defns = [ColDefn(col, type) for col, type in self.cols]
        table_defn = TableDefn(self.table, col_defns)
        table = db.create(table_defn)

class Drop(Command, NamedTuple):
    table: str
    def run(self, db: Database) -> Optional[List[Table]]:
        db.drop(self.table)

class Insert(Command, NamedTuple):
    table: str
    cols: Optional[Sequence[str]] = None
    values: Optional[Sequence[Row]] = None
    def run(self, db: Database) -> Optional[List[Table]]:
        if self.values is None:
            return
        table = db.tables[self.table]
        cols = self.cols
        if cols is None:
            cols = list(table.col_names)
        col_inds = [table.col_names.index(col) for col in cols]
        table.add(*self.values)

class Update(Command, NamedTuple):
    table: str
    set: Expr
    where: Expr

class Delete(Command, NamedTuple):
    table: str
    where: Expr

