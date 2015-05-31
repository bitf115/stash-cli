#!/usr/bin/env python
#  Author:      Purinda Gunasekara
#               purinda@gmail.com
#

import sys, os, stashy, yaml
from stashy import pullrequests
from clint.textui import puts, indent, colored, prompt, validators
from template import Template

# For debugging
import pprint

# Stash configuration file
CONFIG = '.pystash.yml'

# Stash client connection
client = None
template = None

def read_config():
    '''
    Read configuration from the current directory that pystash is run.
    '''
    config = None

    if os.path.isfile(os.path.join(os.getcwd(), CONFIG)):
        config = yaml.load(file(os.path.join(os.getcwd(), CONFIG)))

    return config

def stash_client(config):
    scheme   = config['scheme']
    server   = config['server']
    port     = config['port']
    username = config['username']
    password = config['password']

    client = stashy.connect(scheme + "://" + server + ":" + str(port), username, password)
    return client

def create_pr():
    title = prompt.query('Title:')
    puts('Pull-request template requires:')

    for placeholder in template.getPlaceholders():
        value = prompt.query(placeholder + ":")
        template.setPlaceholderValue(placeholder, value)

    # Get project and repository name
    project = config['project']['code']
    repo = config['project']['repo']

    # Initiate a PR
    client.projects[project].repos[repo].pull_requests.create(title, '50cd5b406da', '1996cc66fb8', str(template))

if __name__ == '__main__':
    config = read_config()
    if config:
        client   = stash_client(config['stash'])
        template = Template(config['template']['summary'])

        if (template.getPlaceholders() != None):
            create_pr()

    else:
        sys.exit(puts(colored.red('Empty configuration file ("' + CONFIG + '")')))

    # pprint.pprint(client.projects.list())