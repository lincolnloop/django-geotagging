from setuptools import setup, find_packages

setup(
    name='django-geotagging',
    version='0.0.2',
    description='This is a geotagging application. It can be used to localised your content',
    author='Yann Malet',
    author_email='yann.malet@gmail.com',
    url='https://code.launchpad.net/django-geotagging',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools', 'setuptools_bzr'],
)
