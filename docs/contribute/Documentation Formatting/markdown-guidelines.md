---
title: Markdown Guidelines
excerpt: Learn how to work with Markdown.
datePublished: 2019/06/20
keywords:
  - Contribute
  - Markdown
  - Documentation
authors:
  - name: Chris Droukas
    github: chrisdroukas
  - name: Alizah Herman
    github: alizahgrace
---

Goldman Sachs Developer documentation is written in [Markdown](https://daringfireball.net/projects/markdown/) or [MDX](https://mdxjs.com/).

## Getting to Know Markdown

### Headings

Use headings to define sections in a document. The relationship between headings should define the structure and outline of a document.

```none
# H1
## H2
### H3
#### H4
##### H5
###### H6
```

Avoid manually inserting `H1` headings. Goldman Sachs Developer automatically inserts and formats document titles [provided as metadata](/gsquant/contribute/Documentation-Formatting/adding-metadata).

### Emphasis

```none
**I'm bold text!**
*I'm italic text.*
```

The syntax in the block above will render as:

**I'm bold text!**
_I'm italic text._

### Lists

```none
- Item 1
- Item 2
- Item 3

1. Item 1
2. Item 2
3. Item 3
```

The syntax in the block above will render as:

- Item 1
- Item 2
- Item 3

1. Item 1
2. Item 2
3. Item 3

### Tables

Tables are created using `|` and `-` delineators. Table boundaries are defined by leading and trailing pipes, and columns are separated by pipes. Create a table header by insering a line of dashes in a separate row.

Each row of text is rendered as a separate row. Empty rows, columns and cells are rendered.

```none
| First Header                    | Second Header   |
| ------------------------------- | --------------- |
| Some text                       | Additional text |
| [Goldman Sachs](https://gs.com) | `Inline Code`   |
```

The code block above renders as:

| First Header                    | Second Header   |
| ------------------------------- | --------------- |
| Some text                       | Additional text |
| [Goldman Sachs](https://gs.com) | `Inline Code`   |

### Blocks

Blocks are custom HTML elements in Goldman Sachs Developer used to distinguish content that requires special attention. Blocks may be incompatible and render incorrectly with external editors and/or viewers (for example, Github).

Three block types — `note`, `warning` and `tip` — are available. Each block type automatically includes an associated title for that type.

```html
<note>I'm a block of information.</note>

<warning>Careful! I'm a warning.</warning>

<tip>You may find this tip helpful.</tip>
```

The code block above renders as:

<note>I'm a block of information.</note>

<warning>Careful! I'm a warning.</warning>

<tip>You may find this tip helpful.</tip>

Blocks support standard HTML elements, but do not support nested Markdown.
