Flatware
=======

Create files from **plates** (single file template), right from the command line.

## Get Started

Let's make a plate for creating React components:

```javascript
[component]
type=str
default=MyComponent
---
import React from 'react';


class {{ component }} extends React.Component {
  
  render() {
    return (
      <div>{{ component }}</div>
    )
  }
}

export default {{ component }};
```

Save this to `~/.plates/react-component`. Now, we can install `Flatware` and try it out!

Install from source:

```bash
git clone https://github.com/madelyneriksen/flatware/
cd flatware
# Whatever you prefer for virtual environments
virtualenv .env
source .env/bin/activate
# Now we can use flatware!
flatware react-component --component Navar > navbar.js
```

Congrats! You made your first plate!

## Intro To Plates

Plates are files that contain configuration and a template.

Configuration in plates is similar to `*.ini` file syntax. Plate configuration defines command line arguments for the plate, as well as the typing and default value of each argument.

```ini
# In brackets is the name of the argument.
# Argument names are used in the command line for passing values.
[languages]

# Arguments have optional types.
# Valid values are str, int, float, and list
type=list

# You can set a default value for an argument.
# Default values are interpreted as their type (lists are space delimited)
default="python javascript rust"

# We mark the end of our configuration with three dashes and a new line
# Configuration is always at the top of a plate
---

```

Template syntax in plates uses Jinja2/Django syntax. Jinja2 allows plate authors to add loops, checks, and basic processing to templates easily.

```jinja
{% for language in languages %}
{{ language }} programming rocks!
{% endfor %}
```

Jinja2 is easy to use, but a lot to cover for one README. You can read more about Jinja2 [here](https://github.com/pallets/jinja).

## Contributing

Pull requests, issues, and feature requests are always welcome! If you'd like to develop a feature, here's the steps for making your dev environment.

```bash
# First, clone this repo from source
git clone https://github.com/madelyneriksen/flatware
cd flatware
# Install our requirements locally
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
# Install in dev mode
python setup.py develop
# Our tests should be working, let's check
pytest
```

Code is linted with the wonderful `pylint` as well as `pycodestyle`.

## License

Flatware is MIT Licensed.

## Special Thanks

* Audreyr for creating [cookiecutter](https://github.com/audreyr/cookiecutter), which inspired flatware
* The team of contributors working on [jinja2](https://github.com/pallets/jinja)
