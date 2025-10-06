#!/usr/bin/env python3
import pytest
import sys
import os

if __name__ == "__main__":
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(__file__))
    
    # Run with debug options
    exit_code = pytest.main([
        "test_infrastructure.py",
        "-v",
        "-s", 
        "--tb=long",
        "--capture=no"
    ])
    
    sys.exit(exit_code)
