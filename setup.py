from setuptools import setup


version = '0.2.0'

setup(
    name='django-snakeoil',
    version=version,
    packages=['snakeoil'],
    include_package_data=True,
    author='Tom Carrick',
    author_email='knyght@knyg.ht',
    license='Simplified BSD',
    long_description='A simple Django SEO module that allows attaching titles '
                     'and meta descriptions to objects and URLs',
    description='Simple Django SEO module',
    install_requires=['django >= 1.7'],
    requires=['django (>= 1.7)'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
