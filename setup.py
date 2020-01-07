from setuptools import setup

setup(name='grippy',
      version='0.1.0',
      description='Pure python GRIB 2 parsing library',
      url='https://github.com/mpiannucci/grippy',
      author='Matthew Iannucci',
      author_email='rhodysurf13@gmail.com',
      license='MIT',
      packages=['grippy'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])