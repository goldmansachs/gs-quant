# Contributing to gs-quant

This file contains information about reporting issues as well as contributing code. Make sure
you read our [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md) before you start participating.


# Development and Build Environment

gs-quant's development environment relies on the following:

### 1) Python 3.7+
Available at [Python.org](https://www.python.org/downloads/) or from your OS's package manager.


### 2) IDE
The main developers use [PyCharm](https://www.jetbrains.com/pycharm/) but you can use another IDE or editor.

Please do not commit IDE files.


# Issues
Search the issue tracker for a relevant issue or create a new one.


# Making changes
Fork the repository in GitHub and make changes in your fork.

Before you submit your first pull request, please first submit a DCO, per the instructions in the last section on this page.

Finally, submit a pull request. In your pull requests:
* Make sure you [rebase your fork](https://github.com/edx/edx-platform/wiki/How-to-Rebase-a-Pull-Request) so that pull requests can be fast-forward merges.
* We generally prefer squashed commits, unless multi-commits add clarity or are required for mixed copyright commits.
* Your commit message for your code must contain a `covered by: <dco>` line. See above.
* Every file you modify should contain a single line with copyright information after the Apache header:
```
//Portions copyright <copyright holder>. Licensed under Apache 2.0 license
```
* New files must contain the standard Apache 2.0 header with appropriate copyright holder.
* If you're going to contribute code from other open source projects, commit that code first with `covered by: <license>`
where `<license>` is license of the code being committed. Ensure the file retains its original copyright notice and add an appropriate line to
NOTICE.txt in the same commit. You can then modify that code in subsequent commits with a reference to your DCO and copyright.

# Licensing

Please make sure that any new dependency licenses are listed in the following list of pre-approved licenses list:

```
MIT
ASL (all versions)
BSD
BSD-like
``` 


# Coding Style
Please see [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).


# Appendix: Contribution Prerequisite: Submitting a DCO

If you have never contributed to gs-quant, or your copyright ownership has changed, you must first create a pull request that has
a developer certificate of origin (DCO) in it. To create this file, follow these steps:

For code you write, determine who the copyright owner is. If you are employed in the US, it's likely that your
employer can exert copyright ownership over your work, even if the work was not done during regular working hours or
using the employer's equipment. Copyright law is highly variable from jurisdiction to jurisdiction. Consult your
employer or a lawyer if you are not sure.

If you've determined that the copyright holder for the code you write is yourself, 
please fill out the following (replace all `<>` terms); place it in a file under `dco/<your name>.dco`. 

```
1) I, <your name>, certify that all work committed with the commit message 
"covered by: <your name>.dco" is my original work and I own the copyright 
to this work. I agree to contribute this code under the Apache 2.0 license.

2) I understand and agree all contribution including all personal 
information I submit with it is maintained indefinitely and may be 
redistributed consistent with the open source license(s) involved. 

This certification is effective for all code contributed from <date submitted> to 9999-01-01.
```

If you've determined that the copyright holder for the code you write is some other entity (e.g. your employer), 
you must ensure that you are authorized by the copyright holder to be able to license this code under the 
Apache 2.0 license for the purpose of contribution to gs-quant. Negotiating such authorization and administering 
the terms is entirely between you and the copyright holder. Please fill out the following (replace all
`<>` terms); place it in a file under `dco/<copyright holder name>-<your name>.dco`. 

```
1) I, <your name>, certify that all work committed with the commit message 
"covered by: <copyright holder name>-<your name>.dco" is copyright 
<copyright holder name> and that I am authorized by <copyright holder name> 
to contribute this code under the Apache 2.0 license.

2) I understand and agree all contribution including all personal 
information I submit with it is maintained indefinitely and may be 
redistributed consistent with the open source license(s) involved. 

This certification is effective for all code contributed from <date submitted> to 9999-01-01.
```

`<your name>` must reference your real name; we will not accept aliases, pseudonyms or anonymous contributions.
Issue a pull request with the appropriate DCO and a change to NOTICE.txt with
one line `This product contains code copyright <copyright holder name>, licensed under Apache 2.0 license`.