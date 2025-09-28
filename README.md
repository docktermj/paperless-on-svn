# paperless-on-svn

## Use

1. [svn_changes.json]
    1. Copy [svn_changes.json] to `~/.config/svn_changes.json`
    1. Edit `~/.config/svn_changes.json`
        1. `inputPath`: (READ) subversion directory to read.
           No changes will be made to this directory
        1. `outputPath`: (WRITE) directory where changes will be copied to.
        1. `svnPaths`: subversion subdirectories under `inputPath` that provide the source files
           which may be copied to `outputPath` directory.

1. Prepare python environment.
    1. Clone this repository to `~/github.com/docktermj/paperless-on-svn`.
    1. Create python virtual environment.

        ```console
        cd ~/github.com/docktermj/paperless-on-svn
        python3 -m venv .venv
        source .venv/bin/activate
        python3 -m pip install --upgrade pip
        python3 -m pip install --requirement requirements.txt
        deactivate
        ```

1. Run [svn_changes.py] using python in virtual environment.

    ```console
    ~/github.com/docktermj/paperless-on-svn/.venv/bin/python3  ~/github.com/docktermj/paperless-on-svn/svn_changes.py
    ```

1. Setting up `cron` job
    1. Edit crontab

        ```console
        crontab -e
        ```

    1. :pencil2: Add the following line to the crontab.
       This example is for 7:00a every day.

        ```console
        0 7 * * * /home/dockter/github.com/docktermj/paperless-on-svn/.venv/bin/python /home/dockter/github.com/docktermj/paperless-on-svn/svn_changes.py
        ```

[svn_changes.json]: svn_changes.json
[svn_changes.py]: svn_changes.py
