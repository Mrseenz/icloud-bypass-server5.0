import json
import re
import sys

def parse_php_array(php_content):
    product_map = {}
    array_content_match = re.search(r'\$productNames\s*=\s*array\s*\((.*?)\)\s*;', php_content, re.DOTALL | re.IGNORECASE)
    if array_content_match:
        array_str = array_content_match.group(1)
        entry_regex = r"['\"]([^'\"]+)['\"]\s*=>\s*['\"]([^'\"]+)['\"](?:,\s*)?"
        for match in re.finditer(entry_regex, array_str):
            identifier = match.group(1)
            name = match.group(2)
            product_map[identifier] = name
    return product_map

def main():
    if len(sys.argv) != 3:
        print("Usage: python merge_product_types_v2.py \"<php_file_content_string>\" \"<json_data_string>\"", file=sys.stderr)
        sys.exit(1)

    php_file_content_str = sys.argv[1]
    json_data_str = sys.argv[2]

    existing_devices = parse_php_array(php_file_content_str)
    new_devices = json.loads(json_data_str)

    for identifier, name in new_devices.items():
        if identifier not in existing_devices:
            existing_devices[identifier] = name

    output_lines = []
    output_lines.append("<?php")
    output_lines.append("$productNames = array(")

    sorted_keys = sorted(existing_devices.keys())
    for i, key in enumerate(sorted_keys):
        php_key = key.replace("'", "\\'")
        php_value = existing_devices[key].replace("'", "\\'")
        # Add trailing comma for all entries, including the last one
        output_lines.append(f"\t'{php_key}' => '{php_value}',")

    output_lines.append(");")
    output_lines.append("?>")

    print("\n".join(output_lines))

if __name__ == '__main__':
    main()
