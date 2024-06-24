from setuptools import setup, find_packages

setup(
    name='openvoice_api_client',
    version='1.0.0',
    description='OpenVoice API client',
    url='https://github.com/yourusername/mypackage',
    author='Your Name',
    author_email='irony00100@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
