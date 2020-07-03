from setuptools import setup, find_packages

setup(
    name='mzt_http_utils',
    version="1.0",
    author="Roberto Mizuuti",
    author_email="rmizuuti@gmail.com",
    url="https://github.com/rmizuuti/mzt_http_utils",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
