import setuptools

setuptools.setup(
    name="metasub-scripts",
    version="0.9.0",
    url="https://github.com/MetaSUB/metasub-scripts",

    author="David C. Danko",
    author_email="dcdanko@gmail.com",

    description="Scripts for various metasub related things",

    packages=['generators'],
    package_dir={'generators': 'generators'},

    install_requires=[
        'click==6.7'
    ],

    entry_points={
        'console_scripts': [
            'metasub-generator=generators.cli:main',
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
