
# SKYOOL


## Overview

Attempting to write a SQL engine in Python, in the quickest-n-dirtiest way possible.

Ended up being an exploration of Python 3.6+ type annotation stuff, like typing.NamedTuple.


## Getting started

In a fresh virtualenv:

    $ pip install -r requirements.txt

Then, in a Python shell:

    from skyool import (
        # This is important
        Database,

        # SQL commands
        Create, Insert, Select, Drop,

        # Expressions
        Val, Col, Len, In, Gt,
    )


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

Go forth and SQL.
