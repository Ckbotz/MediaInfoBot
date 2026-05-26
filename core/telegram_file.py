async def get_file_url(chat_id, message_id):
    """
    Returns a local URL that our background streamer will handle.
    This bypasses the 20MB Bot API limit.
    """
    return f"http://127.0.0.1:8080/stream/{chat_id}/{message_id}"
#@cantarellabots