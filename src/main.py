import os
import sys
import asyncio
import time
from src.config.settings import OUTPUT_DIR
from src.utils.file_utils import os_path_join, os_path_basename, os_path_abspath, os_path_exists, os_makedirs, get_file_tree, get_files_to_process
from src.processors.pdf_processor import PDFProcessor
from src.processors.txt_processor import TXTProcessor

async def main():
    if len(sys.argv) != 2:
        print("Usage: python -m src.main <repository_path>")
        sys.exit(1)

    repo_path = sys.argv[1]

    if not await os_path_exists(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist")
        sys.exit(1)

    start_time = time.time()

    # Create output directory if it doesn't exist
    await os_makedirs(OUTPUT_DIR, exist_ok=True)

    # Get repository name and setup output paths
    repo_name = os_path_basename(os_path_abspath(repo_path))
    pdf_path = os_path_join(OUTPUT_DIR, f"{repo_name}_context.pdf")
    txt_path = os_path_join(OUTPUT_DIR, f"{repo_name}_context.txt")

    print("\n=== Repository to PDF/TXT Converter ===")
    print(f"Repository: {repo_name}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 40)

    # Get files to process
    print("\nCollecting files...")
    files_to_process = await get_files_to_process(repo_path)
    total_files = len(files_to_process)
    print(f"Found {total_files} files to process")

    # Generate PDF
    print("\nGenerating PDF...")
    pdf_processor = PDFProcessor(repo_path, pdf_path)
    await pdf_processor.process(files_to_process)
    print(f"PDF generated successfully: {pdf_path}")

    # Generate TXT
    print("\nGenerating TXT...")
    txt_processor = TXTProcessor(repo_path, txt_path)
    await txt_processor.process(files_to_process)
    print(f"Text file generated successfully: {txt_path}")

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
