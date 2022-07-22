from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in dynamic_closure/__init__.py
from dynamic_closure import __version__ as version

setup(
	name="dynamic_closure",
	version=version,
	description="dynamic closure",
	author="admin",
	author_email="lokesh.w@indictranstech.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
