"""Tidy a list of store names."""

import json
import os


def clean(names, seen=[]):
    for name in names:
        if name == None:
            continue
        seen.append(name.strip())
    return seen


print(json.dumps(clean(["Pearl St ", " University Hill"])))
