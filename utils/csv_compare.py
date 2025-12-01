import csv
import argparse
import sys
import os

def load_and_sort_csv(filename, primary_key):
    """
    Reads a CSV file, checks for the primary key, and returns a dictionary 
    mapping the primary key to the row data.
    """
    data_map = {}
    try:
        # 'utf-8-sig' is CRITICAL: it handles the invisible Byte Order Mark (BOM)
        # that Excel/Notepad often add to the start of files (\ufeffName vs Name).
        with open(filename, mode='r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # 1. Handle empty files
            if reader.fieldnames is None:
                print(f"Error: File '{filename}' appears to be empty.")
                sys.exit(1)

            # 2. Clean headers: strip whitespace (e.g., "Name " -> "Name")
            original_headers = reader.fieldnames
            reader.fieldnames = [name.strip() for name in reader.fieldnames]

            # 3. Check for Primary Key
            if primary_key not in reader.fieldnames:
                print(f"Error: Primary key '{primary_key}' not found in {filename}")
                print("\n--- Diagnostics ---")
                print(f"Expected Key: '{primary_key}'")
                print(f"Found Headers: {reader.fieldnames}")
                print(f"Raw Headers:   {[repr(h) for h in original_headers]}")
                print("-------------------")
                sys.exit(1)

            for i, row in enumerate(reader):
                # Clean keys in the row dict to match the cleaned headers
                clean_row = {k.strip(): v for k, v in row.items() if k is not None}
                
                key_value = clean_row.get(primary_key)
                
                if key_value is None:
                    continue 
                
                if key_value in data_map:
                    print(f"Warning: Duplicate key '{key_value}' found in {filename} on line {i + 2}. Overwriting.")
                
                data_map[key_value] = clean_row
                
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        sys.exit(1)
        
    return data_map

def format_row(row):
    """Helper to format a dictionary row for display."""
    if row is None:
        return "MISSING"
    return str(row)

def main():
    parser = argparse.ArgumentParser(description="Compare two CSV files sorted by a primary key.")
    parser.add_argument("file1", help="Path to the first CSV file")
    parser.add_argument("file2", help="Path to the second CSV file")
    parser.add_argument("primary_key", help="The column name to use as the primary key")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Maximum number of differences to print (default: 10)")

    args = parser.parse_args()

    # Load and Sort
    print(f"Loading {args.file1}...")
    data1 = load_and_sort_csv(args.file1, args.primary_key)
    
    print(f"Loading {args.file2}...")
    data2 = load_and_sort_csv(args.file2, args.primary_key)

    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    diff_count = 0
    print("\n--- Differences Found ---\n")

    for key in all_keys:
        if diff_count >= args.limit:
            print(f"\nLimit of {args.limit} differences reached. Stopping.")
            break

        row1 = data1.get(key)
        row2 = data2.get(key)

        if row1 != row2:
            diff_count += 1
            print(f"Key: {key}")
            
            if row1 is None:
                print(f"< {args.file1}: MISSING")
                print(f"> {args.file2}: {format_row(row2)}")
            elif row2 is None:
                print(f"< {args.file1}: {format_row(row1)}")
                print(f"> {args.file2}: MISSING")
            else:
                # Calculate diff columns
                diff_cols = [k for k in row1 if row1.get(k) != row2.get(k)]
                print(f"  Mismatch in columns: {', '.join(diff_cols)}")
                print(f"< {args.file1}: {format_row(row1)}")
                print(f"> {args.file2}: {format_row(row2)}")
            
            print("-" * 40)

    if diff_count == 0:
        print("No differences found.")
    else:
        print(f"\nTotal differences found: {diff_count}")

if __name__ == "__main__":
    main()