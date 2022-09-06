from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
  Extension("verse_match", ["./verse_match.pyx"])
]

setup (
  ext_modules=cythonize(extensions, annotate=True)
)