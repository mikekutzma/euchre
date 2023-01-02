import logging

from aiohttp import web
from aiohttp_session import get_session, new_session
from euchrelib.game import Game, GameJSON

from . import sio

routes = web.RouteTableDef()
_logger = logging.getLogger(__name__)


def json_response(*args, **kwargs):
    return web.json_response(*args, **kwargs, dumps=GameJSON.dumps)


@routes.get("/games")
async def get_games(request):
    live = request.rel_url.query.get("live")
    games = list(request.app["games"].keys())
    if live is not None:
        islive = bool(int(live))
        games = [game for game in games if request.app["games"][game].live == islive]

    return json_response(games)


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
    session = await get_session(request)
    user = session.get("username")

    if user is None:
        raise web.HTTPUnauthorized()

    game = Game()
    request.app["games"][game.game_id] = game

    games = [id for id, game in request.app["games"].items() if not game.live]
    await sio.sio.emit("gamesUpdate", games)
    return json_response({"gameId": game.game_id})


@routes.post("/join")
async def join(request):
    session = await get_session(request)
    user = session.get("username")

    if user is None:
        raise web.HTTPUnauthorized()

    data = await request.json()
    sid = data.get("sid")
    game_id = data.get("gameId")

    if sid is None or game_id is None:
        raise web.HTTPBadRequest()

    game = request.app["games"][game_id]
    game.add_player(user, sid)

    # Add player to room
    sio.sio.enter_room(sid, game_id)

    # lobby = {"players": request.app["games"][game_id].get_players()}

    await sio.sio.emit("lobbyUpdate", game.status, room=game_id)
    return json_response(game.status)


@routes.get("/gameStatus")
async def get_game_status(request):
    game_id = request.rel_url.query.get("gameId")
    game = request.app["games"][game_id]
    data = game.status
    return json_response(data)


@routes.get("/hand")
async def get_hand(request):
    user = request.rel_url.query.get("username")
    if user is None:
        session = await get_session(request)
        user = session.get("username")
    game_id = request.rel_url.query.get("gameId")
    game = request.app["games"][game_id]
    hand = game.get_hand(user)
    _logger.info("Getting hand for %s", user)
    _logger.info(game.players)
    return json_response(hand)


@routes.get("/players")
async def get_players(request):
    game_id = request.rel_url.query.get("gameId")
    game = request.app["games"][game_id]
    return json_response(game.players)


@routes.get("/resetTrick")
async def reset_trick(request):
    game_id = request.rel_url.query.get("gameId")
    game = request.app["games"][game_id]
    game.shuffle()
    await sio.sio.emit("trickUpdate", game.trick)
    return json_response(game.trick)


@routes.get("/reset")
async def reset(request):
    game_id = request.rel_url.query.get("gameId")
    game = request.app["games"][game_id]
    game.start_game()
    return json_response(game.status)
