#!/usr/bin/env python3
"""
Validation script for eBPF Ransomware Detector
This script validates that the system is properly configured and the BPF program can be compiled.
"""

import sys
import os

def check_root():
    """Check if running as root (not required for validation)"""
    if os.getuid() == 0:
        print("✓ Running as root (optional for validation)")
        return True
    else:
        print("ℹ Not running as root (this is OK for validation)")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (requires 3.6+)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.6+)")
        return False

def check_bcc():
    """Check if BCC is available"""
    try:
        from bcc import BPF
        print("✓ BCC Python module available")
        return True
    except ImportError:
        print("✗ BCC Python module not found")
        print("  Install with: sudo apt-get install python3-bpfcc")
        return False

def check_files():
    """Check if required files exist"""
    required_files = ["detector.py", "bpf.c", "bpf.h"]
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} not found")
            all_exist = False
    
    return all_exist

def compile_bpf():
    """Try to compile the BPF program"""
    try:
        from bcc import BPF
        
        if not os.path.exists("bpf.c"):
            print("✗ bpf.c not found")
            return False
        
        print("Compiling BPF program...")
        b = BPF(src_file="bpf.c", cflags=["-Wno-macro-redefined"], debug=0)
        print("✓ BPF program compiled successfully")
        
        # Check required maps
        required_maps = ['config', 'patterns', 'threshold_patterns', 'pidstats', 'events']
        for map_name in required_maps:
            if map_name in b:
                print(f"  ✓ Map '{map_name}' found")
            else:
                print(f"  ✗ Map '{map_name}' not found")
        
        return True
    except Exception as e:
        print(f"✗ BPF compilation failed: {e}")
        return False

def main():
    """Main validation function"""
    print("=" * 60)
    print("eBPF Ransomware Detector - Validation Script")
    print("=" * 60)
    print()
    
    results = []
    
    print("1. Checking Python version...")
    results.append(check_python_version())
    print()
    
    print("2. Checking required files...")
    results.append(check_files())
    print()
    
    print("3. Checking BCC availability...")
    results.append(check_bcc())
    print()
    
    if all(results[:3]):  # Only try to compile if basic checks pass
        print("4. Compiling BPF program...")
        results.append(compile_bpf())
        print()
    else:
        print("4. Skipping BPF compilation (prerequisites not met)")
        results.append(False)
        print()
    
    print("5. Checking permissions...")
    check_root()
    print()
    
    print("=" * 60)
    if all(results):
        print("✅ All validations passed!")
        print()
        print("System is ready to run the detector:")
        print("  sudo python3 detector.py")
        return 0
    else:
        print("❌ Some validations failed")
        print()
        print("Please fix the issues above before running the detector.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

