#-*- coding: utf-8 -*-
"""pydemo setup.py packaging and distribution script"""

from setuptools import setup, find_packages
import platform
import os


def _replace_readline(req):
    if req.startswith("readline"):
        return "pyreadline"
    return req


def get_requirements(replace_readline=False):
    reqs_filename = "requirements_win.txt" if platform.system().lower() == "windows" else "requirements.txt"
    try:
        with open(reqs_filename) as reqs_file:
            reqs = filter(bool, (line.replace("\n", "").strip() for line in reqs_file))
            if replace_readline:
                reqs = map(_replace_readline, reqs)
            return list(reqs)
    except IOError:
        pass
    return []

exceptions = []
for reqs in (get_requirements(), get_requirements(True)):
    try:
        setup(
            name="pydemo",
            version="0.1.0",
            description="Python code demonstration console for didactic purposes",
            long_description="Python code demonstration console for didactic purposes. \
        Prints and executes input files in blocks of lines. Extends code.InteractiveConsole. \
        Adapted for Python 3.",
            author="Pablo Enfedaque",
            author_email="pablito56@gmail.com",
            url="https://github.com/pablito56/pydemo",
            packages=find_packages(exclude=["test*"]),
            include_package_data=True,
            entry_points={
                "console_scripts": [
                    "pydemo = pydemo.pydemo:main",
                ]
            },
            install_requires=reqs,
            test_suite="nose.collector",
            tests_require="nose",
        )
        break
    except SystemExit as exc:
        print("\n\tCaught SystemExit. Trying alternative requirements\n")
        import traceback
        traceback.print_exc(exc)
        exceptions.append(exc)
else:
    print("\n\tScript failed. Caught to following SystemExit exceptions:")
    for exc in exceptions:
        print(exc)
