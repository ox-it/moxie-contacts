from setuptools import setup, find_packages


install_requires = open('requirements.txt').readlines()

setup(name='moxie-contacts',
    version='0.1',
    packages=find_packages(),
    description='Contact search module for Moxie',
    author='Mobile Oxford',
    author_email='mobileoxford@oucs.ox.ac.uk',
    url='https://github.com/ox-it/moxie-contacts',
    include_package_data=True,
    setup_requires=["setuptools"],
    install_requires=install_requires,
    test_suite="moxie_contacts.tests",
)