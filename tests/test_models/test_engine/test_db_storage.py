#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes

Execution:
     HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd
     HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db
     HBNB_TYPE_STORAGE=db python3 -m unittest discover tests
"""
import unittest
import pep8
import MySQLdb
import models
from models import storage_t as storage_type
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv
from utility import execsafe
from unittest import (skipIf, skipUnless)
from datetime import datetime
import inspect
from models.engine import db_storage
import json
import os


if storage_type == 'db':
    from models.place import place_amenity

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=False)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=False)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class test_DBStorage(unittest.TestCase):
    """
    Define tests for the ``DBStorage`` class
    """
    # Set maxDiff to see all output on error comparison
    maxDiff = None

    def __init__(self, *args, **kwargs):
        """
        Initialiaze the test instance
        """
        super().__init__(*args, **kwargs)
        if storage_type == 'file':
            # print("Iniatialization for database")
            return
        self.value = DBStorage
        self.name = self.value.__name__

        self.db_login = {
                'host':     getenv('HBNB_MYSQL_HOST'),
                'user':     getenv('HBNB_MYSQL_USER'),
                'passwd':   getenv('HBNB_MYSQL_PWD'),
                'db':       getenv('HBNB_MYSQL_DB'),
                'port':     getenv('HBNB_MYSQL_PORT')}

        # Defaults
        if self.db_login['port'] is None:
            self.db_login['port'] = 3306
        else:   # attempt converting to integer
            try:
                val = int(self.db_login['port'])
            except TypeError:
                val = 3306
            self.db_login['port'] = val

        if self.db_login['host'] is None:
            self.db_login['host'] = 'localhost'

        # Connection to database
        for key, val in self.db_login.items():
            if val is None:
                # print("key: {} => value : {}".format(key, val))     # test
                return  # not necessary to proceed

        # Create a connection
        self.db = MySQLdb.connect(**self.db_login)
        # Put a connection to a good use
        self.cur = self.db.cursor()
        # print("cursor created successfully!\n")     # test

        # Attempt truncating table
        query = """SHOW TABLES;"""
        execsafe(self.cur, query)
        tbs = self.cur.fetchall()
        if tbs is None or len(tbs) == 0:
            print("NO TABLES TO TEST\nEXITING")
            exit(1)

        # Disable foreign key checks
        query = """SET FOREIGN_KEY_CHECKS = 0;"""
        execsafe(self.cur, query)

        for tb in tbs:
            query = """TRUNCATE TABLE {};""".format(tb[0])
            execsafe(self.cur, query)

        # Enable foreign key checks
        query = """SET FOREIGN_KEY_CHECKS = 1;"""
        execsafe(self.cur, query)
        # print("All tables successfully cleared")

    def setUp(self):
        """
        Set up the environment for each test methods
        Get current state of database
        """
        # print("storage_type is {}".format(storage_type))    # test
        if storage_type == 'file':
            return

        execsafe(self.cur, """SELECT * FROM states;""")
        self.states = self.cur.fetchall()

        execsafe(self.cur, """SELECT * FROM places;""")
        self.places = self.cur.fetchall()

        execsafe(self.cur, """SELECT * FROM amenities;""")
        self.amenities = self.cur.fetchall()

        execsafe(self.cur, """SELECT * FROM reviews;""")
        self.reviews = self.cur.fetchall()

        execsafe(self.cur, """SELECT * FROM users;""")
        self.users = self.cur.fetchall()

        execsafe(self.cur, """SELECT * FROM cities;""")
        self.cities = self.cur.fetchall()

        execsafe(self.cur, """SELECT * FROM place_amenity;""")
        self.place_amenity = self.cur.fetchall()

        # print("Set up for database done successfully\n")    # test

    def tearDown(self):
        """
        Finishing tasks for a test
        """
        if storage_type == 'file':
            return
        self.db.commit()
        # print("Tear down for database done successfully\n")     # test

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all(self):
        """
        Testing the all method
        """
        state_1 = State(name="Ezra")
        state_1 = state_1.to_dict()
        query = """INSERT INTO states(id, name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}')""".format(
                    state_1['id'], state_1['name'], state_1['updated_at'],
                    state_1['created_at'])
        execsafe(self.cur, query)
        # self.db.commit()
        execsafe(self.cur, """SELECT * FROM states;""")
        states = self.cur.fetchall()
        # print("len(self.states): {}".format(len(self.states)))
        # print("len(states): {}".format(len(states)))
        self.assertTrue(len(states) == len(self.states) + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """
        Ensure the new method is implemented
        """
        # State
        s = State(name="Enugu")
        s_d = s.to_dict()
        query = """INSERT INTO states(id, name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}')""".format(
                    s_d['id'], s_d['name'], s_d['updated_at'],
                    s_d['created_at'])
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM states;""")
        s_objs = self.cur.fetchall()
        self.assertTrue(len(s_objs) == len(self.states) + 1)

        # City
        c = City(name="Abakpa", state_id=s.id)
        c_d = c.to_dict()
        query = """INSERT INTO cities(id, state_id, name, updated_at,
                    created_at)
                    VALUES ('{}', '{}', '{}', '{}', '{}')""".format(
                    c_d['id'], c_d['state_id'], c_d['name'],
                    c_d['updated_at'], c_d['created_at'])
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM cities;""")
        c_objs = self.cur.fetchall()
        self.assertTrue(len(c_objs) == len(self.cities) + 1)

        # User
        u = User(email="ebube@gmail.com", password="ebube123",
                 first_name="Ebube", last_name="Onwuta")
        u_d = u.to_dict()
        query = """INSERT INTO users(id, email, password, first_name,
                    last_name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}',
                    '{}')""".format(
                    u_d['id'], u_d['email'], u_d['password'],
                    u_d['first_name'], u_d['last_name'],
                    u_d['updated_at'], u_d['created_at'])
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM users;""")
        u_objs = self.cur.fetchall()
        self.assertTrue(len(u_objs) == len(self.users) + 1)

        # Amenity
        a = Amenity(name="wifi")
        a_d = a.to_dict()
        query = """INSERT INTO amenities(id, name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}')""".format(
                    a_d['id'], a_d['name'], a_d['updated_at'],
                    a_d['created_at'])
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM amenities;""")
        a_objs = self.cur.fetchall()
        self.assertTrue(len(a_objs) == len(self.amenities) + 1)

        # Place
        p = Place(name="BrainSpark Hub", city_id=c.id, user_id=u.id)
        p_d = p.to_dict()
        query = """INSERT INTO places(id, city_id, user_id, name,
                    updated_at, created_at, number_rooms, number_bathrooms,
                    max_guest, price_by_night)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', 0,
                    0, 0, 0)""".format(
                    p_d['id'], p_d['city_id'], p_d['user_id'], p_d['name'],
                    p_d['updated_at'], p_d['created_at'])
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM places;""")
        p_objs = self.cur.fetchall()
        self.assertTrue(len(p_objs) == len(self.places) + 1)

        # place_amenity -> An association table for the Many-to-Many
        # Relationship between Place and Amenity models
        query = """INSERT INTO place_amenity(amenity_id, place_id)
                    VALUES ('{}', '{}')""".format(a.id, p.id)
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM place_amenity;""")
        place_amenity_objs = self.cur.fetchall()
        self.assertTrue(len(place_amenity_objs) == len(self.place_amenity) + 1)

        # Review
        r = Review(text="The world of my fantasy", user_id=u.id, place_id=p.id)
        r_d = r.to_dict()
        query = """INSERT INTO reviews(id, user_id, place_id, text, updated_at,
                    created_at)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(
                    r_d['id'], r_d['user_id'], r_d['place_id'],
                    r_d['text'], r_d['updated_at'], r_d['created_at'])
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM reviews;""")
        r_objs = self.cur.fetchall()
        self.assertTrue(len(r_objs) == len(self.reviews) + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """
        Ensure that the save method saves changes made in a session
        """
        # State
        prev_name = "Anambra"
        s = State(name=prev_name)
        s_d = s.to_dict()
        query = """INSERT INTO states(id, name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}')""".format(
                    s_d['id'], s_d['name'], s_d['updated_at'],
                    s_d['created_at'])
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM states;""")
        s_objs = self.cur.fetchall()
        self.assertTrue(len(s_objs) == len(self.states) + 1)

        # Make changes to State
        new_name = "Abuja"
        query = """UPDATE states
                    SET states.name = '{}'
                    WHERE states.id = '{}'""".format(new_name, s.id)
        execsafe(self.cur, query)

        # Confirm reflection of changes made
        query = """SELECT name
                    FROM states
                    WHERE states.id = '{}'""".format(s.id)
        execsafe(self.cur, query)

        s_obj = self.cur.fetchone()
        if s_obj is None or len(s_obj) == 0:
            print("Could not get state object\nEXITING")
            exit(1)

        self.assertEqual(new_name, s_obj[0])

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """
        Ensure that that an item can be deleted from the database
        """
        # State
        prev_name = "Bayelsa"
        s = State(name=prev_name)
        s_d = s.to_dict()
        query = """INSERT INTO states(id, name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}')""".format(
                    s_d['id'], s_d['name'], s_d['updated_at'],
                    s_d['created_at'])
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM states;""")
        s_objs = self.cur.fetchall()
        self.assertTrue(len(s_objs) == len(self.states) + 1)

        # Delete this object
        query = """DELETE FROM states
                    WHERE states.id = '{}'""".format(s.id)
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT states.id FROM states;""")
        s_objs = self.cur.fetchall()

        item = (str(s.id),)
        self.assertNotIn(item, s_objs)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Ensure we can retrieve an object from database by id and class"""
        # State
        s = State(name="Enugu")
        s_d = s.to_dict()
        query = """INSERT INTO states(id, name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}')""".format(
                    s_d['id'], s_d['name'], s_d['updated_at'],
                    s_d['created_at'])
        execsafe(self.cur, query)
        # Retrieve
        query = """SELECT * FROM states
                    WHERE id = '{}';""".format(s_d['id'])
        execsafe(self.cur, query)
        s_objs = self.cur.fetchall()
        self.assertEqual(len(s_objs), 1)

        # City
        c = City(name="Abakpa", state_id=s.id)
        c_d = c.to_dict()
        query = """INSERT INTO cities(id, state_id, name, updated_at,
                    created_at)
                    VALUES ('{}', '{}', '{}', '{}', '{}')""".format(
                    c_d['id'], c_d['state_id'], c_d['name'],
                    c_d['updated_at'], c_d['created_at'])
        execsafe(self.cur, query)
        # Retrieve
        query = """SELECT * FROM cities
                    WHERE id = '{}';""".format(c_d['id'])
        execsafe(self.cur, query)
        c_objs = self.cur.fetchall()
        self.assertEqual(len(c_objs), 1)

        # User
        u = User(email="ebube@gmail.com", password="ebube123",
                 first_name="Ebube", last_name="Onwuta")
        u_d = u.to_dict()
        query = """INSERT INTO users(id, email, password, first_name,
                    last_name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}',
                    '{}')""".format(
                    u_d['id'], u_d['email'], u_d['password'],
                    u_d['first_name'], u_d['last_name'],
                    u_d['updated_at'], u_d['created_at'])
        execsafe(self.cur, query)
        # Retrieve
        query = """SELECT * FROM users
                    WHERE id = '{}';""".format(u_d['id'])
        execsafe(self.cur, query)
        u_objs = self.cur.fetchall()
        self.assertEqual(len(u_objs), 1)

        # Amenity
        a = Amenity(name="wifi")
        a_d = a.to_dict()
        query = """INSERT INTO amenities(id, name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}')""".format(
                    a_d['id'], a_d['name'], a_d['updated_at'],
                    a_d['created_at'])
        execsafe(self.cur, query)
        # Retrieve
        query = """SELECT * FROM amenities
                    WHERE id = '{}';""".format(a_d['id'])
        execsafe(self.cur, query)
        a_objs = self.cur.fetchall()
        self.assertEqual(len(a_objs), 1)

        # Place
        p = Place(name="BrainSpark Hub", city_id=c.id, user_id=u.id)
        p_d = p.to_dict()
        query = """INSERT INTO places(id, city_id, user_id, name,
                    updated_at, created_at, number_rooms, number_bathrooms,
                    max_guest, price_by_night)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', 0,
                    0, 0, 0)""".format(
                    p_d['id'], p_d['city_id'], p_d['user_id'], p_d['name'],
                    p_d['updated_at'], p_d['created_at'])
        execsafe(self.cur, query)
        # Retrieve
        query = """SELECT * FROM places
                    WHERE id = '{}';""".format(p_d['id'])
        execsafe(self.cur, query)
        p_objs = self.cur.fetchall()
        self.assertEqual(len(p_objs), 1)

        # place_amenity -> An association table for the Many-to-Many
        # Relationship between Place and Amenity models
        query = """INSERT INTO place_amenity(amenity_id, place_id)
                    VALUES ('{}', '{}')""".format(a.id, p.id)
        execsafe(self.cur, query)
        execsafe(self.cur, """SELECT * FROM place_amenity;""")
        place_amenity_objs = self.cur.fetchall()
        self.assertTrue(len(place_amenity_objs) == len(self.place_amenity) + 1)

        # Review
        r = Review(text="The world of my fantasy", user_id=u.id, place_id=p.id)
        r_d = r.to_dict()
        query = """INSERT INTO reviews(id, user_id, place_id, text, updated_at,
                    created_at)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(
                    r_d['id'], r_d['user_id'], r_d['place_id'],
                    r_d['text'], r_d['updated_at'], r_d['created_at'])
        execsafe(self.cur, query)
        # Retrieve
        query = """SELECT * FROM reviews
                    WHERE id = '{}';""".format(r_d['id'])
        execsafe(self.cur, query)
        r_objs = self.cur.fetchall()
        self.assertEqual(len(r_objs), 1)

    '''
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Ensure we can retrieve an object from database by id and class"""
        for cls in classes.values():
            with self.subTest(cls=cls):
                print("\nTesting table {}\n".format(cls.__tablename__))
                obj = cls(name="Adamawa")
                obj = obj.to_dict()
                query = """INSERT INTO {}(id, name, updated_at, created_at)
                            VALUES ('{}', '{}', '{}', '{}')""".format(
                            cls.__tablename__,
                            obj['id'], obj['name'], obj['updated_at'],
                            obj['created_at'])
                execsafe(self.cur, query)

                # Test we could get that particular object
                query = """SELECT * FROM {}
                            WHERE id = '{}';""".format(cls.__tablename__,
                                                       obj['id'])
                execsafe(self.cur, query)
                items = self.cur.fetchall()
                self.assertEqual(len(items), 1)
    '''

    '''
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all(self):
        """
        Testing the all method
        """
        state_1 = State(name="Ezra")
        state_1 = state_1.to_dict()
        query = """INSERT INTO states(id, name, updated_at, created_at)
                    VALUES ('{}', '{}', '{}', '{}')""".format(
                    state_1['id'], state_1['name'], state_1['updated_at'],
                    state_1['created_at'])
        execsafe(self.cur, query)
        # self.db.commit()
        execsafe(self.cur, """SELECT * FROM states;""")
        states = self.cur.fetchall()
        # print("len(self.states): {}".format(len(self.states)))
        # print("len(states): {}".format(len(states)))
        self.assertTrue(len(states) == len(self.states) + 1)


    '''

    '''
    @skipIf(storage_type == 'file', "This test is for database storage")
    def test_close(self):
        """
        Ensure that the close method of DBStorage is implemented
        """
        errno = 2006    # number for this MySQLdb error
        cursor = self.db.cursor()
        # cursor.execute.side_effect = MySQLdb.OperationalError(errno, '')
        self.db.close()
        query = """SELECT * from states;"""

        with self.assertRaises(MySQLdb.OperationalError) as context:
            cursor.execute(query)

        self.assertEqual(context.exception.args[0], errno)
    '''
