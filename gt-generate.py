#! /usr/bin/env python3
# coding: utf-8

# Author: Alex Ortiz

import os
import sys
import json
from typing import Optional

from git import Repo


LOG_MESSAGE_STRUCT: str = '[*] {}\n'


class bg_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main() -> None:
    draw_banner()

    if not os.path.isdir(BASE_DIR + '/.git'):
        console_error('Git has not been initialized')
        exit_wrong()

    console_log('Git has been initialized')
    repo: Repo = Repo(BASE_DIR)
    commit = repo.commit(repo.head)
    version: str = project_version()

    if version is None and input_version is not None:
        version = input_version

    if version is None:
        console_error('No version found')
        exit_wrong()

    version_formatted: str = "v{}".format(version)

    if len(repo.tags) == 0:
        latest_version = ''
    else:
        latest_version = repo.tags[len(repo.tags) - 1]

    if latest_version != '' and version_formatted == str(latest_version):
        console_error('The version <{}> already exist'.format(latest_version))
        exit_wrong()

    repo.create_tag(version_formatted, commit, 'Version {}'.format(version_formatted))
    repo.remote().push(version_formatted)

    console_success('Tag generated\n'
                    '\tVersion: {}\n'
                    '\tCommit: \n'
                    '\t\tChecksum: {} \n'
                    '\t\tAuthor: {} \n'
                    '\t\tMessage: {}'.format(version_formatted, commit.hexsha, commit.author, commit.message))

    sys.exit(0)


def exit_wrong():
    console_log('Exiting...')
    sys.exit(1)


def draw_banner() -> None:
    banner = "\n______________________________________________________________________________\n"
    banner += "  _____ _ _ _______             _____                           _\n"
    banner += " / ____(_) |__   __|           / ____|                         | |\n"
    banner += "| |  __ _| |_ | | __ _  __ _  | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __\n"
    banner += "| | |_ | | __|| |/ _` |/ _` | | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|\n"
    banner += "| |__| | | |_ | | (_| | (_| | | |__| |  __/ | | |  __/ | | (_| | || (_) | |\n"
    banner += " \_____|_|\__||_|\__,_|\__, |  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|\n"
    banner += "                        __/ |                                                 \n"
    banner += "                       |___/                                                  \n"
    banner += bg_colors.WARNING + "                                                           (Owner Alex Ortiz)\n" + bg_colors.ENDC
    banner += "______________________________________________________________________________\n"

    print(banner)


def project_version() -> Optional[str]:
    if os.path.isfile(BASE_DIR + '/composer.json'):
        return php_project_version()
    else:
        return None


def php_project_version() -> Optional[str]:
    with open(BASE_DIR + '/composer.json', 'r') as composer_file:
        composer_data: dict = json.load(composer_file)

        if 'version' in composer_data:
            return composer_data['version']
        else:
            return None


def console_log(message: str) -> None:
    print(bg_colors.OKBLUE + LOG_MESSAGE_STRUCT.format(message) + bg_colors.ENDC)


def console_error(message: str) -> None:
    print(bg_colors.FAIL + LOG_MESSAGE_STRUCT.format(message) + bg_colors.ENDC)


def console_success(message: str) -> None:
    print(bg_colors.OKGREEN + LOG_MESSAGE_STRUCT.format(message) + bg_colors.ENDC)


if __name__ == "__main__":
    BASE_DIR = os.getcwd()

    input_version: Optional[str]

    if len(sys.argv) == 2 and len(sys.argv[1].split('.')) == 3:
        input_version = sys.argv[1]

    main()
