from setuptools import setup, find_packages

LONG_DESCRIPTION = None
README_MARKDOWN = None

with open('README.md') as markdown_source:
    README_MARKDOWN = markdown_source.read()

try:
    import pandoc
    pandoc.core.PANDOC_PATH = 'pandoc'
    # Converts the README.md file to ReST, since PyPI uses ReST for formatting,
    # This allows to have one canonical README file, being the README.md
    doc = pandoc.Document()
    doc.markdown = README_MARKDOWN
    LONG_DESCRIPTION = doc.rst
except ImportError:
    # If pandoc isn't installed, e.g. when downloading from pip,
    # just use the regular README.
    LONG_DESCRIPTION = README_MARKDOWN

setup(
    name='MongoDBProxy',
    py_modules=['mongodb_proxy'],
#    version='',
    description='Proxy around MongoDB connection that automatically handles AutoReconnect exceptions.',
#    author='',
#    author_email='',
    long_description=LONG_DESCRIPTION,
#    license='',
#    classifiers=[
#    ],
    setup_requires=['pyandoc'],
    install_requires=['pymongo'],
    url="https://github.com/arngarden/MongoDBProxy"
)
