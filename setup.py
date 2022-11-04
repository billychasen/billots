from setuptools import setup, find_packages

setup(name="billots",
      version="0.1.1",
      description="Official project of billots.org cryptocurrency.",
      keywords="billots cryptocurrency billot",
      url="https://github.com/billychasen/billots",
      author="Billy Chasen",
      author_email="billy@billychasen.com",
      license="MIT",
      packages=find_packages(),
      package_data={
        "billots": ["src/resources/*"],
        },
      python_requires='>=3',
      install_requires=[
        "attrs==17.2.0",
        "Automat==0.6.0",
        "constantly==15.1.0",
        "hyperlink==17.2.1",
        "incremental==17.5.0",
        "leveldb==0.194",
        "py==1.4.34",
        "pycrypto==2.6.1",
        "pytest==3.1.3",
        "six==1.10.0",
        "Twisted==22.10.0",
        "zope.interface==4.4.2",
        ],
      entry_points={
        "console_scripts": [
            "bwallet=billots.src.controller.wallet:main",
            "bserver=billots.src.controller.start:main",
            "mock_bservers=billots.src.mock.launch_servers:main",
            "mock_disputed=billots.src.mock.disputed_example:main",
            ],
        },
      zip_safe=False)
