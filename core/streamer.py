from aiohttp import web
import math
import logging
from asyncio import CancelledError
# @cantarellabots

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
            file_name = getattr(media, "file_name", None) or "file"
            mime_type = getattr(media, "mime_type", None) or "application/octet-stream"

            # Parse Range header
            range_header = request.headers.get("Range")
            start = 0
            end = file_size - 1

            if range_header:
                try:
                    h_range = range_header.replace("bytes=", "").split("-")
                    start = int(h_range[0]) if h_range[0] else 0
                    end = int(h_range[1]) if h_range[1] else file_size - 1
                except Exception:
                    return web.Response(status=416, text="Invalid Range header")

            # Clamp values
            start = max(0, min(start, file_size - 1))
            end = max(start, min(end, file_size - 1))
            content_length = end - start + 1

            chunk_size = 1024 * 1024  # 1MB
            offset = math.floor(start / chunk_size)
            first_chunk_skip = start - (offset * chunk_size)

            response = web.StreamResponse(
                status=206 if range_header else 200,
                reason="Partial Content" if range_header else "OK",
                headers={
                    "Content-Type": mime_type,
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                    "Content-Length": str(content_length),
                    "Content-Disposition": f'inline; filename="{file_name}"',
                    "Accept-Ranges": "bytes",
                }
            )

            await response.prepare(request)

            bytes_sent = 0
            skip = first_chunk_skip

            async for chunk in self.client.stream_media(message, offset=offset):
                if request.transport is None or request.transport.is_closing():
                    logging.info("Client disconnected, stopping stream")
                    break

                # Skip bytes at the start to align with exact byte range
                if skip > 0:
                    chunk = chunk[skip:]
                    skip = 0

                # Trim last chunk to not exceed requested range
                remaining = content_length - bytes_sent
                if len(chunk) > remaining:
                    chunk = chunk[:remaining]

                if not chunk:
                    break

                try:
                    await response.write(chunk)
                    bytes_sent += len(chunk)
                except (ConnectionResetError, CancelledError, Exception) as write_err:
                    logging.info(f"Write stopped (client likely disconnected): {write_err}")
                    break

                if bytes_sent >= content_length:
                    break

            try:
                await response.write_eof()
            except Exception:
                pass

            return response

        except CancelledError:
            logging.info("Stream request cancelled by client")
            raise
        except Exception as e:
            logging.error(f"Streaming error: {e}")
            try:
                return web.Response(status=500, text=str(e))
            except Exception:
                pass
