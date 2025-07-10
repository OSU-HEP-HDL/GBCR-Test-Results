import os

def check_summary_file(file_path):
    """
    Checks the summary.txt file for mismatched Ninj and Nobs values.
    """
    mismatched_lines = []
    matched_lines = []
    total_ninj = 0
    total_nobs = 0
    try:
        with open(file_path, 'r') as file:
            # print(f"\nDebugging file: {file_path}")
            for line_num, line in enumerate(file, 1):
                # Skip header lines, empty lines, End of file lines, or lines with Ch1, Ch2, Ch8
                if (line.strip() == "" or "DAQ Lane" in line or line.startswith("End of file") or
                    line.startswith("Ch1 ") or line.startswith("Ch2 ") or line.startswith("Ch3 ") or line.startswith("Ch8 ")):
                    continue
                
                # Split the line into columns
                columns = line.split()
                # print(f"Line {line_num}: {len(columns)} columns - {columns}")
                
                # Ensure the line has enough columns to check Ninj and Nobs
                if len(columns) >= 10:
                    try:
                        # print(f"  Last two columns: {columns[-3]} | {columns[-1]}")
                        # ninj = int(columns[-3].split('/')[0])
                        # nobs = int(columns[-1].split('/')[0])
                        ninj = int(columns[-6].split('/')[0])
                        nobs = int(columns[-4].split('/')[0])
                        total_ninj += ninj
                        total_nobs += nobs
                        # print(f"  Parsed: ninj={ninj}, nobs={nobs}")
                        if ninj != nobs:
                            mismatched_lines.append(line.strip())
                            # print(f"  -> MISMATCH")
                        else:
                            matched_lines.append(line.strip())
                            # print(f"  -> MATCH")
                    except ValueError as ve:
                        print(f"  -> ValueError: {ve}")
                        continue
                else:
                    print(f"  -> Insufficient columns ({len(columns)})")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    
    return mismatched_lines, matched_lines, total_ninj, total_nobs

def traverse_directory(root_dir):
    """
    Traverses the directory structure starting from root_dir and checks all summary.txt files.
    """
    mismatched_files = {}
    matched_files = {}
    checked_files = []
    grand_total_ninj = 0
    grand_total_nobs = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "summary.txt":
                file_path = os.path.join(dirpath, filename)
                checked_files.append(file_path)
                mismatches, matches, ninj_count, nobs_count = check_summary_file(file_path)
                grand_total_ninj += ninj_count
                grand_total_nobs += nobs_count
                if mismatches:
                    mismatched_files[file_path] = mismatches
                if matches:
                    matched_files[file_path] = matches
    
    return mismatched_files, matched_files, checked_files, grand_total_ninj, grand_total_nobs

if __name__ == "__main__":
    # Replace with the root directory you want to traverse
    root_directory = "/Users/steven/Development/GBCR-Test-Results"
    
    mismatched_results, matched_results, checked_files, total_ninj, total_nobs = traverse_directory(root_directory)
    
    print(f"Total files checked: {len(checked_files)}")
    print(f"Files with matched Ninj and Nobs: {len(matched_results)}")
    print(f"Files with mismatched Ninj and Nobs: {len(mismatched_results)}")
    print(f"Total Ninj across all files: {total_ninj}")
    print(f"Total Nobs across all files: {total_nobs}")
    print(f"Total error rate across all files: {1-total_ninj/total_nobs if total_ninj > 0 else 0:.2e}")
    
    # if mismatched_results:
    #     print("\nFiles with mismatched Ninj and Nobs:")
    #     for file, lines in mismatched_results.items():
    #         print(f"\nFile: {file}")
    #         for line in lines:
    #             print(f"  {line}")
    # else:
    #     print("\nNo mismatched files found.")