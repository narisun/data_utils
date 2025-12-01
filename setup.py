from setuptools import setup, find_packages

setup(
    name="data_utils",
    version="0.1.0",
    description="A collection of CLI data utilities",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            # This allows you to type 'csv-compare' in the terminal directly
            'csv-compare=utils.csv_compare:main',
        ],
    },
)