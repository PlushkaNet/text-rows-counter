#!/usr/bin/env python3
"""
Quick test script to verify TRC functionality works correctly.
"""

import os
import tempfile
from trc import scan_file, scan_dir

def test_functionality():
    """Test the main functionality of TRC."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        file1_path = os.path.join(temp_dir, "test1.txt")
        file2_path = os.path.join(temp_dir, "test2.txt")
        
        with open(file1_path, 'w') as f:
            f.write("Line 1\nLine 2\nLine 3\n")
            
        with open(file2_path, 'w') as f:
            f.write("Line 1\nLine 2\n")
            
        # Test file scanning
        lines1 = scan_file(file1_path)
        lines2 = scan_file(file2_path)
        
        print(f"File 1 has {lines1} lines")
        print(f"File 2 has {lines2} lines")
        
        # Test directory scanning
        total_lines = scan_dir(temp_dir, recursive=False)
        print(f"Total lines in directory: {total_lines}")
        
        # Verify results
        assert lines1 == 3, f"Expected 3 lines in file1, got {lines1}"
        assert lines2 == 2, f"Expected 2 lines in file2, got {lines2}"
        assert total_lines == 5, f"Expected 5 total lines, got {total_lines}"
        
        print("All tests passed!")

if __name__ == "__main__":
    test_functionality()