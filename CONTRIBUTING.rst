Contributing Guide
==================

Github Issues - Bug Reports
    You found a bug and would like to see it fixed - alright then! Make sure to
    include the following:

        - Your Python and OS version
        - A `pip freeze` of the environment with which you were able to
            reproduce the bug consistently
        - Any logs you may have (make sure to set your `logging` level to `logging.DEBUG`)
        - A description of the expected behaviour
        - A description of the actual behaviour (as witnessed from your account)

    All of these are **required** before work on a bug fix can be started.

Github Issues - Feature Requests
    If you'd like to see a new feature provided by :mod:`bitex`, you're always
    welcome to submit a feature request on the GitHub issue tracker.
    When you do, be sure to include the following details:

    - What is the current state (e.g. how do things work at the moment from your perspective)
    - What is the desired state (e.g. your feature description)
    - One or more User Stories which can be used to make sure the feature was
        implemented as you intended.

    All of these are **required** before work on a feature can be started.

Branch Commit Messages
    Should be as atomic as possible. We do not require extensive reasoning in
    commit messages on a PR branch; a descriptive subject line should be enough
    to describe your change. If it is not, perhaps your change is too big.

Merge Commit Messages
    Require a reasonably detailed description of the change being implemented,
    preferably with a linked github issue present. You do not need to write a
    20 page essay on the change, but it should give any future reader a good idea
    on how and why you changed the code the way you did.
    Finally, if the change affects the code base (e.g. anything in bitex/bitex), it
    needs to be prefixed with `FEAT-#<issue_num>` or `FIX-#<issue_num>`, depending
    on the nature of the change respectively. This is required, as new features and
    fixes are automatically tagged and published to PyPi by our CI setup. In order
    for this to happen though, the stated prefix is required.

Merging Changes
    When merging a PR, the commits of the PR are preserved (i.e. neither squashed nor rebased).
    If the merge commit's subject line starts with `FEAT` or `FIX`, a new version
    is tagged and released on PyPi.

Test Coverage
    Any PR touching the code base, needs to have test coverage. It's typically expected
    that the PR does not decrease overall test coverage of the project.
    Coverage is determined by `pytest-cov`.

Unit & Integration Tests
    Either of these is required before a PR can be merged (if it touches the codebase).
    If a user story is present in the related PR's GitHub issue, it should be present
    as an integration test. Otherwise, unit tests will suffice.
    If possible, try not to mock objects living in the :mod:`bitex` project (but
    be sensible about when an exception for this is reasonable).
    When in doubt, ask the devs.

