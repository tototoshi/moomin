from setuptools import setup
import sys
sys.path.append("./test")

setup(
    name='moomin',
    py_modules=['moomin'],
    scripts=["scripts/moomin"],
    version="0.1.0",
    license='BSD',
    platforms=['POSIX', 'Windows'],
    description='Moinmoin client',
    author='Toshiyuki Takahashi',
    author_email='t.toshi.0412 at gmail.com',
    url='https://github.com/tototoshi/moomin',
    keywords=['MoinMoin'],
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities "
        ],
    long_description='MoinMoin client',
    install_requires = ["BeautifulSoup4"],
    test_suite = ''
    )
