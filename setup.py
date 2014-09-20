from setuptools import setup

setup(
    name='flask-kdb',
    version='0.1',
    py_modules=[
        'flask_kdb'
    ],
    url='github.com/buckie/flask-kdb',
    license='MIT',
    author='wjm',
    keywords=['kdb+'],
    author_email='',
    zip_safe=False,
    platforms='any',
    description='KDB connection wrapper for Flask based on qPython',
    install_requires=[
        'Flask>=0.8',
        'qPython>=1.0.Beta.1'
    ],
    classifiers=[
        'Development Status :: 5 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7'
    ]
)
