import aiomysql
import random

async def query_with_pool(pool):
    async with await pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(get_sql_query())
            return await cur.fetchall()
