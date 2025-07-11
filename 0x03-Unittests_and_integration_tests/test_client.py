#!/usr/bin/env python3
""" Parameterize and patch as decorators, Mocking a property, More patching,
    Parameterize, Integration test: fixtures, Integration tests """
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
# from requests import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """ TESTCASE """
    """ inputs to test the functionality """
    @parameterized.expand([
        ("google"),
        ("abc"),
        ])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name, mock_get):
        """ test that GithubOrgClient.org returns the correct value """
        test_client = GithubOrgClient(org_name)
        test_return = test_client.org
        self.assertEqual(test_return, mock_get.return_value)
        mock_get.assert_called_once

    def test_public_repos_url(self):
        """ to unit-test GithubOrgClient._public_repos_url """
        with patch.object(GithubOrgClient,
                          "org",
                          new_callable=PropertyMock,
                          return_value={"repos_url": "holberton"}) as mock_get:
            test_json = {"repos_url": "holberton"}
            test_client = GithubOrgClient(test_json.get("repos_url"))
            test_return = test_client._public_repos_url
            mock_get.assert_called_once
            self.assertEqual(test_return,
                             mock_get.return_value.get("repos_url"))

    @patch("client.get_json", return_value=[{"name": "holberton"}])
    def test_public_repos(self, mock_get):
        """
        Use @patch as a decorator to mock get_json and make
        it return a payload of your choice.
        Use patch as a context manager to mock GithubOrgClient.
        _public_repos_url and return a value of your choice.
        Test that the list of repos is what you expect from the chosen payload.
        Test that the mocked property and the mocked get_json was called once.
        """
        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock,
                          return_value="https://api.github.com/") as mock_pub:
            test_client = GithubOrgClient("hoberton")
            test_return = test_client.public_repos()
            self.assertEqual(test_return, ["holberton"])
            mock_get.assert_called_once
            mock_pub.assert_called_once

    """ inputs to test the functionality """
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ])
    def test_has_license(self, repo, license_key, expected_return):
        """ to unit-test GithubOrgClient.has_license """
        test_client = GithubOrgClient("holberton")
        test_return = test_client.has_license(repo, license_key)
        self.assertEqual(expected_return, test_return)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
    )
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    TESTCASE
    The repos_payload carries the Response object with it:
    """
    @classmethod
    def setUpClass(cls):
        """
        It is part of the unittest.TestCase API
        method to return example payloads found in the fixtures
        """
        cls.get_patcher = patch('utils.get_json')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.startswith("https://api.github.com/orgs/"):
                return cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return {}

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """ It is part of the unittest.TestCase API
        method to stop the patcher """
        cls.get_patcher.stop()

    # def test_public_repos(self):
    #     """ method to test GithubOrgClient.public_repos """
    #     test_class = GithubOrgClient("google")
    #     repos = test_class.public_repos()
    #     self.assertEqual(sorted(repos), sorted(self.expected_repos))

    # def test_public_repos_with_license(self):
    #     """ method to test the public_repos with the argument license """
    #     test_class = GithubOrgClient("google")
    #     apache_repos = test_class.public_repos(license="apache-2.0")
    #     self.assertEqual(apache_repos, self.apache2_repos)
