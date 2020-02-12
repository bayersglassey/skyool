
from skyool.database import *
from skyool.syntax import *


db = Database("example")

results = db.execute(
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
    Select("people", ["age"]),
    Select("people", ["age", "name"]),
    Drop("people"),
)

assert results == [
    [
        ("Joe", "pear"),
        ("Mack", "peach"),
        ("Ricky F", "grape"),
    ],
    [(12,), (45,), (32,)],
    [
        (12, "Joe"),
        (45, "Mack"),
        (32, "Ricky F"),
    ],
]

