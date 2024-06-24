from setuptools import setup, find_packages

from openvoice_api_client import __version__

setup(
    name='openvoice_api_client',
    version=__version__,
    description='OpenVoice API client',
    url='https://github.com/ground-creative/openvoice-api-client-python',
    author='Carlo Pietrobattista',
    author_email='irony00100@gmail.com',
    license='MIT',
    py_modules=['openvoice_api_client'],
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
