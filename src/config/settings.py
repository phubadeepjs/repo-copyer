import os
import psutil
from typing import Tuple

# File processing settings
BATCH_SIZE = 5000
MAX_CONCURRENT_TASKS = min(200, (psutil.cpu_count() * 4))
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for file reading

# File size limits
MAX_FILE_SIZE = 1024 * 1024  # 1MB
MAX_FORMAT_FILE_SIZE = 100 * 1024  # 100KB

# Output settings
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "output")

# Exclude patterns
EXCLUDE_PATTERNS: Tuple[str, ...] = (
    # Version Control
    ".git", ".svn", ".hg",
    # Python
    "__pycache__", "*.pyc", "*.pyo", "*.pyd", "*.so", ".Python",
    "build/", "develop-eggs/", "dist/", "downloads/", "eggs/", ".eggs/",
    "lib/", "lib64/", "parts/", "sdist/", "var/", "wheels/",
    "*.egg-info/", ".installed.cfg", "*.egg", "MANIFEST",
    ".env", ".venv", "env/", "venv/", "ENV/",
    # Node.js / JavaScript / TypeScript
    "node_modules/", "npm-debug.log*", "yarn-debug.log*", "yarn-error.log*",
    ".npm", ".yarn", "package-lock.json", "yarn.lock", "*.tsbuildinfo",
    "dist/", "build/", ".next/", "out/", ".nuxt/", ".output/", "report*", "reports*",
    # Java / Kotlin
    "target/", "*.class", "*.jar", "*.war", "*.ear", "*.zip", "*.tar.gz",
    "*.rar", "hs_err_pid*", ".gradle/", "build/", "out/", ".idea/",
    "*.iml", "*.iws", "*.ipr", ".settings/", ".project", ".classpath",
    # Go
    "bin/", "pkg/", "*.exe", "*.exe~", "*.dll", "*.so", "*.dylib",
    "*.test", "*.out", "go.work",
    # Swift
    "*.xcodeproj/", "*.xcworkspace/", "*.pbxuser", "*.mode1v3",
    "*.mode2v3", "*.perspectivev3", "*.xcuserstate", "xcuserdata/",
    "*.moved-aside", "*.xccheckout", "*.xcscmblueprint", "DerivedData/",
    "*.hmap", "*.ipa", "*.dSYM.zip", "*.dSYM",
)

def get_optimal_batch_size() -> int:
    """Calculate optimal batch size based on system memory."""
    memory = psutil.virtual_memory()
    available_memory = memory.available * 0.5  # Use 50% of available memory
    avg_file_size = 10 * 1024  # Assume average file size of 10KB
    return min(10000, int(available_memory / avg_file_size))

# Update batch size based on system resources
BATCH_SIZE = get_optimal_batch_size()
