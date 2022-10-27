from app_factory import create_app

app = create_app()


@app.on_event('shutdown')
async def shutdown():
    print('Shutting down...')
    await app.state.db.close()
