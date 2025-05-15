# Repository to PDF/TXT Converter

A Python tool that converts a repository's contents into both PDF and TXT formats, with code formatting and syntax highlighting.

## Features

- Converts repository contents to both PDF and TXT formats
- Maintains repository structure in the output
- Formats code using appropriate formatters (black for Python, prettier for web files)
- Handles large repositories efficiently with batch processing
- Skips binary files and large files for better performance
- Supports various file types and languages

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd repo-copyer
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with a repository path as an argument:

```bash
python -m src.main <repository_path>
```

The script will:
1. Process the repository
2. Generate a PDF file in the `output` directory
3. Generate a TXT file in the `output` directory

Example:
```bash
python -m src.main /path/to/your/repo
```

## Output

The script generates two files in the `output` directory:
- `<repo_name>_context.pdf`: A formatted PDF document containing the repository contents
- `<repo_name>_context.txt`: A text file containing the repository contents

## Configuration

You can modify various settings in `src/config/settings.py`:
- File size limits
- Batch processing size
- Concurrent task limits
- Excluded patterns

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## License

MIT License