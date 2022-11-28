import logging

from aiohttp import web
from aiohttp_session import get_session, new_session

from euchre import sio
from game import Game, GameJSON

routes = web.RouteTableDef()
_logger = logging.getLogger(__name__)


def json_response(*args, **kwargs):
    return web.json_response(*args, **kwargs, dumps=GameJSON.dumps)


@routes.get("/")
async def root(request):
    return web.FileResponse("./dist/index.html")

@routes.get("/games")
async def get_games(request):
    return json_response(list(request.app["games"].keys()))

@routes.get("/getSession")
async def get_sess(request):
    session = await get_session(request)
    data = {"logged_in": False}
    _logger.info(session)
    if session.get("username") is not None:
        data["logged_in"] = True
        data["username"] = session["username"]
    return json_response(data)


@routes.post("/login")
async def login(request):
    data = await request.json()
    user = data["username"]
    session = await new_session(request)
    session.set_new_identity(user)
    session["username"] = user
    _logger.info(session)
    return json_response({"logged_in": True})


@routes.post("/logout")
async def logout(request):
    session = await get_session(request)
    session.invalidate()
    data = {"logged_in": False}
    return json_response(data)


@routes.post("/newGame")
async def newGame(request):
    # session = await get_session(request)
    # user = session.get("username")

    # if user is None:
    #     raise web.HTTPUnauthorized()

    game = Game()
    request.app["games"][game.game_id] = game

    # player = request.app["game"].add_player(user, sid)
    # lobby = {"players": request.app["game"].get_players()}

    # await sio.emit("lobbyUpdate", lobby)
    return json_response(game.status)

@routes.post("/join")
async def join(request):
    session = await get_session(request)
    user = session.get("username")

    if user is None:
        raise web.HTTPUnauthorized()

    data = await request.json()
    sid = data.get("sid")

    if sid is None:
        raise web.HTTPBadRequest()
    request.app.logger.error(sid)

    player = request.app["game"].add_player(user, sid)
    lobby = {"players": request.app["game"].get_players()}

    await sio.emit("lobbyUpdate", lobby)
    return json_response(player)


@routes.get("/gameStatus")
async def get_game_status(request):
    data = request.app["game"].status
    return json_response(data)


@routes.get("/hand")
async def get_hand(request):
    user = request.rel_url.query.get("username")
    if user is None:
        session = await get_session(request)
        user = session.get("username")
    hand = request.app["game"].get_hand(user)
    return json_response(hand)


@routes.get("/players")
async def get_players(request):
    return json_response(request.app["game"].players)


@routes.get("/resetTrick")
async def reset_trick(request):
    request.app["game"].shuffle()
    await sio.emit("trickUpdate", request.app["game"].trick)
    return json_response(request.app["game"].trick)


@routes.get("/reset")
async def reset(request):
    request.app["game"].start_game()
    return json_response(request.app["game"].status)
