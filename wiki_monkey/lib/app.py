# Wiki Monkey's database server
# Copyright (C) 2018 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Wiki Monkey's database server.
#
# Wiki Monkey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wiki Monkey is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wiki Monkey.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os.path
import re
import json
from configfile import ConfigFile, NonExistentFileError
from flask import Flask
from flask_cors import CORS

VERSION = '5.0.0'  # TODO Extract the version from setup.py or something

# 'conf' and 'app' are assigned in run() as global variables to ease
# importing them from the subpackages without e.g. requiring to pass them as
# arguments to init functions
conf = None
app = None


def _pre_run(cors):
    # 'app' must be imported by the subpackages, so assign it globally
    global app
    app = Flask(__name__)

    if cors:
        # BUG: Requiring to separate the origins with spaces isn't the safest
        #      way to handle lists of values...
        CORS(app, origins=re.split(r'\s', conf['origins']) or ['*'])

    # 'models' must be imported *before* 'api'!!!
    from . import models, api, static

    return models, api, static


def run(default_configfile, base_conf, cliargs):
    # Only main.py supports a configuration file, so don't put the following in
    # _pre_run()

    default_clientconfigfile = base_conf['client_conf']

    try:
        # Note how the file is imported *before* importing any command-line
        # options
        base_conf.upgrade(cliargs.conf or default_configfile)
    except NonExistentFileError:
        # If a custom path was specified, don't create it automatically
        # If changing this behavior, also update the documentation, including
        # argparse's help message for the --conf option
        if cliargs.conf:
            raise
        # Note how the file is created with the default values, i.e. *before*
        # importing any command-line options
        base_conf.export_add(default_configfile)

    # 'conf' must be imported by the subpackages, so assign it globally
    global conf
    if cliargs.preset:
        # Let this raise the exception if the section doesn't exist
        conf = base_conf(cliargs.preset)
    else:
        conf = base_conf

    # Command-line options must override the configuration file
    # If changing this behavior, also update the documentation, including
    # argparse's help message for the --conf option

    if cliargs.host:
        conf.upgrade({'host': cliargs.host})

    if cliargs.port:
        conf.upgrade({'port': str(cliargs.port)})

    if cliargs.origins:
        # BUG: Requiring to separate the origins with spaces isn't the safest
        #      way to handle lists of values...
        conf.upgrade({'origins': cliargs.origins.join(' ')})

    if cliargs.ssl_cert:
        conf.upgrade({'ssl_cert': cliargs.ssl_cert})

    if cliargs.ssl_key:
        conf.upgrade({'ssl_key': cliargs.ssl_key})

    if cliargs.db_path:
        conf.upgrade({'db_path': cliargs.db_path})

    if cliargs.user_script_dir:
        conf.upgrade({'user_script_dir': cliargs.user_script_dir})

    if cliargs.client_conf:
        conf.upgrade({'client_conf': cliargs.client_conf})
    elif (conf['client_conf'] == default_clientconfigfile and
            not os.path.isfile(conf['client_conf'])):
        # Only generate the client configuration if the default path was left,
        # and the option --client-conf was not passed to the command line
        with open(conf['client_conf'], 'w') as client_json:
            # Note that the '#default' name is a convention also used in the
            # client project (Wiki Monkey)
            json.dump({'#default': {}}, client_json, indent=2)

    models, api, static = _pre_run(True)

    models.init_database()

    app.run(host=conf['host'],
            port=conf.get_int('port'),
            ssl_context=(conf['ssl_cert'], conf['ssl_key'])
            # Using ad-hoc certificates requires the pyOpenSSL library
            if conf['ssl_cert'] and conf['ssl_key'] else 'adhoc',
            # No need to support 'debug' in the configuration file
            debug=cliargs.debug)


def maintain(cliargs):
    # 'conf' must be imported by the subpackages, so assign it globally
    global conf
    conf = ConfigFile({
        'db_path': cliargs.db_path,
        'init_env': cliargs.init_env,
        'revise': cliargs.revise,
        'migrate': cliargs.migrate,
    })

    models, api, static = _pre_run(False)

    if conf['init_env']:
        models.init_migrations()
    elif conf['revise']:
        models.create_revision()
    elif conf['migrate']:
        models.create_migration()
    else:
        raise ValueError("Unspecified maintenance command")
