Filing Issues
-------------

When filing an issue, please use this template:

::

    ### Overview Description

    # Steps to Reproduce

    1.
    2.
    3.

    # Actual Results

    # Expected Results

    # Reproducibility

    # Additional Information:


Rules and guidelines for developers
-----------------------------------

Please create one branch (named accordingly) for each different feature/exchange you are working on and submit a separate PR for each one of them, like this it's easier to review and approve the PR.

If you just forked the project and you want to add your changes to the _dev_ branch, don't do that: create a new branch based on _dev_, instead.

E.g. if you are implementing a new exchange called BitFoo, create a branch called _bitfoo_.

If you are fixing some bugs in the _CryptoBar_ exchange, create a branch called _cryptobar-fix_ (or just _cryptobar_).

When the PR is merged, you can delete these branches. Like this, it's also easier for you to [sync your forked dev branch with the upstream one](https://help.github.com/articles/syncing-a-fork/).

- [Standardized Methods](README.md#user-content-standardized-methods) signatures should all have the required parameters, especially [*args and **kwargs](https://github.com/Crypto-toolbox/bitex/issues/183) (even if they are not used. Your IDE may complain: in that case you can add a comment to ignore the warning).
- Method signatures should have positional parameters first, then *args (if required), then optional parameters, e.g. see bitstamp interface: `def wallet(self, *args, pair=None, **kwargs)`
- Configure your IDE to show visual guides at 100 columns and write code that doesn't exceed 100 characters per line.
- For string formatting, always use str.format() and replace any old-style formatting with this.
- While fixing a bug or adding something new, feel free to fix typos, code style issues etc. _to the same file_, while working on it. It's a good practice to improve the code in general. If such fixes/rafactorings tend to become huge, consider doing a separate commit, so it will be easier to review.


PR Merge Criteria
-----------------

For a PR to be merged, the following statements must hold true:

-  PEP8 has been enforced
-  All commits of the PR are atomic
-  The pull request was approved by a core maintainer
