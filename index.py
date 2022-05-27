#!/usr/bin/env python3
# coding=utf-8
import sys
import os

current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)
if current_dir != '':
    os.chdir(current_dir)

    # optional configuration
    target_domain = os.environ.get('TARGET_DOMAIN', 'xmovies8.pw')
    domain_dir = os.path.join(current_dir, 'target_domains', target_domain)
    if os.path.exists(domain_dir):
        sys.path.insert(0, domain_dir)

from zmirror.zmirror import app
