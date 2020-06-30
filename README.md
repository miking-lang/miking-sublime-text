# Miking syntax highlighter for Sublime Text
Provides syntax highlighting for Miking languages in Sublime Text 3. This
repository is also available through
[Sublime Text's Package Control](https://packagecontrol.io/) as
_Miking Syntax Highlighting_. Consider using that instead of manually
installing the syntax highlighting.

## Contributing
Do not modify any of the syntax highlighters situated in the root of the
repository as they are generated from files under `src/<lang>`. See the
README under each such folder for code contributing instructions to a
specific language highlighter.

Before pushing changes to a syntax highlighter, run `make build` as a command
in the repository root and commit any changes made by the makefile.

The versioned releases must follow the `Major.Minor.Patch` naming format, which
is further described [here](https://semver.org/). For changes to be available
in Package Control, a new release must be made. Until the first 1.0
specification of MCore is released, keep the major version as 0 and all GitHub
releases as pre-releases.

## Dependencies
To build/configure the syntax highlighter, the following software is required:
 - [Python 3](https://www.python.org/)
 - [GNU Make](https://www.gnu.org/software/make/)

The following Python 3 packages are required:
 - [regex](https://pypi.org/project/regex/)
