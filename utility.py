#!/usr/bin/python3
"""
This module contains some helper functions
"""
import re   # For regular expression
import MySQLdb


def param_to_dict(text=str()):
    """
    Return a dictionary representation of a parameter
    {<key name>: <value>}
    Sample:
        * input: name="My_little_house"
        * output: {'name': "My little house"}

        * input: price_by_night=25.52
        * output: {'price_by_night': 25.52}

        * input: max_guest=4
        * output: {'max_guest': 4}

        * input: name="California"
        * output: {'name': "California"}

        # Invalid input
        * input: nameaoj44dakh3n208;diab
        * output: None

    Syntax: <param>
    Param syntax: <key name>=<value>
    Value syntax:
        * String: "<value>" => starts with a double quote
            * any double quote inside the value must be escaped with \
a backslash \\
            * all underscores _ must be replace by spaces . \
Example: You want to set the string My little house to the attribute \
name, your command line must be name="My_little_house"
            * Float: <unit>.<decimal> => contains a dot .
            * Integer: <number> => default case
        * If any parameter doesn’t fit with these requirements or \
can’t be recognized correctly by your program, it must be skipped
    """
    if type(text) != str:
        print("** Invalid parameter to convert **")
        return

    # match <key name>=<value>
    paramRegex = re.compile(r"^(.+)(=)(.+)$")
    match = paramRegex.search(text)
    if match is None:
        return

    key_name = match.group(1)
    value = match.group(3)

    # Convert the value to the required type
    try:    # try converting to float
        value = float(value)
    except ValueError:
        try:    # try converting to int
            if value == int(value):
                value = int(value)
        except ValueError:
            try:   # Value is string: replace all underscores with spaces
                value = str(value)
                value = value.replace(str('_'), str(' '))
            except ValueError:
                pass    # do nothing to value

    attribute = {key_name: value}
    return attribute


def execsafe(cur, query, params=None):
    """
    Safely execute a query on a cursor

    cur     -> a cursor object
    query   -> a query to execute
    params -> a tuple of parameters

    return False if execution error else True
    """
    if cur is None or query is None:
        return False

    try:
        if params is not None:
            if type(params) is not tuple:
                print("parameters must be a tuple")
                return False

            cur.execute(query, params)
        else:
            cur.execute(query)
    except MySQLdb.Error as e:
        try:
            print("MySQL Error [{:d}]: {}".format(e.args[0], e.args[1]))
        except IndexError:
            print("MySQL Error: {}".format(str(e)))
        return False

    return True
