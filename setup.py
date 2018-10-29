import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basketball_reference_web_scraper",
    version="1.0.0",
    author="Jae Bradley",
    author_email="jae.b.bradley@gmail.com",
    license="MIT",
    description="A client for the Basketball Reference web site that gets data via scraping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaebradley/basketball_reference_web_scraper",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.0.0",
    install_requires=[
        "certifi==2018.10.15",
        "chardet==3.0.4",
        "idna==2.7",
        "lxml==4.2.5",
        "pytz==2018.6",
        "requests==2.20.0",
        "urllib3==1.24",
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
