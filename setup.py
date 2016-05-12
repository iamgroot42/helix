from setuptools import setup,find_packages

setup(name='precog_testing',
      version='0.1',
      description='PreCog stuff',
      url='https://github.com/iamgroot42/image-classification',
      author='Anshuman Suri',
      author_email='anshuman14021@iiitd.ac.in',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pymongo',
          'ImageChops',
          'PIL',
          'numpy',
          'tweepy',
          'requests',
          'os'
      ],
      zip_safe=False)