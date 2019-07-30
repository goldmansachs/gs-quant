---
title: Building Docs
excerpt: Building python function documentation
datePublished: 2019/06/22
dateModified: 2019/06/22
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Python
  - LaTeX
  - Sphinx
authors:
  - name: Andrew Phillips
    github: andyphillipsgs
links:
  - title: Sphinx
    url: http://www.sphinx-doc.org/en/master/
  - title: reStructuredText
    url: http://docutils.sourceforge.net/rst.html
---

gs-quant uses [Sphinx](http://www.sphinx-doc.org/en/master/) to generate Python
[API documentation](/gsquant/api/) automatically from the source code. Developers can
run Sphinx locally in order to build and view gs-quant documentation.

## Documentation Site

The gs-quant documentation site renders the output from the Sphinx generator. The API documentation in this site lives
in the `/docs` folder within the project.

<note>Make sure you have Sphinx installed through the development version of the project</note>

When you have finished writing your Python function, add it to the relevant section in the docs folder, by updating _gs_quant/docs/timeseries.rst_ and updating or creating a new [reStructuredText](http://docutils.sourceforge.net/rst.html) file (.rst). See example:

```
Title
-------

.. currentmodule:: gs_quant.package.module

.. autosummary::
   :toctree: functions

   func_1
   func_2
```

The `currentmodule` directive locates the Python module within the RST file. The `autosummary` directive along with
the `:toctree: functions` directive automatically generates documentation for the listed functions. For more details on
how to use reStructuredText with Sphinx see the following
[cheatsheet](https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html).

## Building Docs

Navigate to the docs folder via your console, and run the documentation generator as follows to build the HTML output:

```bash
gs_quant\docs>make html
```

This will create output under the _docs/\_build_ folder. To clean the existing docs first, run the following:

```bash
gs_quant\docs>make clean
```

If you added a new function, Sphinx will automatically create a file for it under _gs_quant/docs/functions_. Open the
file and update the header to match the following:

```
function_name
==================================

.. currentmodule:: gs_quant.package.module

.. autofunction:: function_name
```

We remove the package from the title to make the documentation cleaner. If you can find a way to do this automatically,
let us know! The output files are under _gs_quant/docs/\_build_. Open _index.html_ to view your function docs!
