from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name='funkcium',
      version='0.1',
      description='Yet Another Python functional library, with scala inspiration',
      long_description=readme,
      long_description_content_type='text/markdown; charset=UTF-8',
      url='https://github.com/nykh/funkcium',
      author='nykh',
      author_email='nykh.pypi.199421@tryninja.io',
      license='MIT',
      packages=['funkcium'],
      zip_safe=False,
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
