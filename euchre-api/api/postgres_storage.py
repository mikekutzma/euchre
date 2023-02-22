import json
import logging
import random
from typing import Any, Callable, Optional

from aiohttp import web
from aiohttp_session import AbstractStorage, Session, new_session

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
        with open("names.txt") as f:
            self.names = [name.strip() for name in f.readlines() if name.strip()]
        with open("nouns.json") as f:
            self.nouns = json.load(f)

    async def new_session(self) -> Session:
        name = random.choice(self.names).title()
        noun = random.choice(self.nouns[name[0]])
        data = {"username": f"{noun} {name}"}
        session_data = {"session": data}
        insert = """
            INSERT INTO users
            (data)
            VALUES(
            $1
            )
            RETURNING ID;
        """
        async with self.pool.acquire() as conn:
            key = await conn.fetchval(insert, json.dumps(session_data))
        session = Session(key, data=session_data, new=True, max_age=self.max_age)
        session.changed()
        return session

    async def load_session(self, request: web.Request) -> Session:
        cookie = self.load_cookie(request)
        if cookie is None:
            session = await new_session(request)
        else:
            key = str(cookie)
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("""SELECT * from users where id=$1""", key)

            if row is None:
                session = await new_session(request)

            data = json.loads(row["data"])
            _logger.info(data)
            session = Session(key, data=data, new=False, max_age=self.max_age)
        return session

    async def save_session(
        self, request: web.Request, response: web.StreamResponse, session: Session
    ) -> None:
        key = session.identity
        self.save_cookie(response, key, max_age=session.max_age)

        data = self._get_session_data(session)
        update = """
            UPDATE
                users
            SET
                data=$1
            WHERE
                id=$2
        """
        async with self.pool.acquire() as conn:
            await conn.execute(update, json.dumps(data), key)
