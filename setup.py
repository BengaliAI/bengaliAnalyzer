import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bengalianalyzer",
    license="BSD 3-Clause ""New"" or ""Revised"" License",
    license_files=('LICENSE.txt',),
    version="0.0.107",
    author="A. A. Noman Ansary",
    author_email="showrav.ansary.bd@gmail.com",
    description="A package for analyzing entities present in Bengali sentence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BengaliAI/bengaliAnalyzer",
    project_urls={
        "Bug Tracker": "https://github.com/BengaliAI/bengaliAnalyzer/issues",
    },
    install_requires=['pandas', 'indicparser', 'bnunicodenormalizer', 'tqdm', 'termcolor'],
    include_package_data=True,
    package_data={'': ['src/bengali_analyzer/assets/*.csv', 'src/bengali_analyzer/assets/*.txt', 'include src/bengali_analyzer/assets/*.json', 'src/bengali_analyzer/assets_orig/*.csv', 'src/bengali_analyzer/assets_orig/*.txt', 'include src/bengali_analyzer/assets_orig/*.json']},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    zip_safe=False,
)
