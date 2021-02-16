from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup():
    import aiomysql
    import secret
    app.state.pool = await aiomysql.create_pool(host=secret.DB_URL, port=3306, user=secret.DB_USERNAME, password=secret.DB_PASSWORD, db=secret.DB_DATABASE)
    print("statup done")
