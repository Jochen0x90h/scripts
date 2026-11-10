import subprocess
import sys
from pathlib import Path
import fnmatch

# Check out a branch in all matching subdirectories
# example: $ python checkout.py foo* main

def checkout_git_branch(match, branch):
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
        # check if it is a git repository
        if not (repo_dir / ".git").exists():
            continue
        print(f"📁 {repo_dir.name}")

        try:
            # call git checkout
            result = subprocess.run(
                ["git", "checkout", branch],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            # print output
            output = result.stderr.strip() or result.stdout.strip()
            print(f"   ✅ {output}")

        except subprocess.CalledProcessError as e:
            # catch error (e.g. branch does not exist or uncommitted changes)
            print(f"   ❌ Error checking out '{branch}':")
            print(f"      {e.stderr.strip()}")

        print("-" * 40)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python checkout.py <match> <branch>")
        sys.exit(1)
    checkout_git_branch(sys.argv[1], sys.argv[2])
