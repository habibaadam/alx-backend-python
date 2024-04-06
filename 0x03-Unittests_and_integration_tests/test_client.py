#!/usr/bin/env python3
"""Tests for client"""


import unittest
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock


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

    def test_public_repos_url(self):
        """Test that the result of _public_repos_url
        is the expected one
        """
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            org_name = "google"
            url = f"https://www.{org_name}.com"
            mock_org.return_value = {"repos_url": url}
            client = GithubOrgClient(org_name)
            self.assertEqual(client._public_repos_url, url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test the public repo method
        """
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_repo_url:
            mock_get_json.return_value = [{"name": "name1"}, {"name": "name2"}]
            mock_repo_url.return_value = "https://www.google.com"
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["name1", "name2"])
            mock_repo_url.assert_called_once()
            mock_get_json.assert_called_once()
