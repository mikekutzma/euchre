import json
import logging
import random
from typing import Any, Callable, Optional
from uuid import uuid4

from aiohttp import web
from aiohttp_session import AbstractStorage, Session, new_session

_logger = logging.getLogger(__name__)


class RedisConfig:
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs,
    ):
        self.host = host
        self._port = port
        self.username = username
        self.password = password
        self.kwargs = kwargs

    @property
    def port(self):
        if self._port is not None:
            return int(self._port)
        return None

    def to_dict(self):
        config = {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
        }
        config = {key: value for key, value in config.items() if value is not None}
        return {**config, **self.kwargs}


class RedisStorage(AbstractStorage):
    def __init__(
        self,
        redis,
        *,
        cookie_name: str = "EUCHRE_SESSION",
        sessions_prefix: str = "euchre:sessions",
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
        self.redis = redis
        self.sessions_prefix = sessions_prefix
        with open("names.txt") as f:
            self.names = [name.strip() for name in f.readlines() if name.strip()]
        with open("nouns.json") as f:
            self.nouns = json.load(f)

    def to_key(self, key: str) -> str:
        return f"{self.sessions_prefix}:{key}"

    @property
    def sessions_list_key(self) -> str:
        return self.sessions_prefix

    async def new_session(self) -> Session:

        name = random.choice(self.names).title()
        noun = random.choice(self.nouns[name[0]])
        initial_data = {"username": f"{noun} {name}"}

        session_data = {"session": initial_data}
        added = False
        while not added:
            key = str(uuid4())
            added = bool(await self.redis.sadd(self.sessions_list_key, key))

            if added:
                await self.redis.set(self.to_key(key), json.dumps(session_data))
            else:
                _logger.warning("Session key %s is already in use, trying another", key)
        session = Session(key, data=session_data, new=True, max_age=self.max_age)
        session.changed()
        return session

    async def load_session(self, request: web.Request) -> Session:
        cookie = self.load_cookie(request)
        if cookie is None:
            session = await new_session(request)
        else:
            key = str(cookie)
            data = json.loads(await self.redis.get(self.to_key(key)))
            _logger.info("Found data: %s", data)
            if not data:
                session = await new_session(request)
            else:
                session = Session(key, data=data, new=False, max_age=self.max_age)
        return session

    async def save_session(
        self, request: web.Request, response: web.StreamResponse, session: Session
    ) -> None:
        key = session.identity
        self.save_cookie(response, key, max_age=session.max_age)

        data = self._get_session_data(session)
        _logger.info("saving session data: %s", data)
        await self.redis.set(self.to_key(key), json.dumps(data))
