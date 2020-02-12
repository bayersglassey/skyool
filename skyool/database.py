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

    def __init__(self, defn: TableDefn):
        self.defn = defn
        self.rows = []
        self.col_names = tuple(col_defn.name for col_defn in defn.cols)

    def check(self):
        n_cols = len(self.defn.cols)
        for row in self.rows:
            assert len(row) == n_cols

    def add(self, *rows):
        for row in rows:
            assert len(row) == len(self.defn.cols)
            self.rows.append(row)


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
        results = []
        for cmd in cmds:
            result = cmd.run(self)
            if result is not None:
                results.append(result)
        return results
