#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License: GPLv3

import os
from subprocess import call
import random
import logging
import subprocess

backup_dir = os.path.expanduser('~/github_backup')
soft = 'github-backup'
git = 'git'

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
steam_handler = logging.StreamHandler()
logger.addHandler(steam_handler)

class Repository():
    """
    Class to gather repository's parameters

    :param name: account or specific repo name
    """

    def __init__(self, name):
        self.name = name

        if name.find('/') == -1:
            self.account = True
            self.path = name
        else:
            self.account = False
            (self.path, self.folder) = name.split('/')
            self.url = 'https://github.com/' + name + '.git'

    def is_account(self):
        """
        return true if it's an account, false otherwise.
        :return: bool
        """
        if self.account:
            return True
        return False


def run(repos):
    """
    Run the backup
    """
    random.shuffle(repos)
    for repo in repos:
        logger.info('Check out: ' + str(repo.name))
        backup_path = os.path.join(backup_dir, repo.name)
        if os.path.isdir(backup_path):
            logger.debug('dir exist')
        else:
            logger.info('First clone for ' + str(repo.name))
            os.makedirs(backup_path, exist_ok=True)
            if repo.is_account():
                # soft will clone the repos
                pass
            else:
                os.chdir(os.path.join(backup_dir, repo.path))
                command = [git, 'clone', repo.url, repo.folder]
                process = subprocess.Popen(command, bufsize=4096, stdout=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if stderr:
                    logger.warning(stderr)
                if stdout:
                    logger.debug(stdout)
        if repo.is_account():
            os.chdir(backup_dir)
            logger.debug(soft + ' ' + repo.name)
            command = [soft, repo.name]
            process = subprocess.Popen(command, bufsize=4096, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.warning(stderr)
            if stdout:
                logger.debug(stdout)
        else:
            os.chdir(backup_path)
            command = [soft,]
            logger.debug(soft)
            process = subprocess.Popen(command, bufsize=4096, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.warning(stderr)
            if stdout:
                logger.debug(stdout)


if __name__ == '__main__':
    repos = [
             Repository('sciunto'),
             ]

    run(repos)
