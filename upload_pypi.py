#!/usr/bin/env python3
"""ENTRO-CORE PyPI Upload - v0.1.0"""

import requests
import hashlib
import os
import glob
import subprocess

TOKEN = "pypi-AgEIcHlwaS5vcmcCJGI0ZjlkMjEzLTc4N2ItNDM5NS1hMTE4LTMzM2RmYWJiYjZiYQACKlszLCJlZjQ3ZDllOS04YmU5LTQ2OWMtYWQ0OC0wODRhZTg4YzZjMTUiXQAABiDHQVpBbpufka2NU1d1qNlGwRmnTZuJe0N9IbbTd9F2XQ"

print("=" * 60)
print("🔴 ENTRO-CORE v0.1.0 - PyPI Upload")
print("=" * 60)

# 1. تحديث pyproject.toml
with open("pyproject.toml", "w") as f:
    f.write('''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "entro-core"
version = "0.1.0"
description = "ENTRO-CORE: Regime-Dependent Entropy-Augmented Control for Dynamical Systems"
authors = [{name = "Samir Baladi", email = "gitdeeper@gmail.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.8"

dependencies = []

[project.urls]
Homepage = "https://entro-core.netlify.app"
Repository = "https://github.com/gitdeeper10/entro-core"
DOI = "https://doi.org/10.5281/zenodo.19431029"

[tool.setuptools]
packages = ["entro_core"]

[tool.setuptools.packages.find]
where = ["."]
include = ["entro_core*"]
exclude = ["paper*", "figures*", "Netlify*", "notebooks*", "simulation*", "tests*", "docs*"]
''')

print("✅ pyproject.toml configured")

# 2. إنشاء ملف __init__.py
os.makedirs("entro_core", exist_ok=True)
with open("entro_core/__init__.py", "w") as f:
    f.write('''"""
ENTRO-CORE: Regime-Dependent Entropy-Augmented Control
E-LAB-03 | DOI: 10.5281/zenodo.19431029
"""

__version__ = "0.1.0"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"
__license__ = "MIT"

ENTRO_CORE_DOI = "10.5281/zenodo.19431029"
''')

print("✅ entro_core/__init__.py created")

# 3. بناء الحزمة
print("\n📦 Building package...")
subprocess.run(["rm", "-rf", "dist", "build", "*.egg-info"], capture_output=True)
result = subprocess.run(["python", "-m", "build"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
    exit(1)

# 4. رفع الملفات
wheel_files = glob.glob("dist/*.whl")
tar_files = glob.glob("dist/*.tar.gz")

for filepath in wheel_files + tar_files:
    filename = os.path.basename(filepath)
    print(f"\n📤 Uploading: {filename}")

    with open(filepath, "rb") as f:
        content = f.read()
    md5_hash = hashlib.md5(content).hexdigest()
    sha256_hash = hashlib.sha256(content).hexdigest()

    data = {
        ":action": "file_upload",
        "metadata_version": "2.1",
        "name": "entro-core",
        "version": "0.1.0",
        "filetype": "bdist_wheel" if filename.endswith(".whl") else "sdist",
        "pyversion": "py3" if filename.endswith(".whl") else "source",
        "md5_digest": md5_hash,
        "sha256_digest": sha256_hash,
    }

    with open(filepath, "rb") as f:
        response = requests.post(
            "https://upload.pypi.org/legacy/",
            files={"content": (filename, f, "application/octet-stream")},
            data=data,
            auth=("__token__", TOKEN),
            timeout=60,
        )

    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Success!")
    else:
        print(f"   ❌ Error: {response.text[:200]}")

print("\n" + "=" * 60)
print("🔗 https://pypi.org/project/entro-core/0.1.0/")
print("=" * 60)
