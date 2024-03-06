"""
Setup development environment
"""


import os

os.environ.setdefault("DOMAIN_NAME", "localhost")
os.environ.setdefault("IS_TEST", "1")
os.environ.setdefault("DISABLE_AUTH", "1")
os.environ.setdefault("PASSWORD", "1234")

from mediabiasscorer.app import main

if __name__ == "__main__":
    main()
