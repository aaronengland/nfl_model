from setuptools import setup

setup(name='nfl_model',
      version='1.0.0',
      description='NFL Game Predictor',
      url='http://github.com/aaronengland/nfl_model',
      author='Aaron England',
      author_email='aaron.england.dev@gmail.com',
      license='MIT',
      packages=['nfl_model'],
      zip_safe=False,
      install_requires=['numpy==1.19.2',
                        'pandas==1.1.3',
                        'requests==2.0.0',
                        'beautifulsoup4==4.9.3',
                        'wquantiles==0.6'])
