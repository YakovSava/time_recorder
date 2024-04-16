from os import listdir
from setuptools import Extension, setup


def compile():
    for file in listdir():
        if file.endswith(('.c', '.cc', '.cpp', '.cxx')):
            setup(
                ext_modules=[Extension(
                    name=file.split('.')[0],
                    sources=[file],
                    language='c++'
                )]
            )

if __name__ == '__main__':
    compile()