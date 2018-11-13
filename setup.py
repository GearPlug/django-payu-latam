import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='django-payu-latam',
      version='0.1.0',
      include_package_data=True,
      license='MIT License',
      description='A django integration for PayU Latam.',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/django-payu-latam',
      author='GearPlug',
      author_email='support@gearplug.io',
      install_requires=[
          'django',
          'payu-python',
      ],
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Framework :: Django :: 2.0+',  # replace "X.Y" as appropriate
          'Intended Audience :: Developers',
          'License :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      zip_safe=False)
