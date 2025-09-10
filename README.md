[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/6718/badge)](https://bestpractices.coreinfrastructure.org/projects/6718)
[![GitHub](https://img.shields.io/badge/issue_tracking-github-blue.svg)](https://github.com/claimed-framework/component-library/issues)



# CLAIMED - It's time to concentrate on your code only

For more information, please visit the project's [website](https://claimed-framework.github.io/)

## Credits

CLAIMED is supported by the EU’s Horizon Europe program under Grant Agreement number 101131841 and also received funding from the Swiss State Secretariat for Education, Research and Innovation (SERI) and the UK Research and Innovation (UKRI).

# Install

```bash
pip install claimed
```

This package installs the [CLAIMED Component Library (CCL)](https://pypi.org/project/claimed/), [CLAIMED Component Compiler (C3)](https://pypi.org/project/claimed-c3/) and the [CLAIMED CLI tool](https://pypi.org/project/claimed-cli/) which can be used to run operators locally. 


# Build & Publish
```bash
python -m build # might require a 'pip install build'
python -m twine upload --repository pypi dist/* # might require a 'pip install twine'
rm -r dist
```



