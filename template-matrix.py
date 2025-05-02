import json
import yaml
import sys
import argparse
from jinja2 import Environment, FileSystemLoader, Template
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def read_file(filename):
    """
    Reads the content of a file.

    Args:
        filename (str): The path to the file.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If an error occurs while reading the file.
    """
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found: {filename}")
    except IOError as e:
        raise IOError(f"Error reading file {filename}: {e}")

def load_config(filename):
    """
    Loads the configuration data from a JSON or YAML file.

    Args:
        filename (str): The path to the configuration file.

    Returns:
        dict: The configuration data as a dictionary.

    Raises:
        json.JSONDecodeError: If the file is a JSON file and cannot be decoded.
        yaml.YAMLError: If the file is a YAML file and cannot be decoded.
        ValueError: If the file format is not supported.
    """
    try:
        config_data = read_file(filename)
        if filename.endswith('.json'):
            return json.loads(config_data)
        elif filename.endswith(('.yaml', '.yml')):
            return yaml.safe_load(config_data)
        else:
            raise ValueError("Unsupported config file format. Use .json, .yaml, or .yml")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON config file {filename}: {e.msg}", e.doc, e.pos)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error decoding YAML config file {filename}: {e}")
    except Exception as e:
        raise ValueError(f"Error loading config file: {e}")

def load_schema(filename):
    """
    Loads the JSON schema data from a JSON or YAML file.

    Args:
        filename (str): The path to the schema file.

    Returns:
        dict: The schema data as a dictionary.

    Raises:
        json.JSONDecodeError: If the file is a JSON file and cannot be decoded.
        yaml.YAMLError: If the file is a YAML file and cannot be decoded.
        ValueError: If the file format is not supported.
    """
    try:
        schema_data = read_file(filename)
        if filename.endswith('.json'):
            return json.loads(schema_data)
        elif filename.endswith(('.yaml', '.yml')):
            return yaml.safe_load(schema_data)
        else:
            raise ValueError("Unsupported schema file format. Use .json, .yaml, or .yml")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON schema file {filename}: {e.msg}", e.doc, e.pos)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error decoding YAML schema file {filename}: {e}")
    except Exception as e:
        raise ValueError(f"Error loading schema file: {e}")


def validate_config(config, schema_filename):
    """
    Validates the configuration data against a JSON schema.

    Args:
        config (dict): The configuration data.
        schema_filename (str): The path to the JSON schema file.

    Raises:
        jsonschema.exceptions.ValidationError: If the configuration does not
            conform to the schema.
        FileNotFoundError: If the schema file does not exist.
        json.JSONDecodeError: If the schema file is not valid JSON.
    """
    try:
        schema = load_schema(schema_filename)
        validate(instance=config, schema=schema)
    except ValidationError as e:
        raise ValidationError(f"Config validation failed: {e.message}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Schema file not found: {schema_filename}")
    except Exception as e:
        raise Exception(f"Error validating schema: {e}")

def main():
    """
    Main function to parse arguments, load configuration and template,
    and render the template with the configuration data.
    """
    parser = argparse.ArgumentParser(description='Process Jinja2 templates with configuration data.')
    parser.add_argument('-template', required=True, help='Path to the Jinja2 template file')
    parser.add_argument('-config', required=True, help='Path to the JSON or YAML configuration file')
    parser.add_argument('-jsonschema', help='Path to the JSON schema file for validating the config (optional)')

    args = parser.parse_args()

    template_file = args.template
    config_file = args.config
    schema_file = args.jsonschema

    # Check file extensions.
    if not (template_file.endswith(".j2") or template_file.endswith(".jinja2")):
        print("Error: Template file must have .j2 or .jinja2 extension")
        sys.exit(1)

    if not (config_file.endswith(".json") or config_file.endswith(".yaml") or config_file.endswith(".yml")):
        print("Error: Config file must have .json, .yaml, or .yml extension")
        sys.exit(1)

    if schema_file and not (schema_file.endswith(".json") or schema_file.endswith(".yaml") or schema_file.endswith(".yml")):
        print("Error: Schema file must have .json, .yaml, or .yml extension")
        sys.exit(1)

    try:
        # Load the configuration
        config = load_config(config_file)

        # Validate the configuration against the schema if provided
        if schema_file:
            validate_config(config, schema_file)

        # Load the template
        template_content = read_file(template_file)

        # Create a Jinja2 environment
        env = Environment(loader=FileSystemLoader('.'))  # Load templates from the current directory
        template: Template = env.from_string(template_content) # type: ignore

        # Render the template with the configuration
        output = template.render(config)

        # Output the result to stdout
        print(output)

    except (ValueError, FileNotFoundError, IOError, json.JSONDecodeError, yaml.YAMLError, ValidationError, Exception) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
