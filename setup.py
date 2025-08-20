#!/usr/bin/env python3
"""
Setup script for Weather Assistant App
Developed by hafizullahkhokhar1
"""

from setuptools import setup, find_packages
import sys
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="weather-assistant-app",
    version="1.0.0",
    author="hafizullahkhokhar1",
    author_email="hafizullahkhokhar1@gmail.com",
    description="A beautiful real-time weather application with animations and smart advice",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/hafizullahkhokhar1/weather-assistant-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "weather-assistant=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.py"],
    },
    keywords="weather, gui, api, openweathermap, pakistan, forecast, animation",
    project_urls={
        "Bug Reports": "https://github.com/hafizullahkhokhar1/weather-assistant-app/issues",
        "Source": "https://github.com/hafizullahkhokhar1/weather-assistant-app",
        "Documentation": "https://github.com/hafizullahkhokhar1/weather-assistant-app/blob/main/README.md",
    },
)