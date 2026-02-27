import site
import os
import sys

# Get the absolute path to your project root
project_root = os.path.abspath(os.path.dirname(__file__))

# Find the site-packages directory in your virtual environment
site_packages = site.getsitepackages()[0]

# Path to the .pth file we'll create
pth_file = os.path.join(site_packages, "project_root.pth")

# Write the project root path to the .pth file
with open(pth_file, "w") as f:
    f.write(project_root)

print(f"--- PATH SETUP ---")
print(f"Project root '{project_root}' added to '{site_packages}'.")
print(f"You can now run 'python tests/test_upsert.py' from the root without setting PYTHONPATH!")
