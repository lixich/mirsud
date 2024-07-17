import logging
import re
from typing import Any, Dict, Iterator

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from tenacity import (
    after_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)

from settings import settings

logger = logging.getLogger(__name__)


class SearchParams(BaseModel):
    page: int
    sprs: str
    onlytext: int = 0
    mss: int = 1
    sprsType: str = 'jp'
    numberingyear: int
    spt: str = 'CS'
    s: int = 0
    uid: str = 'NO'


class DetailParams(BaseModel):
    guid: str


class Parser:
    _base_url = 'https://ms1.mirsud24.ru/ms/sudoproizvodstvo/informatsiya-po-sudebnym-delam/'
    _search_method = 'search.php'
    _detail_method = 'detail_page.php?guid={}'
    _page_size = 20

    def __init__(self) -> None:
        self._session = requests.Session()
        self._base_params: Dict[str, Any] = {}

    def _auth(self) -> None:
        r = self._session.get(self._base_url)
        r.raise_for_status()

        if not (set_cookie := r.headers.get('Set-Cookie')):
            raise ValueError('Not found Set-Cookie in response headers')
        if not (php_sessid := re.findall('PHPSESSID=\w*', set_cookie)) or not php_sessid[0]:
            raise ValueError('Not found php_sessid in response')
        if not (bitrix_sessid := re.search("'bitrix_sessid':'(\w*)'}", r.text)):
            raise ValueError('Not found bitrix_sessid in response')
        if not (session_id := re.search('\'sessionid\': "(\w*)",', r.text)):
            raise ValueError('Not found sessionid in response')

        self._session.headers['Cookie'] = php_sessid[0]
        self._session.headers['X-Requested-With'] = 'XMLHttpRequest'

        self._base_params['sessid'] = bitrix_sessid.group(1)
        self._base_params['sessionid'] = session_id.group(1)

    @retry(
        reraise=True,
        after=after_log(logger, logging.INFO),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        stop=stop_after_attempt(5),
    )
    def _post(self, method: str, params: Dict) -> str:
        params = dict(self._base_params, **params)
        logger.info(f'Request with method {method}')
        r = self._session.post(self._base_url + method, data=params)
        r.raise_for_status()
        assert r.text is not None
        return r.text

    def _fetch_search_pages(self) -> Iterator[str]:
        search_params = SearchParams(page=1, sprs=settings.company, numberingyear=settings.year)
        while True:
            search_text = self._post(self._search_method, params=search_params.dict())
            soup = BeautifulSoup(search_text, features='lxml')
            guid_tags = soup.find_all('a', {'class': 'fast_look_btn'})
            logger.info(f'Found {len(guid_tags)} guids')
            for guid_tag in guid_tags:
                fast_look = re.search('javascript:fast_look\("(.*)"\);', guid_tag['href'])
                if not fast_look:
                    raise ValueError('Not found fast_look with guid in response')
                guid = fast_look.group(1)
                yield self._fetch_detail_page(guid)

            if len(guid_tags) < self._page_size:
                break
            search_params.page += 1

    def _fetch_detail_page(self, guid: str) -> str:
        guid_params = DetailParams(guid=guid)
        detail_text = self._post(self._detail_method.format(guid), params=guid_params.dict())
        return detail_text

    def run(self) -> Iterator[str]:
        self._auth()
        yield from self._fetch_search_pages()
