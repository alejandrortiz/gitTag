#! /usr/bin/env python3
# coding: utf-8

# Author: Alex Ortiz

import os
import sys

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

    if len(repo.tags) == 0:
        console_error('No version found')
        exit_wrong()

    latest_version = repo.tags[len(repo.tags) - 1]

    repo.delete_tag(latest_version)
    repo.remote().push()

    console_success('Tag <{}> delete'.format(latest_version))

    sys.exit(0)


def exit_wrong():
    console_log('Exiting...')
    sys.exit(1)


def draw_banner() -> None:
    banner = "________________________________________________________________\n"
    banner += "  _____ _ _ _______            _____       _      _             \n"
    banner += " / ____(_) |__   __|          |  __ \     | |    | |            \n"
    banner += "| |  __ _| |_ | | __ _  __ _  | |  | | ___| | ___| |_ ___ _ __  \n"
    banner += "| | |_ | | __|| |/ _` |/ _` | | |  | |/ _ \ |/ _ \ __/ _ \ '__| \n"
    banner += "| |__| | | |_ | | (_| | (_| | | |__| |  __/ |  __/ ||  __/ |    \n"
    banner += " \_____|_|\__||_|\__,_|\__, | |_____/ \___|_|\___|\__\___|_|    \n"
    banner += "                        __/ |                                   \n"
    banner += "                       |___/                                    \n"
    banner += bg_colors.WARNING + "                                            (Owner Alex Ortiz)\n" + bg_colors.ENDC
    banner += "_______________________________________________________________\n"

    print(banner)


def console_log(message: str) -> None:
    print(bg_colors.OKBLUE + LOG_MESSAGE_STRUCT.format(message) + bg_colors.ENDC)


def console_error(message: str) -> None:
    print(bg_colors.FAIL + LOG_MESSAGE_STRUCT.format(message) + bg_colors.ENDC)


def console_success(message: str) -> None:
    print(bg_colors.OKGREEN + LOG_MESSAGE_STRUCT.format(message) + bg_colors.ENDC)


if __name__ == "__main__":
    BASE_DIR = os.getcwd()

    main()
