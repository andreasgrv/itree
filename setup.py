from setuptools import setup

setup(
        name='itree',
        packages=['itree'],
        version='0.0.1',
        author='Andreas Grivas',
        author_email='andreasgrv@gmail.com',
        description='Indexable tree structure',
        # url='https://github.com/andreasgrv/tictacs',
        # download_url='https://github.com/andreasgrv/tictacs/tarball/0.0.3',
        license='BSD',
        keywords=['tree'],
        classifiers=[],
        install_requires=[
            # 'pyyaml',
            ],
        setup_requires=['pytest-runner'],
        tests_require=['pytest']
        )
