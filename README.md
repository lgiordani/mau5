# Mau v5

Mau is a lightweight markup language heavily inspired by [AsciiDoc](https://asciidoctor.org/docs/what-is-asciidoc), [Asciidoctor](https://asciidoctor.org/) and [Markdown](https://daringfireball.net/projects/markdown/).

It is built on **Jinja** and designed for authors who want the simplicity of Markdown with the expressive power of templating. You can use Mau to create blog posts, books, documentation.

## Why Mau?

Mau combines:
- **Readable plain text** similar to Markdown.
- **Jinja templating** that allow to easily affect the rendering of Mau syntax.
- **Flexible output** via pluggable visitors (HTML, YAML, etc.)

## Backward compatibility

Mau v5 changed some parts of the Mau syntax in a non-backward compatible way. For example, now `source` and `footnote` are aliases that should be used with `@source` in blocks, while before they were mere subtypes used with `*source`.

The file `MAJOR_CHANGES.md` contains a list of the major changes that occurred.

## Installation

Mau is available on PyPI:

``` sh
pip install mau
```

## Plugins

Mau parses the source into an abstract tree and then transforms it into the final output using a visitor.

To render Mau syntax into HTML you need the HTML visitor

``` sh
pip install mau-html-visitor
```

To render Mau syntax into TeX you need the TeX visitor

``` sh
pip install mau-tex-visitor
```

## Quick Start

You can render a demo of Mau capabilities cloning this repository and running

``` sh
mau -c demo/config.yaml -i demo/demo.mau -t core:HtmlVisitor -o demo/demo.html
```

You can then open the file `demo/demo.html` with any browser.

## Documentation

The full documentation is available here:

https://project-mau.github.io/

## Pelican Plugin

There’s a Pelican plugin to use Mau directly in your blog:

https://github.com/pelican-plugins/mau-reader

Make sure to read the instructions in that repository to configure the plugin correctly.

## Support

Bug reports and feature requests: https://github.com/Project-Mau/mau/issues

Discussions and Q&A: https://github.com/Project-Mau/mau/discussions

## License

MIT License.
