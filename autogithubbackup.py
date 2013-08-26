#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License: GPLv3

import os
from subprocess import call
import random
import logging, logging.handlers
import subprocess

backup_dir = os.path.expanduser('~/github_backup')
soft = 'github-backup'
git = 'git'

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
#steam_handler = logging.StreamHandler()
#logger.addHandler(steam_handler)
backup_log_dir = os.path.expanduser('~/log')
if not os.path.isdir(backup_log_dir):
    os.makedirs(backup_log_dir)
LOG_PATH = os.path.join(backup_log_dir, 'backup.log')
log_rotator = logging.handlers.TimedRotatingFileHandler(LOG_PATH,
                                                        when='midnight',
                                                        interval=1,
                                                        backupCount=30,
                                                        encoding=None,
                                                        delay=False,
                                                        utc=False)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
log_rotator.setFormatter(formatter)
logger.addHandler(log_rotator)



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
    logger.debug('The script starts')
    random.shuffle(repos)
    for repo in repos:
        logger.info('Check out: ' + str(repo.name))
        backup_path = os.path.join(backup_dir, repo.name)
        if os.path.isdir(backup_path):
            logger.debug('dir already exists')
        else:
            logger.info('First clone for ' + str(repo.name))
            os.makedirs(backup_path, exist_ok=True)
            if repo.is_account():
                logger.debug('Repository is an account')
                # soft will clone the repos
                pass
            else:
                os.chdir(os.path.join(backup_dir, repo.path))
                command = [git, 'clone', repo.url, repo.folder]
                logger.debug('Command: %s' % command)
                process = subprocess.Popen(command, bufsize=4096, stdout=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if stderr:
                    logger.warning(stderr.decode('utf8'))
                if stdout:
                    logger.info(stdout.decode('utf8'))
        if repo.is_account():
            os.chdir(backup_dir)
            logger.debug(soft + ' ' + repo.name)
            command = [soft, repo.name]
            logger.debug('Command: %s' % command)
            process = subprocess.Popen(command, bufsize=4096, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.warning(stderr.decode('utf8'))
            if stdout:
                logger.info(stdout.decode('utf8'))
        else:
            os.chdir(backup_path)
            command = [soft,]
            logger.debug('Command: %s' % command)
            process = subprocess.Popen(command, bufsize=4096, stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.warning(stderr.decode('utf8'))
            if stdout:
                logger.info(stdout.decode('utf8'))

    logger.debug('The script ends')

if __name__ == '__main__':
    repos = [
             Repository('sciunto'),
             ]

    run(repos)
