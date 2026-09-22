import asyncio
import json
import os

from openai import AsyncOpenAI
from pydantic import BaseModel
from stagehand import LLMStructuredGenerateResult, Stagehand, local_browser


class Story(BaseModel):
    title: str
    points: int


class Stories(BaseModel):
    stories: list[Story]


openai = AsyncOpenAI(
    api_key="sk-or-v1-...",
    base_url="https://openrouter.ai/api/v1",
)


def content_part(block):
    # Each block is a LLMTextContent or LLMImageContent under `.root`. The
    # Responses API takes input parts, so map text to an input text part and
    # images (which `extract(screenshot=True)` sends) to an input image data URL.
    if block.root.type == "text":
        return {"type": "input_text", "text": block.root.text}
    return {
        "type": "input_image",
        "image_url": f"data:{block.root.mime_type};base64,{block.root.data}",
        "detail": "auto",
    }


def message_content(message):
    # A message's content is one block or a list of them.
    content = message.content
    blocks = content if isinstance(content, list) else [content]
    return [content_part(block) for block in blocks]


async def generate_with_openai(params):
    response_format = params.response_format
    response = await openai.responses.create(
        model="~deepseek/deepseek-flash-latest",
        instructions=params.system_prompt,
        input=[
            {"role": message.role.value, "content": message_content(message)}
            for message in params.messages
        ],
        temperature=params.temperature,
        text={
            "format": {
                "type": "json_schema",
                "name": response_format.name,
                "schema": response_format.schema_.model_dump(),
                "strict": True,
            }
        },
    )

    return LLMStructuredGenerateResult.model_validate(
        {
            "role": "assistant",
            "content": {"type": "text", "text": response.output_text},
            "output_format": "json_schema",
            "structured_content": json.loads(response.output_text),
        }
    )


async def main() -> None:
    browser = await local_browser.launch()
    sh = await Stagehand.create(browser=browser, model=generate_with_openai)

    page = await browser.context.active_page()
    if page is None:
        raise RuntimeError("Stagehand initialized without an active page")

    await page.goto("https://news.ycombinator.com")

    result = await sh.extract(
        "Extract the top 5 stories",
        Stories,
    )

    print(result.data.stories)

    await sh.close()
    await browser.close()


asyncio.run(main())
