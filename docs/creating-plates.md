# Creating Plates

Flatware uses Jinja2 syntax for creating plates. By default, plates are stored in your home directory in a folder named `.plates`. On a *nix distribution, this is `~/.plates`.

## Basics of a Plate

A basic plate has a section of the file for defining variables, with the rest of the file being the template.

```
[subject]
type=str
default=world
---
Hello, {{ subject }}!
```

If we saved this plate as `~/.plates/myplate`, we can use it from the command line like this:

```bash
flatware myplate --subject $USER
Hello, <username>!
```

## Saving Plates to Files

To save plate output to a file, simply use *nix style pipes:

```bash
flatware myplate --subject $USER > greeting.txt
flatware myplate --subject $USER | xclip -sel clipboard
```

## Argument Syntax

Plates use a specific syntax for defining arguments, based on `.ini` configuration files.

### Argument Names

Argument names are placed in brackets at the start of an argument definition.

```
[argument]
type: str
```

### Types

Arguments for plates are typed. Valid types for plate arguments are as follows:

* str: A string. This is the default type.
* float: A floating point number
* int: A valid integer
* list: A list, space delimited. Ex: "fork spoon knife"

```
[argument]
type=list
```

### Default Values

It can be helpful to have an optional argument. You may set a default value for an argument with the `default` attribute. Default values are parsed according to argument types

```
[argument]
type=int
default=7
```

### Finishing Up

Arguments are defined at the top of a plate. To end the argument section, three dashes and a new line are added.

```
[argument]
type=list
default="spork cup dish"
---
```

## Template Syntax

Flatware uses Jinja2 as its templating language for the templates in plates. For complete documentation on Jinja2, please see [the documentation.](jinja.pocoo.org/docs/)

### Using Variables

You can add variables into your plate's template using curly brackets. Arguments are stored as variables under their argument name.

```
{{ argument }}
```

### Checking Arguments

Jinja2 has support for many logical operators and functions. One of the most useful is `if`.

```
{% if argument %}
{{ argument }}
{% else %}
No argument here!!!
{% endif %}
```

### Using Loops

Jinja2 supports looping using `for` syntax. If your plate contains a list, this is especially handy.

```
[places]
type=list
default="Cali Texas Washington"
---
{% for place in places %}
Visit {{ place }}!
{% endfor %}
```
