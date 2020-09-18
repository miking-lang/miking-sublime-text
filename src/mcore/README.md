# MCore Syntax Highlighting
**Read this before making any changes to the MCore syntax highlighter.**

This syntax highlighter is designed to be a replication of the official MCore
parser. As such, it is able to distinguish the context of terms and set
highlighting based how they appear in the code. This also makes the syntax
highlighter slightly complicated since the MCore syntax is not very
LL1-friendly. Because of this, much is implemented multiple times depending on
which set of symbols that ends a context.

To avoid code duplication, the reimplementation of the same contexts are
handled by a fragment system where the base file can at specified points
include fragments with arguments. At the point where the base file includes a
fragment, it is also able to specify custom arguments, such as how the stack
should be affected on a match.

## Replace Rules
The replace rules listed in `replacements.sh` are:

 * `set: []` -> `pop: true`

These should get applied by the top-level makefile by running
```
./src/mcore/replacements.sh mcore.sublime-syntax
```
