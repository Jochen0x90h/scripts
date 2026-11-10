import subprocess
import sys
from pathlib import Path
import fnmatch

# Remove a version in all matching subdirectories
# example: $ python conanRemove.py foo* 0.2.0-beta

def conan_remove(match, version):
    current_dir = Path.cwd()
    #print(f"Directory: {current_dir}")

    # get matching subdirectories (not recursive)
    target_dirs = [
        d for d in current_dir.iterdir() if d.is_dir() and fnmatch.fnmatch(d.name, match)
    ]

    if not target_dirs:
        print(f"No directories found matching '{match}'.")
        return

    for repo_dir in target_dirs:
        name = repo_dir.name
        print(f"📁 {name}")

        try:
            subprocess.run(f"conan remove -c {name}/{version}", cwd=repo_dir)

        except subprocess.CalledProcessError as e:
            # catch error (e.g. branch does not exist or uncommitted changes)
            print(f"   ❌ Error removing '{name}/{version}':")
            print(f"      {e.stderr.strip()}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python conanRemove.py <match> <version>")
        sys.exit(1)
    conan_remove(sys.argv[1], sys.argv[2])
