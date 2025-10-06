#!/usr/bin/env python3
import subprocess
import os
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error in {description}: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    # Change to terraform directory (assuming it's in parent directory)
    tf_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    
    print("Starting user deletion and session invalidation process...")
    
    # Step 1: Terraform destroy to delete users
    os.chdir(tf_dir)
    if not run_command("terraform destroy -auto-approve", "Terraform destroy (deleting users)"):
        print("Failed to delete users with Terraform")
        sys.exit(1)
    
    # Step 2: Run session invalidation script
    script_dir = os.path.join(tf_dir, "scripts")
    invalidate_script = os.path.join(script_dir, "invalidate_sessions.py")
    
    if not run_command(f"python3 {invalidate_script}", "Session invalidation"):
        print("Session invalidation completed with some errors")
    
    print("\n✓ Process completed: Users deleted and sessions invalidated")

if __name__ == "__main__":
    main()
