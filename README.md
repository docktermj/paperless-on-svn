# paperless-on-svn

## Synopsis

Copy files from a Subversion directory that have been modified since a Subversion revision number.

## Use

1. Clone this repository to `~/github.com/docktermj/paperless-on-svn`.

1. Create a Python virtual environment.

    ```console
    cd ~/github.com/docktermj/paperless-on-svn
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install --requirement requirements.txt
    deactivate
    ```

1. Configure `svn_change`.
    1. Copy [svn_changes.json] to `~/.config/svn_changes.json`
    1. Edit `~/.config/svn_changes.json`
        1. `svnRepositories`: A list of Subversion repositories to process.
            1. `inputPath`: The Subversion directory to read.
               No changes will be made to this directory.
            1. `outputPath`: Modified files are copied to this directory.
               The subdirectories of `outputPath` will mirror the `inputPath` structure.
            1. `include`: A list of file extension wildcards that will be copied from non-excluded directories.
            1. `exclude`: A list of subdirectories that will not be copied.
            1. `revision`: Latest Subversion revision number processed in the repository.
               This value is modified by `svn_changes.py`.
               Set to `0` to process all revisions.

1. Run [svn_changes.py] using `python3` in virtual environment.

    ```console
    ~/github.com/docktermj/paperless-on-svn/.venv/bin/python3  ~/github.com/docktermj/paperless-on-svn/svn_changes.py
    ```

    For additional options, run `svn_changes.py --help`

1. Set up `cron` job.
    1. Edit crontab

        ```console
        crontab -e
        ```

    1. :pencil2: Add the following line to the crontab.
       This example is for 7:00a every day.

        ```console
        0 7 * * * /home/dockter/github.com/docktermj/paperless-on-svn/.venv/bin/python /home/dockter/github.com/docktermj/paperless-on-svn/svn_changes.py --config /home/dockter/.config/svn_changes.json
        ```

1. Running `paperless-ngx` docker-compose formation.

    ```console
    docker compose --file /home/dockter/github.com/docktermj/paperless-on-svn/docker-compose.yaml up --detach
    ```

    1. References:
        1. [Use Docker Compose]

[svn_changes.json]: svn_changes.json
[svn_changes.py]: svn_changes.py
[Use Docker Compose]: https://docs.paperless-ngx.com/setup/#docker
