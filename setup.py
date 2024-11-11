# setup.py

from setuptools import find_packages, setup

setup(
    name="personal_task_manager_cli",
    version="1.0.0",
    description="A command-line task manager for managing personal tasks",
    author="Lifeisacanvas24",
    author_email="lifeisacanvas24@gmail.com",
    packages=find_packages(),
    install_requires=[
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "personal-task-manager=main:main",
        ]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
