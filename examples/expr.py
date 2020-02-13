
from skyool import *


db = Database("example")

tables = db.execute(
    Create("people", [
        ("name", str),
        ("age", int),
        ("fave_fruit", str),
    ]),
    Insert("people", None, [
        ("Joe", 12, "pear"),
        ("Mack", 45, "peach"),
        ("Rick", 32, "grape"),
    ]),
    Select("people", ["name"], Lt(Col("age"), Val(40))),
    Select("people", ["name"], Eq(Len(Col("name")), Val(4))),
)

assert [table.rows for table in tables] == [
    [("Joe",), ("Rick",)],
    [("Mack",), ("Rick",)],
]

