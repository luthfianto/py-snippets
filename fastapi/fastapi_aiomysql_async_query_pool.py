from fastapi import FastAPI
import aiomysql
import secret

app = FastAPI()

@app.on_event("startup")
async def _startup():
    app.state.pool = await aiomysql.create_pool(host=secret.DB_URL, port=3306, user=secret.DB_USERNAME, password=secret.DB_PASSWORD, db=secret.DB_DATABASE)
    print("startup done")

async def _get_query_with_pool(pool):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT 1")
            return await cur.fetchall()

@app.get("/v1/get_data")
async def _get_data():
    return await _get_query_with_pool(app.state.pool)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
