import os
import asyncio
import aiofiles
import black
import autopep8
from typing import Optional
from src.config.settings import MAX_FORMAT_FILE_SIZE
from src.utils.async_utils import async_lru_cache

@async_lru_cache(maxsize=256)
async def format_code(content: str, file_extension: str) -> str:
    """Format code content based on file extension.
    
    Args:
        content: The code content to format
        file_extension: File extension to determine formatter
        
    Returns:
        Formatted code content
    """
    if not content.strip():
        return content

    try:
        if file_extension in ['.py']:
            return await _format_python(content)
        elif file_extension in ['.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss']:
            return await _format_web(content, file_extension)
        return content
    except Exception:
        return content

async def _format_python(content: str) -> str:
    """Format Python code using black or autopep8.
    
    Args:
        content: Python code to format
        
    Returns:
        Formatted Python code
    """
    try:
        return black.format_str(content, mode=black.FileMode())
    except:
        try:
            return autopep8.fix_code(content)
        except:
            return content

async def _format_web(content: str, file_extension: str) -> Optional[str]:
    """Format web code using prettier.
    
    Args:
        content: Web code to format
        file_extension: File extension for prettier
        
    Returns:
        Formatted web code
    """
    # Skip formatting for large files
    if len(content) > MAX_FORMAT_FILE_SIZE:
        return content
        
    try:
        async with aiofiles.tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp:
            await temp.write(content.encode())
            temp_path = temp.name
        
        # Use --no-config to avoid looking for config files
        # Use --ignore-path to avoid checking .prettierignore
        process = await asyncio.create_subprocess_shell(
            f'npx prettier --no-config --ignore-path /dev/null --write {temp_path}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        
        async with aiofiles.open(temp_path, 'r') as f:
            formatted = await f.read()
        
        await aiofiles.os.remove(temp_path)
        return formatted
    except:
        return content
