
# SKYOOL


## Overview

Attempting to write a SQL engine in Python, in the quickest-n-dirtiest way possible.

Ended up being an exploration of Python 3.6+ type annotation stuff, like typing.NamedTuple.


## Getting started

In a fresh virtualenv:

    $ pip install -r requirements.txt

Then, in a Python shell:

    from skyool.database import Database
    from skyool.syntax import Create, Insert, Select, Drop


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

Go forth and SQL.
