Source and citation
-------------------

* Source: `palmerpenguins data package (Palmer Station Antarctica LTER and K. Gorman) <https://github.com/allisonhorst/palmerpenguins/tree/v0.1.0>`__
* Obtained from: The file inst/extdata/penguins.csv of the GitHub repository allisonhorst/palmerpenguins, tag v0.1.0. Its SHA-256 digest is pinned in the build recipe.
* Creators: Allison Marie Horst, Alison Presmanes Hill, Kristen B Gorman
* DOI: https://doi.org/10.5281/zenodo.3960218

Please cite the dataset as:

   Horst AM, Hill AP, Gorman KB (2020). palmerpenguins: Palmer Archipelago (Antarctica) penguin data. R package version 0.1.0. https://allisonhorst.github.io/palmerpenguins/. doi:10.5281/zenodo.3960218.

See also:

* Gorman KB, Williams TD, Fraser WR (2014). Ecological sexual dimorphism and environmental variability within a community of Antarctic penguins (genus Pygoscelis). PLoS ONE 9(3):e90081. https://doi.org/10.1371/journal.pone.0090081
* Adelie data record: https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f
* Gentoo data record: https://doi.org/10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689
* Chinstrap data record: https://doi.org/10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e

License
-------

`CC0 1.0 <https://creativecommons.org/publicdomain/zero/1.0/>`__, as stated by the source. The license was checked at the source on 2026-10-17. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Measurements are stored as float64 and the species as int64 labels (0 = Adelie, 1 = Chinstrap, 2 = Gentoo).
* The columns island and sex are stored as integer codes, see the categorical features. The missing values (NA in the CSV file) are stored as NaN.
* All columns except the species are features. No row and no column was removed.

.. note::

   The data are released under CC0. The package page also asks anyone who wants to publish with the data to contact its creator about the analysis and final products, and expects users to follow the US LTER Network Data Access Policy.
