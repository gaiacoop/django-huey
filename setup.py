from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-huey",
    version="1.0.0",
    scripts=[],
    author="GAIA - Cooperativa de desarrollo de software",
    author_email="contacto@gaiacoop.tech",
    description="An extension for django and huey that supports multi queue management",
    long_description=long_description,
    install_requires=[
        "django>=2.2",
        "huey>=2.0",
    ],
    long_description_content_type="text/markdown",
    url="https://github.com/gaiacoop/django-huey",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)