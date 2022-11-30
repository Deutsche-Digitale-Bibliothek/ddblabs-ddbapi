import pathlib
import setuptools

here = pathlib.Path(__file__).parent
readme = (here / 'README.md').read_text()

setuptools.setup(
    name="ddbapi",
    version="0.1.2",
    author="Karl Krägelin",
    author_email="kraegelin@sub.uni-goettingen.de",
    description="Library for querying DDB infrastructure",
    url='https://gitlab.gwdg.de/becker210/ddbapi',
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        "requests",
        "pandas",
        "urllib3"
    ],
    python_requires='>=3.8.5'
)
