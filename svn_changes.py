#! /usr/bin/env python3

import argparse
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

    # Parse commandline

    parser = argparse.ArgumentParser(description="Copy Subversion revision changes.")
    parser.add_argument(
        "--config",
        type=str,
        default="~/.config/svn_changes.json",
        help="Path to configuration file.",
    )

    args = parser.parse_args()
    config_path = os.path.expanduser(args.config)

    print(config_path)
    sys.exit(0)

    # Read configuration file.

    with open(config_path, "r") as file:
        config = json.load(file)

    svn_repositories = config.get("svnRepositories")

    # Process individual SVN repositories.

    errors = []
    for svn_repository in svn_repositories:
        files_copied = 0
        files_excluded = 0

        # Read configuration for a repository.

        input_path = os.path.expanduser(svn_repository.get("inputPath"))
        output_path = os.path.expanduser(svn_repository.get("outputPath"))
        include_list = svn_repository.get("include", [])
        exclude_list = svn_repository.get("exclude", [])
        previous_revision = svn_repository.get("revision", 0)

        # Make globs to identify files to exclude.

        excludes = []
        for exclude in exclude_list:
            excludes.append(f"{input_path}/{exclude}")

        # Query the repository for current revision.

        repository = svn.local.LocalClient(input_path)
        info = repository.info()
        current_revision = info.get("entry_revision")
        svn_repository["revision"] = (
            current_revision  # Update configuration for updating config file later.
        )

        # Determine the files that differ between the previous and current revisions.

        diffs = repository.diff_summary(previous_revision, current_revision)

        # Process the differences.

        for diff in diffs:
            item = diff.get("item")
            kind = diff.get("kind")
            path = diff.get("path")

            # Determine if file should be included.

            is_included = False
            for include in include_list:
                if fnmatch.fnmatch(path.lower(), include.lower()):
                    is_included = True
            if not is_included:
                files_excluded += 1
                continue

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
                            errors.append(
                                f"Unknown kind: {svn_repository}.{diff}.{kind}"
                            )
                case _:
                    errors.append(f"Unknown item: {svn_repository}.{diff}.{item}")

        print(f"From {input_path}, {files_copied} copied;  {files_excluded} excluded.")

    # If there were errors, exit early.

    if len(errors) > 0:
        for error in errors:
            print("Error: {error}")
        sys.exit(1)

    # Write configuration file with updated revisions.

    with open(CONFIG_PATH, "w") as file:
        json.dump(config, file, indent=4)
