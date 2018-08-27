from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='funkcium',
      version='0.1.6',
      description='Yet Another Python functional library, with scala inspiration',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/nykh/funkcium',
      author='nykh',
      author_email='nykh.pypi.199421@tryninja.io',
      license='MIT',
      packages=['funkcium', 'funkcium.functor'],
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
