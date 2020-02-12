
from skyool.database import *
from skyool.syntax import *


db = Database("example", [
    TableDefn("people", [
        ColDefn("name", str),
        ColDefn("age", int),
        ColDefn("fave_fruit", str),
    ]),
    TableDefn("fruits", [
        ColDefn("name", str),
        ColDefn("color", str),
    ]),
])
db.tables["people"].add(
    ("Joe", 12, "pear"),
    ("Mack", 45, "peach"),
    ("Ricky F", 32, "grape"),
)

values = Select("people", ["name", "fave_fruit"]).run(db)
assert values == [
    ("Joe", "pear"),
    ("Mack", "peach"),
    ("Ricky F", "grape"),
]


example_transaction = [
    Create("people", [ColDefn("id", int), ColDefn("name", str), ColDefn("age", int)]),
    Insert("people", ("id", "name", "age"), [
        (1, "Joe", 23),
        (2, "Mark", 46),
    ]),
    Select("people", ["name", "age"]),
]
