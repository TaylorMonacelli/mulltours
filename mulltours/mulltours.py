import argparse
import logging
import os
import pathlib
import sys

import cookiecutter.main
from clinepunk import clinepunk

from mulltours import git


def git_setup(path):
    if not git.git_found_ok():
        sys.exit(-1)

    if not git.git_init(path):
        sys.exit(-1)

    if not git.git_init_branch(path):
        sys.exit(-1)

    if not git.git_add_all(path):
        sys.exit(-1)

    if not git.git_commit(path):
        sys.exit(-1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "basedir",
        nargs="?",
        default=".",
        help="create project_name in basedir so it results in basedir/project_name",
    )
    parser.add_argument(
        "--project",
        nargs="?",
        default=None,
        help="choose specific name instead of random",
    )

    args = parser.parse_args()

    name = "".join(clinepunk.get_words(count=2)) if not args.project else args.project
    path = pathlib.Path(args.basedir) / name

    url = "https://github.com/audreyr/cookiecutter-pypackage.git"
    logging.debug(f"creating project {name} from template {url}")
    os.chdir(args.basedir)
    cookiecutter.main.cookiecutter(
        url,
        extra_context={"project_name": name},
        no_input=True,
    )

    # commit boilerplate
    os.chdir(path)
    git_setup(path)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{pathlib.Path(__file__).stem}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    main()
