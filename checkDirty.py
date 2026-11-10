import os
import subprocess
from pathlib import Path

# Check for uncommitted changes or being behind in all subdirectories
# example: $ python checkDirty.py

def check_git_status():
    current_dir = Path.cwd()
    #print(f"Directory: {current_dir}")

    # counters
    dirty_count = 0
    repo_count = 0

    # list subdirectories (non recursive)
    subdirectories = [d for d in current_dir.iterdir() if d.is_dir()]

    if not subdirectories:
        print("No subdirectories found.")
        return

    for subdir in subdirectories:
        # check if it is a git repository
        git_dir = subdir / ".git"
        if git_dir.exists():
            repo_count += 1
            try:
                result = subprocess.run(
                    ["git", "status", "--porcelain", "--untracked-files=no"],
                    cwd=subdir,
                    capture_output=True,
                    text=True,
                    check=True
                )

                # commitable changes when output not empty
                if result.stdout.strip():
                    print(f"⚠️  {subdir.name} has uncommitted changes!")
                    # print affected files
                    # print(result.stdout)
                    dirty_count += 1
                else:
                    # check if repo is ahead of remote
                    result = subprocess.run(
                        ["git", "status", "-sb"],
                        cwd=subdir,
                        check=True,
                        capture_output=True,
                        text=True,
                    )

                    # first line contains branch information (e.g. "## main...origin/main [ahead 2]")
                    first_line = result.stdout.splitlines()[0]
                    if "[ahead" in first_line:
                        print(f"⚠️  {subdir.name} is ahead of remote!")
                    else:
                        print(f"✅ {subdir.name} is clean.")

            except subprocess.CalledProcessError as e:
                print(f"❌ Error checking {subdir.name}: {e}")
            except FileNotFoundError:
                print(f"❌ Git is not installed or not in path.")
                return

    # Zusammenfassung ausgeben
    print(f"\nResult: {dirty_count} of {repo_count} git-repositories are dirty.")

if __name__ == "__main__":
    check_git_status()
