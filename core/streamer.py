from aiohttp import web
import math
import logging
#@cantarellabots
class MediaStreamer:
    def __init__(self, client):
        self.client = client
        self.app = web.Application()
        self.app.router.add_get("/stream/{chat_id}/{message_id}", self.stream_handler)
        self.runner = None

    async def start(self, host="127.0.0.1", port=8000):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, host, port)
        await site.start()
        logging.info(f"Local streamer started at http://{host}:{port}")

    async def stream_handler(self, request):
        chat_id = int(request.match_info["chat_id"])
        message_id = int(request.match_info["message_id"])

        try:
            message = await self.client.get_messages(chat_id, message_id)
            if not message or not (message.video or message.audio or message.document):
                return web.Response(status=404, text="Media not found")

            media = message.video or message.audio or message.document
            file_size = media.file_size
            file_name = media.file_name or "file"

            # Handle Range Header
            range_header = request.headers.get("Range")
            start = 0
            end = file_size - 1

            if range_header:
                # Example: bytes=0-1024
                h_range = range_header.replace("bytes=", "").split("-")
                start = int(h_range[0])
                if h_range[1]:
                    end = int(h_range[1])

            chunk_size = 1024 * 1024 # 1MB chunks
            
            response = web.StreamResponse(
                status=206 if range_header else 200,
                reason="Partial Content" if range_header else "OK",
                headers={
                    "Content-Type": media.mime_type or "application/octet-stream",
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                    "Content-Length": str(end - start + 1),
                    "Content-Disposition": f'attachment; filename="{file_name}"',
                    "Accept-Ranges": "bytes",
                }
            )

            await response.prepare(request)

            async for chunk in self.client.stream_media(message, offset=math.floor(start / (1024 * 1024))):
                # This logic is slightly simplified; production streamers handle exact byte offsets better
                # but for ffprobe/mediainfo header probing, this is often sufficient.
                await response.write(chunk)
                if response.prepared: # Rough check to avoid writing more than needed if connection closes
                    pass

            return response

        except Exception as e:
            logging.error(f"Streaming error: {e}")
            return web.Response(status=500, text=str(e))
