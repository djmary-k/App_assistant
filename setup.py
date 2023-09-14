from setuptools import setup, find_namespace_packages

setup(
    name='App_assistant',
    version='1.0.2',
    description='Console bot that gives opportunity to save contacts, creat and save notes and sort files.',
    url='https://github.com/djmary-k/App_assistant.git',
    author='Maryna Kondratiuk, Tetiana Shevchenko, Anastasiia Kysliak, Volodymyr Mazurets, Oleksandr Semochkin',
    author_email='kondratyukmv@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['prettytable'],
    entry_points={'console_scripts': ['yfa=YFA.main:run']}
)