import logging
import aiohttp
from .adapter import RestAdapter
from .models.issue import RootObject


class SeeClickFixClient:
    """Client for interacting with the SeeClickFix API"""

    def __init__(
        self, logger: logging.Logger = None
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self._session = None
        self.adapter = RestAdapter(hostname="seeclickfix.com", base="api/v2")

    @property
    def session(self):
        if not self._session:
            self._session = aiohttp.ClientSession()
        return self._session

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        self.adapter.session = self.session
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if not self.session:
            return

        await self.session.close()
        self.session = None

    async def get_issues(
        self,
        min_lat: float,
        min_lng: float,
        max_lat: float,
        max_lng: float,
        status: str,
        fields: str,
        page: int,
    ) -> RootObject:
        """Get a list of issues"""
        params = {
            "min_lat": min_lat,
            "min_lng": min_lng,
            "max_lat": max_lat,
            "max_lng": max_lng,
            "status": status,
            "fields[issue]": fields,
            "page": page,
        }

        result = await self.adapter.get(self.session, "issues", ep_params=params)
        return RootObject.from_dict(result.data)
