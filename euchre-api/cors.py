import aiohttp_cors

def setup_cors(app):
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )

    for route in list(app.router.routes()):
        if route._resource.raw_match("/socket.io/"):
            continue
        cors.add(route)
