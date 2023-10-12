from setuptools import find_packages, setup
from typing import List

with open("README.md", "r", encoding= "utf-8") as f:
    long_description = f.read()


__version__ == "0.0.0"

REPO_NAME = "Lumi"
AUTHOR_USER_NAME = "CatSci"
SRC_REPO = "Lumi"
AUTHOR_EMAIL = "atul.yadav@catsci.com"

HYPEN_E_DOT = '-e .'

# def get_requirements()->List[str]:
#     """Returns a list of requirements"""

#     requirements_list:List[str] = []
#     with open('requirements.txt') as f:
#         requirements_list = f.readlines()
#         requirements_list = [req.replace("\n", "") for req in requirements_list]
        
#         if HYPEN_E_DOT in requirements_list:
#             requirements_list.remove(HYPEN_E_DOT)

#     return requirements_list


setup(
    name = SRC_REPO,
    version = __version__,
    author = AUTHOR_USER_NAME,
    author_email = AUTHOR_EMAIL,
    description= 'Python package to create experiments in Lumi and pass data from Lumi to ELN',
    long_description= long_description,
    url = f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls = {
        "BUG Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir = {"": "Lumi"},
    packages = setup.find_packages(where = "Lumi")
)