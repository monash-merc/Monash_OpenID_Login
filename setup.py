import os
from setuptools import setup, find_packages

version = '0.0.1'

setup(name='monash_openid_login',
      version=version,
      description="Strore.Monash specific login page for OpenID authentications",
      long_description="""\
MyTardis app to override default login template and use MOnash specific OpenID authentication methods.\
""",
      classifiers=[],
      keywords='store monash openID',
      author='Manish Kumar',
      author_email='manish.kumar@monash.edu',
      url='',
      license='',
      packages=find_packages(),
      )
