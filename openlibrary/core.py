import os
import sys
import yaml
import requests
import subprocess
from urllib.parse import urlparse

class openlibrary:
    def __init__(self, target):
        self.target = target
        self.local_yml = "config_temp.yml"
        self.is_remote = False

    def log(self, msg):
        print(f"[openlibrary] {msg}")

    def prepare_config(self):
        """Checks if target is a local file or a URL and prepares it."""
        if os.path.exists(self.target):
            self.log(f"Using local config: {self.target}")
            self.local_yml = self.target
            return True
        
        # Check if it looks like a URL
        parsed = urlparse(self.target)
        if parsed.scheme in ('http', 'https'):
            self.is_remote = True
            self.log(f"Downloading remote config from {self.target}...")
            try:
                r = requests.get(self.target, timeout=30)
                r.raise_for_status()
                with open(self.local_yml, 'w') as f:
                    f.write(r.text)
                return True
            except Exception as e:
                print(f"Error downloading YML: {e}")
                return False
        
        print(f"Error: '{self.target}' is neither a local file nor a valid URL.")
        return False

    def run(self):
        if not self.prepare_config():
            return

        # Parse YML
        try:
            with open(self.local_yml, 'r') as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error parsing YML: {e}")
            return
        
        codebase_url = config.get('codebase')
        if not codebase_url:
            print("Error: YML missing 'codebase' parameter.")
            return

        # Extract library name
        lib_name = codebase_url.split('/')[-1].replace('.git', '').lower()
        
        # Check and Install
        if not self.is_installed(lib_name):
            self.log(f"Library '{lib_name}' not found. Installing...")
            if not self.install_lib(codebase_url):
                print(f"Error: Failed to install {lib_name}.")
                return
        
        # Execute
        self.log(f"Running: {lib_name} {self.local_yml}")
        try:
            # subprocess.run handles the terminal command execution
            # When running the library, we ALSO pass os.environ
            # so GDAL knows where its drivers and data are
            subprocess.run(
                [sys.executable, "-m", f"{lib_name}.core", self.local_yml],
                check=True,
                env=os.environ
            )            
        except subprocess.CalledProcessError as e:
            print(f"Execution failed: {e}")
        finally:
            # Clean up the temp file only if we downloaded it
            if self.is_remote and os.path.exists(self.local_yml):
                os.remove(self.local_yml)

    def is_installed(self, name):
        import importlib.util
        return importlib.util.find_spec(name) is not None

    def install_lib(self, url):
        self.log(f"Attempting to install: {url}")
        try:
            # We use subprocess.run so we can catch the exit code
            # We pass os.environ so GDAL/PATH variables are visible to Pip
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--force-reinstall", f"git+{url}"],
                env=os.environ,
                check=True
            )
            self.log("Installation successful.")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"CRITICAL: Installation failed.")
            # This will show you exactly why it failed in the terminal
            return False
        
def main():
    if len(sys.argv) < 2:
        print("Usage: openlibrary [url_to_yml | path_to_yml]")
        sys.exit(1)
    
    bootstrapper = openlibrary(sys.argv[1])
    bootstrapper.run()