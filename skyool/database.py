from types import SimpleNamespace
from typing import NamedTuple, Tuple, Sequence, Optional, Type, Dict
from collections import OrderedDict


# For now, just use Python types as database types
Type = Type

class ColDefn(NamedTuple):
    name: str
    type: Type

class TableDefn(NamedTuple):
    name: str
    cols: Sequence[ColDefn]


# For now, rows are just tuples
Row = tuple


class Table(SimpleNamespace):

    defn: TableDefn
    rows: Sequence[Row]

    def __init__(self, defn: TableDefn, rows: Sequence[Row] = None):
        self.defn = defn
        self.rows = [] if rows is None else rows
        self.col_names = tuple(col_defn.name for col_defn in defn.cols)

    def check(self):
        n_cols = len(self.defn.cols)
        for row in self.rows:
            assert len(row) == n_cols

    def add(self, *rows):
        for row in rows:
            assert len(row) == len(self.defn.cols)
            self.rows.append(row)

    def get_col_ind(self, col_name):
        """Returns index of given column name"""
        return self.col_names.index(col_name)

    def get_col_inds(self, col_names=None):
        """Returns tuple of column indices given sequence of column names"""
        if col_names is None:
            col_names = self.col_names
        return tuple(self.col_names.index(col_name) for col_name in col_names)

    def show(self):
        """Prints human-readable table and returns None"""
        n_cols = len(self.col_names)
        rowstrs = [[str(val) for val in row] for row in self.rows]

        # Figure out printed column widths
        # (Just max width of all values we'll need to print in each column,
        # including column names)
        col_widths = [2] * n_cols
        for row in [self.col_names] + rowstrs:
            for i in range(n_cols):
                width = len(row[i])
                col_widths[i] = max(col_widths[i], width)

        # Define solid lines and lines showing values
        bars = ["-" * col_widths[i] for i in range(n_cols)]
        solid_line = "+" + "+".join(bars) + "+"
        def get_line(rowstr):
            padded_values = [
                val.rjust(col_widths[i])
                for i, val in enumerate(rowstr)]
            return "|" + "|".join(padded_values) + "|"

        # Actually print stuff
        print(solid_line)
        print(get_line(self.col_names))
        print(solid_line)
        for rowstrs in rowstrs:
            print(get_line(rowstrs))
        print(solid_line)


class Database(SimpleNamespace):

    name: str

    # I really want typing.OrderedDict, but it's not in Py36 :'(
    tables: Dict[str, Table]

    def __init__(self, name, table_defns: Sequence[TableDefn] = None):
        self.name = name
        self.tables = OrderedDict()
        if table_defns is not None:
            for defn in table_defns:
                self.create(table_defn)

    def create(self, defn: TableDefn):
        assert defn.name not in self.tables
        self.tables[defn.name] = Table(defn)

    def drop(self, table_name):
        del self.tables[table_name]

    def check(self):
        for table in self.tables.values():
            table.check()

    def execute(self, *cmds):
        tables = []
        for cmd in cmds:
            table = cmd.run(self)
            if table is not None:
                tables.append(table)
        return tables
