from setuptools import setup,find_packages

setup(name='precog_testing',
      version='0.1',
      description='PreCog stuff',
      url='https://github.com/iamgroot42/image-classification',
      author='Anshuman Suri',
      author_email='anshuman14021@iiitd.ac.in',
      license='MIT',
      packages=find_packages(),
      package_data={'precog_testing': ['NN_Data/*']},
      install_requires=[
          'pymongo',
          'numpy',
          'tweepy',
          'requests',
      ],
      zip_safe=False)