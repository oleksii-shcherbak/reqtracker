"""Import to package name mappings.

This module contains mappings from Python import names to their
corresponding PyPI package names.
"""

# Common import name to package name mappings
IMPORT_TO_PACKAGE = {
    # Image processing
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "skimage": "scikit-image",
    # Scientific computing
    "sklearn": "scikit-learn",
    "scipy": "scipy",
    "numpy": "numpy",
    "pandas": "pandas",
    # Web frameworks
    "flask": "Flask",
    "django": "Django",
    "fastapi": "fastapi",
    # Database
    "MySQLdb": "mysqlclient",
    "psycopg2": "psycopg2-binary",
    "pymongo": "pymongo",
    "redis": "redis",
    "sqlalchemy": "SQLAlchemy",
    # Data formats
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
    "lxml": "lxml",
    "openpyxl": "openpyxl",
    "docx": "python-docx",
    "PyPDF2": "PyPDF2",
    # Testing
    "pytest": "pytest",
    "nose": "nose",
    "mock": "mock",
    # Other common mappings
    "dotenv": "python-dotenv",
    "jwt": "PyJWT",
    "cryptography": "cryptography",
    "requests": "requests",
    "click": "click",
    "tqdm": "tqdm",
    "colorama": "colorama",
    "dateutil": "python-dateutil",
}
