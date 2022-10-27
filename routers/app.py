def add_app_routes(router):
    @router.get("/")
    async def root():
        return {"message": "Hello World"}

    @router.get("/hello/{name}")
    async def say_hello(name: str):
        return {"message": f"Hello {name}"}
