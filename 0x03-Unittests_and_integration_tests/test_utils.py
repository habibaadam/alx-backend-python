#!/usr/bin/env python3
"""Tests for utils"""


import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, MagicMock


class TestAccessNestedMap(unittest.TestCase):
    """class for testing the acess map function
    inheriting from unittest.TestCase
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """method for testing the access map function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """tests for incorrect inputs error"""
        self.assertRaises(KeyError)


class TestGetJson(unittest.TestCase):
    """class for testing the get_json function"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_requests):
        """Method for testing the get_json function"""
        response = MagicMock()
        response.json.return_value = test_payload
        mock_requests.return_value = response
        self.assertEqual(get_json(test_url), test_payload)


class TestMemoize(unittest.TestCase):
    """class for testing the memoize function"""
    def test_memoize(self):
        """method for testing memoize"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        instance = TestClass()
        with patch.object(instance, "a_method") as mocked_a_method:
            mocked_a_method.return_value = 42

            first_result = instance.a_property
            second_result = instance.a_property

            mocked_a_method.assert_called_once()
            self.assertEqual(first_result, 42)
            self.assertEqual(second_result, 42)
