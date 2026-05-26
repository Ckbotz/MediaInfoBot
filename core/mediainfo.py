import asyncio
import json
import shutil
#@cantarellabots
async def extract_mediainfo(url):
    """
    Runs mediainfo or ffprobe on the remote URL to extract metadata.
    """
    # Check if mediainfo is available
    if shutil.which("mediainfo"):
        cmd = ["mediainfo", "--Output=JSON", url]
        return await run_command(cmd)
    
    # Fallback to ffprobe
    if shutil.which("ffprobe"):
        cmd = [
            "ffprobe", 
            "-v", "quiet", 
            "-print_format", "json", 
            "-show_format", 
            "-show_streams", 
            url
        ]
        return await run_command(cmd)
    
    raise Exception("Neither 'mediainfo' nor 'ffprobe' was found on the system.")

async def run_command(cmd):
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        error_msg = stderr.decode().strip() or "Unknown error"
        raise Exception(f"Command error: {error_msg}")
        
    return json.loads(stdout.decode())
