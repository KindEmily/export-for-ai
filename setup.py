from setuptools import setup, find_packages

setup(
    name="export-for-ai",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "export-for-ai=export_for_ai.main:main",  # Corrected the entry point
        ],
    },
    install_requires=[
        # Add any dependencies here
    ],
    author="Emily Vlasiuk",
    #author_email="your.email@example.com",
    description="A tool to export data for AI processing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/export-for-ai",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
