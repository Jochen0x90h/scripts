import subprocess
import sys
from pathlib import Path
import fnmatch

# Set git author and email in all matching subdirectories
# example: $ python setAuthor.py * "Foo Bar" foo.bar@baz.com

def set_author(match, author, email):
    current_dir = Path.cwd()
    #print(f"Directory: {current_dir}")
    #print(f"Author: {author}")
    #print(f"Email: {email}")

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
            subprocess.run(["git", "config", "user.name", author], cwd=repo_dir, check=True)
            subprocess.run(["git", "config", "user.email", email], cwd=repo_dir, check=True)
        except subprocess.CalledProcessError as e:
            # catch error (e.g. branch does not exist or uncommitted changes)
            print(f"   ❌ Error setting author '{author}':")
            print(f"      {e.stderr.strip()}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python setUser.py <match> <author> <email>")
        sys.exit(1)
    set_author(sys.argv[1], sys.argv[2], sys.argv[3])
