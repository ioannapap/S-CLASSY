# S-CLASSY
Discovering Rule Lists with Preferred Variables

This repository contains the code for using preferred variables to discover Hybrid Rule Lists (HRL) for univariate or multivariate classification in Data Mining. These models use the Minimum Description Length (MDL) principle as selection criterion.

## Dependencies

This project was written for Python>=3.7. All required packages from PyPI are specified in the `requirements.txt`.
*NOTE:* This list of packages includes the `gmpy2` package.
You can install the dependencies locally:

```bash
pip install -r requirements.txt
```

## Execution guide

- Open: `run_S-CLASSY.ipynb` or `run_S-CLASSY_cross_validation.ipynb` in the Jupyter Notebook dashboard by clicking on the name of the file in the dashboard.
- Update the configurations regarding the datasets tha you want to load (for more info read the comments in the .ipynb file).
- Run the file.


## References
   
[1] Proença, H.M., Grünwald, P., Bäck, T., van Leeuwen, M.: Robust subgroup discovery. Data Mining and Knowledge Discovery 36(5), 1885–1970 (2022)

[2] Proença, H.M., van Leeuwen, M.: Interpretable multiclass classification by MDL-based rule lists. Information Sciences 512, 1372–1393 (2020)
