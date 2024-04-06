#!/usr/bin/env python3
"""Tests for client"""


import unittest
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch


class TestGithubOrgClient(unittest.TestCase):
    """class containing tests for github org client"""
    @parameterized.expand([("google"), ("abc")])
    @patch("client.get_json")
    def test_org(self, test_org_name, mock_get_json):
        """tests whether githuborg client returns correct
        output"""
        mock_get_json.return_value = {"test_key": "test_org_name"}
        client = GithubOrgClient(test_org_name)

        self.assertEqual(client.org, {"test_key": test_org_name})
