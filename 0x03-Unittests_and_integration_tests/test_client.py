#!/usr/bin/env python3
"""Test for Client
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """This class contains tests for the
    GithubOrgClient class
    """
    @parameterized.expand([("google"), ("abc")])
    @patch("client.get_json")
    def test_org(self, test_org_name, mock_get_json):
        """Test that GithubOrgClient.org returns
        the correct value
        """
        mock_get_json.return_value = {"test_key": test_org_name}
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, test_map, test_license, expected_output):
        """Test the has_licensce method"""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(test_map,
                                            test_license), expected_output)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Class for Integration test of fixtures """

    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """ Integration test: public repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """ Integration test for public repos with License """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""
        cls.get_patcher.stop()
