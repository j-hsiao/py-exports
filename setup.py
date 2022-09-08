from setuptools import setup
from jhsiao.namespace import make_ns
make_ns('jhsiao')
setup(
    name='jhsiao-exports',
    version='0.0.1',
    author='Jason Hsiao',
    author_email='oaishnosaj@gmail.com',
    description='register items to __all__',
    packages=['jhsiao'],
    py_modules=['jhsiao.exports'],
    install_requires=[
        'jhsiao-scope @ git+https://github.com/j-hsiao/py-scope.git']
)
