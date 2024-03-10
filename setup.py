from setuptools import setup, find_packages

setup(
    name="portfolio-optimize",
    version="1.1.1",  # Incrementing version to reflect new changes
    author="Manu Jayawardana",
    author_email="manujajayawardanais@gmail.com",
    description="A Python package for portfolio optimization. (Note: This package is under ongoing development. Contributions and corrections are welcome!)",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/manujajay/portfolio-optimize", 
    packages=find_packages(),
    install_requires=["numpy", "pandas", "yfinance", "matplotlib", "tqdm"],  # Updated dependencies
    classifiers=[
        "Programmi