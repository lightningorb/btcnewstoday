import os
import unittest
import requests
import json
import pytest

host = os.environ["bndev_test_url"]

from bn_auth_test_case import *


class TestBounties(BNAuthTestCase):
    def test_login(self, access_token, host):
        assert access_token
