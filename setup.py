from setuptools import setup, find_packages

setup(
    name='pepino-bdd',         # How you named your package folder (MyLib)
    packages=find_packages(".", include=['pepino*'], exclude=['tests']),   # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    license='GPL2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Pepino BDD',   # Give a short description about your library
    author='Patrick Gallagher',                   # Type in your name
    url='https://github.com/patrickguk/pepino',   # Provide either the link to your github or to your website
    keywords=['Cucumber', 'Gherkin', 'BDD'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'gherkin-official',
        'termcolor',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Testing :: BDD',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    tests_require=[
        'setuptools',
        'coverage',
        'flake8'
        'flake8-deprecated',
        'flake8-print'
        'flake8-comprehensions',
        'pep8-naming'
        'flake8-bugbear',
        'mypy'
        'pytest'
        'pytest-sugar'
        'pytest-cov'
    ]
)
