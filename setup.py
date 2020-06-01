import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basketball_reference_web_scraper",
    version="4.9.2",
    author="Jae Bradley",
    author_email="jae.b.bradley@gmail.com",
    license="MIT",
    description="A Basketball Reference client that generates data by scraping the website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaebradley/basketball_reference_web_scraper",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.4",
    install_requires=[
        "certifi==2018.10.15",
        "chardet==3.0.4",
        "idna==2.7",
        "lxml==4.5.1",
        "pytz==2018.6",
        "requests==2.20.0",
        "urllib3==1.24.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "NBA",
        "Basketball",
        "Basketball Reference",
        "basketball-reference.com",
    ],
)
