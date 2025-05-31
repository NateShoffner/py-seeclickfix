from seeclickfix.client import SeeClickFixClient
from seeclickfix.models.issue import Status
import unittest

class IssuesTest(unittest.IsolatedAsyncioTestCase):
    async def test_fetch(self):

        params = {
            "min_lat": 40.02961244400919,
            "min_lng": -76.333590881195,
            "max_lat": 40.04702644421361,
            "max_lng": -76.26908911880496,
            "status": [Status.OPEN],
            "page": 1,
        }

        client = SeeClickFixClient()
        issues = await client.get_issues(**params)

        self.assertIsNotNone(issues)
        self.assertGreater(len(issues.issues), 0)

        for issue in issues.issues:
            self.assertIsNotNone(issue.description)

if __name__ == "__main__":
    unittest.main()