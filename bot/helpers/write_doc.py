import aiofiles


async def write_doc(file_name: str, doc_content: str) -> None:
    async with aiofiles.open(file_name, mode="w", encoding="utf-8") as doc:
        document = await doc.write(doc_content)

        return document
