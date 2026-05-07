"""
Setup configuration for Pancarbo Greenfuels AI System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pancarbo-greenfuels",
    version="1.0.0",
    author="Pancarbo AI Team",
    author_email="team@pancarbo.com",
    description="Industrial AI platform for biomass quality prediction and boiler optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Pancarbo-Greenfuels-AI-System",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Industrial Applications",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pancarbo=streamlit_app:main",
        ],
    },
    include_package_data=True,
    keywords=[
        "industrial-ai",
        "biomass",
        "boiler-optimization",
        "machine-learning",
        "predictive-maintenance",
        "streamlit",
        "dashboard",
    ],
)
