def add_app_routes(router):
    @router.get("/ping")
    async def ping():
        return {"ping": "pong!"}


