# template-matrix
Template Matrix
# template-matrix

## Description

`template-matrix` is a Python program that processes Jinja2 templates with configuration data. It allows you to populate dynamic templates with data from JSON or YAML configuration files.  Optionally, it can validate the configuration data against a JSON schema (also in JSON or YAML format) to ensure data integrity.

## Features

* **Jinja2 Templating:** Uses Jinja2 for flexible and powerful template rendering.
* **Configuration Loading:** Supports loading configuration data from both JSON and YAML files.
* **Schema Validation:** Optionally validates configuration data against a JSON schema (in JSON or YAML format) using the `jsonschema` library.
* **Command-Line Interface:** Provides a simple command-line interface for easy usage.

## Requirements

* Python 3.x
* Jinja2
* PyYAML
* jsonschema

## Installation

1.  **Clone the repository (if applicable) or create a new project directory.**
2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS and Linux
    venv\Scripts\activate    # On Windows
    ```

3.  **Install the dependencies:**

    ```bash
    pip install Jinja2 PyYAML jsonschema
    ```

    or

    ```bash
    pip install -r requirements.txt #if you have a requirements.txt file
    ```

## Usage

```bash
python template-matrix.py -template <template_file> -config <config_file> [-jsonschema <schema_file>]
<template_file>: Path to the Jinja2 template file (.j2 or .jinja2 extension).<config_file>: Path to the JSON (.json) or YAML (.yaml or .yml) configuration file.<schema_file>: (Optional) Path to the JSON schema file (.json, .yaml, or .yml) for validating the config.ExampleCreate a template file (e.g., template.j2):<h1>Welcome, {{ user.name }}!</h1>
<p>Your role is: {{ user.role }}</p>
Create a configuration file (e.g., config.yaml):user:
  name: "John Doe"
  role: "Admin"
Run the program:python template-matrix.py -template template.j2 -config config.yaml
This will output the rendered HTML to the console:<h1>Welcome, John Doe!</h1>
<p>Your role is: Admin</p>
Schema Validation ExampleCreate a JSON schema file (e.g., schema.json):{
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "role": { "type": "string" }
      },
      "required": ["name", "role"]
    }
  },
  "required": ["user"]
}
Run the program with the -jsonschema option:python template-matrix.py -template template.j2 -config config.yaml -jsonschema schema.json
If the config.yaml file does not match the schema, the program will output an error message.Configuration SchemaThe configuration file should adhere to the following JSON schema:{
  "$schema": "[http://json-schema.org/draft-07/schema#](http://json-schema.org/draft-07/schema#)",
  "title": "Configuration Schema",
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "The title of the application"
    },
    "user": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the user"
        },
        "role": {
          "type": "string",
          "description": "The role of the user"
        }
      },
      "required": [
        "name",
        "role"
      ],
      "description": "Information about the user"
    },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "The name of the item"
          },
          "price": {
            "type": "number",
            "description": "The price of the item"
          }
        },
        "required": [
          "name",
          "price"
        ],
        "description": "An item in the list"
      },
      "description": "A list of items"
    },
    "show_message": {
      "type": "boolean",
      "description": "Whether to show a message"
    },
    "message_content": {
      "type": "string",
      "description": "The content of the message"
    }
  },
  "required": [
    "title",
    "user",
    "items",
    "show_message",
    "message_content"
  ]
}
Error HandlingThe program provides informative error messages for the following:Missing template or configuration files.Errors reading files.Invalid JSON or YAML syntax in configuration or schema files.Unsupported file formats.Schema validation errors.Contributing(Add your