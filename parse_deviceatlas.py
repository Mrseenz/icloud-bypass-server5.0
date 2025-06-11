import json
import re
import sys

def parse_device_atlas_data(text_content):
    device_map = {}
    lines = text_content.splitlines()
    data_lines = []

    # Try to find the precise start and end markers from the prompt
    start_marker_found = False
    block_captured = False
    for line_idx, line_content in enumerate(lines):
        if "iPhone 16e iPhone17,5 2025" in line_content: # Start marker
            start_marker_found = True
            # The data includes this line, so start from here
            for data_line_idx in range(line_idx, len(lines)):
                current_data_line = lines[data_line_idx]
                data_lines.append(current_data_line)
                if "iPhone iPhone1,1 2007" in current_data_line: # End marker
                    block_captured = True
                    break
            if block_captured: # Block captured
                break

    if not block_captured:
        # Fallback to a more generic table start if specific markers fail
        data_lines = [] # Reset
        table_header_found = False
        for line in lines:
            if "Model Model Identifiers Year Released" in line:
                table_header_found = True
                continue # Skip the header line itself
            if table_header_found:
                if not line.strip(): # Stop if an empty line is encountered after header
                    break
                # Add lines that seem to contain device info
                # This is a loose filter, primary parsing logic is below
                if re.search(r'(iPhone|iPad)\d*,\d*', line):
                     data_lines.append(line)
                elif line.startswith("iPhone") or line.startswith("iPad"): # Broader match
                     data_lines.append(line)


    current_model_name = ""
    for raw_line in data_lines:
        # Pre-process line: remove "Primary Hardware Type", "Without Client-side", "With Client-side" columns
        # These columns often contain generic terms like "iPhone" or "iPad" that can confuse parsing if not handled.
        # The main target is "Model" and "Model Identifiers" and "Year" to help structure.

        # Remove from "Primary Hardware Type" (often "Mobile Phone" or "Tablet") onwards
        line = re.sub(r'\s+(Mobile Phone|Tablet)\s+.*', '', raw_line)
        line = line.strip()

        if not line or "Model Model Identifiers Year Released" in line:
            continue

        # Regex to capture:
        # 1. Model Name (anything before identifiers)
        # 2. Identifiers (one or more, space separated)
        # 3. Optional Year (to help distinguish identifiers from other text)
        # This regex is greedy for model name, then looks for identifiers.
        match = re.match(r'^(.*?)\s+((?:(?:iPhone|iPad|ipad|iphone)\d{1,2},\d{1,2}\s*)+)(?:\s+\d{4})?', line)

        if match:
            model_name_full = match.group(1).strip()
            identifiers_str = match.group(2).strip()
        else:
            # Simpler match for lines like "iPhone iPhone1,1" (name is also part of identifier string)
            # or if year is missing and identifier is last significant piece of data.
            match_simple = re.match(r'^(.*?)\s+((?:iPhone|iPad|ipad|iphone)\d{1,2},\d{1,2})$', line)
            if match_simple:
                model_name_full = match_simple.group(1).strip()
                identifiers_str = match_simple.group(2).strip()
            else:
                continue # Skip lines that don't fit expected patterns

        if not model_name_full or not identifiers_str:
            continue

        # Handle model name slashes as per prompt ("iPhone 15 Pro/iPhone 16" -> "iPhone 15 Pro")
        if '/' in model_name_full:
            model_name_full = model_name_full.split('/')[0].strip()

        # Further clean model name: sometimes year or other things get stuck if regex is not perfect
        model_name_full = re.sub(r'\s+\d{4}$', '', model_name_full).strip() # Remove trailing year if any
        # Remove trailing "iPhone" or "iPad" if it got stuck to model name (from "Without client side" etc.)
        model_name_full = re.sub(r'\s+(iPhone|iPad)$', '', model_name_full, flags=re.IGNORECASE).strip()


        # Extract individual identifiers from the string of identifiers
        raw_identifiers = re.findall(r'(?:iPhone|iPad|ipad|iphone)\d{1,2},\d{1,2}', identifiers_str)

        for identifier in raw_identifiers:
            identifier_clean = identifier.strip()
            # Normalize capitalization
            if identifier_clean.lower().startswith('iphone'):
                normalized_identifier = 'iPhone' + identifier_clean[len('iphone'):]
            elif identifier_clean.lower().startswith('ipad'):
                normalized_identifier = 'iPad' + identifier_clean[len('ipad'):]
            else:
                continue

            device_map[normalized_identifier] = model_name_full

    return device_map

if __name__ == '__main__':
    # Read the entire stdin as a single string for the text content
    input_text = sys.stdin.read()
    result = parse_device_atlas_data(input_text)
    print(json.dumps(result))
