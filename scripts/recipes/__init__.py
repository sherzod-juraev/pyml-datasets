"""Recipes of the bundled datasets, one module per dataset.

A recipe is a module named after its dataset with a function ``build()`` that takes no
arguments, loads or downloads the raw data and returns it as a ``Built`` object. Recipes are
found by their module name, there is no registry to edit. Modules whose name starts with an
underscore hold shared code and are not recipes. The origin, the license and the changes of
a dataset are not part of its recipe, they are written once in ``pyml_datasets/datasets``.
"""

from collections.abc import Callable
from importlib import import_module
from pkgutil import iter_modules
from typing import cast

from scripts.recipes._common import Built


def recipe_names() -> tuple[str, ...]:
    """List the datasets that have a recipe.

    Returns
    -------
    tuple of str
        Recipe module names in alphabetical order, without importing the recipes.
    """
    return tuple(
        sorted(module.name for module in iter_modules(__path__) if not module.name.startswith("_"))
    )


def get_recipe(name: str) -> Callable[[], Built]:
    """Import the recipe of a dataset and return its ``build`` function.

    Parameters
    ----------
    name : str
        Dataset name, one of ``recipe_names()``.

    Returns
    -------
    callable
        The ``build`` function of the recipe.

    Raises
    ------
    ValueError
        If the dataset has no recipe.
    """
    if name not in recipe_names():
        raise ValueError(f"No recipe for dataset {name!r}. Recipes: {', '.join(recipe_names())}.")
    module = import_module(f"{__name__}.{name}")
    return cast(Callable[[], Built], module.build)


__all__ = ["Built", "get_recipe", "recipe_names"]
