#! /usr/bin/env python3

import json
import os
import shutil

import svn.local

CONFIG_PATH = os.path.expanduser("~/.config/svn_changes.json")

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def copy_file(input_path, output_path, source_path):
    """Copy a file from the source repository directory to the target directory."""
    destination_path = source_path.replace(input_path, output_path)
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    shutil.copy(source_path, destination_path)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    # Read configuration file.

    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)

    input_path = os.path.expanduser(config.get("inputPath"))
    output_path = os.path.expanduser(config.get("outputPath"))
    svn_paths = config.get("svnPaths")

    # Process individual SVN repositories.

    errors = 0
    for svn_path in svn_paths:

        # Read configuration for a repository.

        path = svn_path.get("path")
        previous_revision = svn_path.get("revision")
        repository_path = os.path.join(input_path, path)

        # Query the repository for current revision.

        repository = svn.local.LocalClient(repository_path)
        info = repository.info()
        current_revision = info.get("entry_revision")
        svn_path["revision"] = (
            current_revision  # Update configuration for updating config file later.
        )

        # Determine the files that differ between the previous and current revisions.

        diffs = repository.diff_summary(previous_revision, current_revision)

        # Process the differences.

        for diff in diffs:
            item = diff.get("item")
            kind = diff.get("kind")
            path = diff.get("path")
            match item:
                case "added":
                    match kind:
                        case "file":
                            copy_file(input_path, output_path, path)
                        case "dir":
                            continue
                        case _:
                            errors += 1
                            print(f"Unknown kind: {kind}")
                case _:
                    errors += 1
                    print(f"Unknown item: {item}")

    # Write configuration file with updated revisions.

    if errors == 0:
        with open(CONFIG_PATH, "w") as file:
            json.dump(config, file, indent=4)
