#! /usr/bin/env python3

import fnmatch
import json
import os
import shutil
import sys

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

    errors = []
    for svn_path in svn_paths:
        files_copied = 0
        files_excluded = 0

        # Read configuration for a repository.

        repository_path_fragment = svn_path.get("path")
        previous_revision = svn_path.get("revision", 0)
        exclude_fragments = svn_path.get("exclude", [])
        repository_path = os.path.join(input_path, repository_path_fragment)

        # Make globs to identify files to exclude.

        excludes = []
        for exclude_fragment in exclude_fragments:
            excludes.append(f"{repository_path}/{exclude_fragment}")

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

            # Determine if file should be excluded from copying.

            is_excluded = False
            for exclude in excludes:
                if fnmatch.fnmatch(path, exclude):
                    is_excluded = True
            if is_excluded:
                files_excluded += 1
                continue

            # If path was not excluded and is a file, copy it.

            match item:
                case "added":
                    match kind:
                        case "file":
                            files_copied += 1
                            copy_file(input_path, output_path, path)
                        case "dir":
                            continue
                        case _:
                            errors.append(f"Unknown kind: {svn_path}.{diff}.{kind}")
                case _:
                    errors.append(f"Unknown item: {svn_path}.{diff}.{item}")

        print(
            f"From {repository_path}, {files_copied} copied;  {files_excluded} excluded."
        )

    # If there were errors, exit early.

    if len(errors) > 0:
        print("There were errors: {errors}")
        sys.exit(1)

    # Write configuration file with updated revisions.

    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)
