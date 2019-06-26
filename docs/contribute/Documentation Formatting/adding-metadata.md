---
title: Documentation Metadata
excerpt: Writing a guide or tutorial for GS Quant? Learn best practices for working with our documentation format.
datePublished: 2019/06/20
keywords:
  - Contribute
  - Markdown
  - Frontmatter
  - Documentation
authors:
  - name: Chris Droukas
    github: chrisdroukas
  - name: Jon Hickman
    github: jonhickman5
---

Goldman Sachs Developer documentation supports a number of properties to provide information about a document. This information may be used in a variety of contexts across Goldman Sachs Developer to enrich and improve the experience of reading and writing guides, tutorials, and documentation.

## Supported Properties

While these properties are not required, including as much information as possible is preferred. Goldman Sachs Developer will attempt to infer some properties (for example, an `excerpt`) if not included.

Properties do not need to be provided in any particular order.

Avoid referencing metadata as variables within a document.

| Property                              | Description                                                                                                                                                                                                                     |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `authors [{ name, github }]`          | The authors of a document. A name and Github username for each author may be displayed with uniform formatting as part of a byline. A Github username is required to display an avatar in a list of contributors on a document. |
| `dateModified`                        | The date a document was last modified. Dates are formatted `YYYY/MM/DD`.                                                                                                                                                        |
| `datePublished`                       | The date a document was originally published. Content published recently may be displayed first. Dates are formatted `YYYY/MM/DD`.                                                                                              |
| `excerpt`                             | A brief description of a document's contents. An excerpt is typically the leading paragraph of a document. An excerpt may be displayed in document previews.                                                                    |
| `githubUrl`                           | A fully qualified link to the current document in Github.                                                                                                                                                                       |
| `image { description, url }`          | An image representative of the document's contents. An image may be displayed in document previews. A description may be used for alt text and accessibility.                                                                   |
| `keywords []`                         | Keywords that describe a document. Keywords may be used for indexing and discovery.                                                                                                                                             |
| `links [{ title, description, url }]` | Links to other documents in Goldman Sachs Developer. A title, description, and URL for each link may be displayed as supplementary content in a document.                                                                       |
| `title`                               | The title of a document. A title will be displayed with uniform formatting at the beginning of a document.                                                                                                                      |

## Metadata Formatting

Metadata is inserted at the beginning of a Markdown or MDX (`.md` or `.mdx`) document in a block fenced at the beginning and end by `---`. Goldman Sachs Developer will parse information provided as metadata automatically — as such, there is no need to restate this information within a document body.

```yaml
title: Documentation Formatting
excerpt: Writing a guide or tutorial for GS Quant? Learn best practices for working with Markdown and our documentation format.
datePublished: 2019/05/22
dateModified: 2019/05/23
image:
  title: Image Title
  url: https://gs.com
githubUrl: https://github.com/goldmansachs
keywords:
  - Contribute
  - Markdown
  - Frontmatter
  - Documentation Formatting
links:
  - title: Goldman Sachs Developer
    description: Visit the Goldman Sachs Developer homepage.
    url: https://developer.gs.com/
  - title: Goldman Sachs
    description: Visit the Goldman Sachs homepage.
    url: https://gs.com/
authors:
  - name: Chris Droukas
    github: chrisdroukas
  - name: Jon Hickman
    github: jonhickman5
```
