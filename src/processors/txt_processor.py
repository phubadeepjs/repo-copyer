import os
from typing import List, Tuple
import aiofiles
from tqdm import tqdm
import gc

from src.config.settings import BATCH_SIZE
from src.utils.file_utils import os_path_join, os_path_basename, os_path_abspath, get_file_tree
from src.formatters.code_formatter import format_code

class TXTProcessor:
    def __init__(self, repo_path: str, output_txt: str):
        self.repo_path = repo_path
        self.output_txt = output_txt
        self.repo_name = os_path_basename(os_path_abspath(repo_path))

    async def process(self, files_to_process: List[str]) -> None:
        """Process files and generate TXT.
        
        Args:
            files_to_process: List of files to process
        """
        async with aiofiles.open(self.output_txt, 'w', encoding='utf-8') as f:
            # Write header
            await f.write(f"{self.repo_name}\n\n")
            await f.write("Repository Structure\n")
            await f.write("===================\n\n")
            
            # Add repository structure
            print("Generating repository structure...")
            tree_content = await get_file_tree(self.repo_path)
            await f.write(tree_content)
            await f.write("\n\n")
            
            # Process files in batches
            total_files = len(files_to_process)
            with tqdm(total=total_files, desc="Processing files", unit="file") as pbar:
                for i in range(0, total_files, BATCH_SIZE):
                    batch = files_to_process[i:i + BATCH_SIZE]
                    async for rel_path, content in self._process_batch(batch):
                        await f.write(f"\nFile: {rel_path}\n")
                        await f.write("=" * (len(rel_path) + 6) + "\n\n")
                        await f.write(content)
                        await f.write("\n\n")
                        pbar.update(1)
                    
                    # Force garbage collection after each batch
                    gc.collect()

    async def _process_batch(self, files_batch: List[str]) -> Tuple[str, str]:
        """Process a batch of files.
        
        Args:
            files_batch: List of files to process
            
        Yields:
            Tuple of (relative_path, content) for each file
        """
        for file_path in files_batch:
            try:
                rel_path = os.path.relpath(file_path, self.repo_path)
                
                # Skip node_modules and other large directories
                if 'node_modules' in rel_path or 'dist' in rel_path or 'build' in rel_path:
                    yield rel_path, "[Directory skipped for performance]"
                    continue
                    
                content = await self._read_file_content(file_path)
                yield rel_path, content
            except Exception as e:
                print(f"\nError processing file {file_path}: {str(e)}")
                yield os.path.relpath(file_path, self.repo_path), f"[Error processing file: {str(e)}]"

    async def _read_file_content(self, file_path: str) -> str:
        """Read and format file content.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Formatted file content
        """
        from src.config.settings import MAX_FILE_SIZE, CHUNK_SIZE
        
        try:
            # Skip large files
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                return f"[File too large to process: {file_size / (1024*1024):.1f}MB]"
                
            content = []
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                while True:
                    chunk = await f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    content.append(chunk)
            
            content = ''.join(content)
            content = content.replace('\t', '    ')
            
            # Remove block characters
            block_chars = ['■', '▄', '▌', '█', '▐', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝', '▞', '▟']
            for ch in block_chars:
                content = content.replace(ch, ' ')
            
            # Format code
            file_extension = os.path.splitext(file_path)[1].lower()
            formatted_content = await format_code(content, file_extension)
            return formatted_content
        except UnicodeDecodeError:
            return "[Binary file content]"
        except Exception as e:
            return f"[Error reading file: {str(e)}]"
