import os
import json

# Input and output file paths
ROOT_DIR = os.getcwd()  # Root directory where the script is run
RULES_DIR = os.path.join(ROOT_DIR, "rules")  # Subdirectory for JSON files
SETTINGS_FILE = os.path.join(ROOT_DIR, "settings.json")  # Path to settings.json
OUTPUT_FILE = os.path.join(ROOT_DIR, "main.tf")  # Output Terraform file in the root

def read_json_files(input_dir):
    """Read and parse all JSON files in a directory."""
    rules = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, "r") as f:
                try:
                    content = json.load(f)
                    rules.append(content)
                except json.JSONDecodeError as e:
                    print(f"Error parsing {file_name}: {e}")
    return rules

def read_settings_file(settings_file):
    """Read and parse the settings.json file."""
    if not os.path.exists(settings_file):
        print(f"Error: {settings_file} not found.")
        return None
    with open(settings_file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing {settings_file}: {e}")
            return None

def generate_custom_rules_blocks(rules):
    """Generate multiple Terraform custom_rules blocks."""
    custom_rules_blocks = []
    for rule in rules:
        block = f"""
  custom_rules {{
    name      = "{rule['name']}"
    priority  = {rule['priority']}
    action    = "Allow"

    match_condition {{
      match_variables {{
        variable_name = "RemoteAddr"
      }}
      operator = "IPMatch"
      values   = {json.dumps(rule['match_values'])}
    }}
  }}
"""
        custom_rules_blocks.append(block)
    return custom_rules_blocks

def generate_managed_rules_block(settings):
    """Generate the managed_rules block based on the settings.json file."""
    return f"""
  managed_rules {{
    managed_rule_set {{
      type    = "{settings['type']}"
      version = "{settings['version']}"
    }}
  }}
""" if settings else ""

def write_to_main_tf(output_file, settings, managed_rules_block, custom_rules_blocks):
    """Write the complete Terraform configuration to the main.tf file."""
    with open(output_file, "w") as f:
        f.write('resource "azurerm_web_application_firewall_policy" "example" {\n')
        f.write(f'  name                = "example-waf-policy"\n')
        f.write(f'  resource_group_name = "{settings["resource_group_name"]}"\n')
        f.write(f'  location            = "{settings["location"]}"\n')
        f.write('  policy_settings {\n')
        f.write('    mode = "Prevention"\n')
        f.write('  }\n')
        f.write(managed_rules_block)
        for block in custom_rules_blocks:
            f.write(block)
        f.write("}\n")

def main():
    if not os.path.exists(RULES_DIR):
        print(f"The directory {RULES_DIR} does not exist.")
        return

    rules = read_json_files(RULES_DIR)
    if not rules:
        print("No valid JSON files found in the directory.")
        return

    settings = read_settings_file(SETTINGS_FILE)
    if not settings:
        print("Error reading settings.json. Managed rules block will be skipped.")
        return

    managed_rules_block = generate_managed_rules_block(settings)
    custom_rules_blocks = generate_custom_rules_blocks(rules)
    write_to_main_tf(OUTPUT_FILE, settings, managed_rules_block, custom_rules_blocks)
    print(f"Terraform configuration written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

