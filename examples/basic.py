
from skyool import *


db = Database("example")

result_tables = db.execute(
    Create("people", [
        ("name", str),
        ("age", int),
        ("fave_fruit", str),
    ]),
    Insert("people", None, [
        ("Joe", 12, "pear"),
        ("Mack", 45, "peach"),
        ("Ricky F", 32, "grape"),
    ]),
    Select("people", ["name", "fave_fruit"]),
    Select("people", ["age"], In(Val("pea"), Col("fave_fruit"))),
    Select("people", ["age", "name"], Gt(Len(Col("name")), Val(3))),
    Drop("people"),
)

assert [table.rows for table in result_tables] == [
    [
        ("Joe", "pear"),
        ("Mack", "peach"),
        ("Ricky F", "grape"),
    ],
    [(12,), (45,)],
    [
        (45, "Mack"),
        (32, "Ricky F"),
    ],
]

