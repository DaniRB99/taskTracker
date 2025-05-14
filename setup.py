from setuptools import setup, find_packages

setup(
    name="task_tracker",
    version="1.0",
    description="Un gestor de tareas simple desde la línea de comandos",
    author="Daniel Rocamora Bru",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "task_tracker=task_tracker.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        "task_tracker": ["data/*.json", "config/*.yaml"]
    }
)

#INSTALAR: pip install .

#CREAR NUEVA DISTRIBUCIÓN: pip build
#INSTALAR DISTRIBUCIÓN: pip install dist/task_tracker-0.1.0-py3-none-any.whl
