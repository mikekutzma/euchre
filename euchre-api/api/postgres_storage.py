import json
import logging
from typing import Any, Callable, Optional

from aiohttp import web
from aiohttp_session import AbstractStorage, Session

_logger = logging.getLogger(__name__)


class PostgresStorage(AbstractStorage):
    def __init__(
        self,
        pg_pool,
        *,
        cookie_name: str = "AIOHTTP_SESSION",
        domain: Optional[str] = None,
        max_age: Optional[int] = None,
        path: str = "/",
        secure: Optional[bool] = None,
        httponly: bool = True,
        samesite: Optional[str] = None,
        encoder: Callable[[object], str] = json.dumps,
        decoder: Callable[[str], Any] = json.loads,
    ) -> None:
        super().__init__(
            cookie_name=cookie_name,
            domain=domain,
            max_age=max_age,
            path=path,
            secure=secure,
            httponly=httponly,
            samesite=samesite,
            encoder=encoder,
            decoder=decoder,
        )
        self.pool = pg_pool

    async def load_session(self, request: web.Request) -> Session:
        cookie = self.load_cookie(request)
        if cookie is None:
            return Session(None, data=None, new=True, max_age=self.max_age)
        else:
            key = str(cookie)
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""SELECT * from users where id=$1""", key)
                _logger.info(row)

            if row is None:
                return Session(None, data=None, new=True, max_age=self.max_age)
            data = row["data"]
            data["id"] = row["id"]
            return Session(key, data=data, new=False, max_age=self.max_age)

    async def save_session(
        self, request: web.Request, response: web.StreamResponse, session: Session
    ) -> None:
        key = session.identity
        if key is None:
            key = self._key_factory()
            self.save_cookie(response, key, max_age=session.max_age)
        else:
            if session.empty:
                self.save_cookie(response, "", max_age=session.max_age)
            else:
                key = str(key)
                self.save_cookie(response, key, max_age=session.max_age)

        data_str = self._encoder(self._get_session_data(session))
        await self._redis.set(
            self.cookie_name + "_" + key,
            data_str,
            ex=session.max_age,
        )
