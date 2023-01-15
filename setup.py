import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Trading Patterns",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Preetam Sharma",                     # Full name of the author
    description="A python package for detecting complex trading patterns like Head and Shoulder Wedge up and many more.",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: LICENSE",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',                # Minimum version requirement of the package
    py_modules=["tradingpatterns"],             # Name of the python package
    package_dir={'':'tradingpattern/src'},     # Directory of the source code of the package
    install_requires=["numpy","pandas"]                     # Install other dependencies if any
)