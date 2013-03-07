#!/usr/bin/env python
#
# We assume that the virtual env is activated and this repo's parent dir is the
# same as Open-Knesset one's.
#
# The script is intended to periodicly run via a cron job

import os
import sys
import urllib2
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
BASE_URL = 'http://oknesset.org'

OKNESSET_DIR = os.path.join(BASE_DIR, 'Open-Knesset')
OKSTATIC_DIR = os.path.join(BASE_DIR, 'ok-static')

sys.path.insert(0, OKNESSET_DIR)

PAGES = (
    ('/', 'index.html'),
    ('/member/194/%D7%96%D7%91%D7%95%D7%9C%D7%95%D7%9F-%D7%90%D7%95%D7%A8%D7%9C%D7%91/', 'member.html'),
    ('/party/14/', 'party.html'),
    ('/about/', 'about.html'),
)


def download_pages():
    for url, target in PAGES:
        response = urllib2.urlopen(BASE_URL + url + '?ModPagespeed=off')
        with open(target, 'w') as target_file:
            target_file.write(response.read().replace('"/static', '"static'))


def copy_less_files():
    params = [
        'rsync', '-av', 
        os.path.join(OKNESSET_DIR, 'less'),
        OKSTATIC_DIR,
    ]

    p = subprocess.Popen(params, shell=False)
    p.communicate()

        
def collect_static():
    from django.conf import settings, global_settings
    from knesset import settings as ok_settings
    from django.core.management import call_command

    settings.configure(
        global_settings,
        INSTALLED_APPS=ok_settings.INSTALLED_APPS,
        STATIC_URL=ok_settings.STATIC_URL,
        STATIC_ROOT=os.path.join(OKSTATIC_DIR, 'static'),
        STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
        STATICFILES_DIRS=ok_settings.STATICFILES_DIRS)

    call_command('collectstatic', interactive=False)


if __name__ == '__main__':
    download_pages()
    copy_less_files()
    collect_static()
