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
try:
    # Running a proper WSGI server is recommended in production environments
    # https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.run
    from gunicorn.app.base import BaseApplication as GunicornApplication
except ImportError:
    GunicornApplication = None

VERSION = '5.5.2'  # TODO Extract the version from setup.py or something

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

    if cliargs.proxy_url:
        conf.upgrade({'proxy_url': cliargs.proxy_url})

    if cliargs.origins:
        # BUG: Requiring to separate the origins with spaces isn't the safest
        #      way to handle lists of values...
        conf.upgrade({'origins': ' '.join(cliargs.origins)})

    if cliargs.ssl_cert:
        conf.upgrade({'ssl_cert': cliargs.ssl_cert})

    if cliargs.ssl_key:
        conf.upgrade({'ssl_key': cliargs.ssl_key})

    if cliargs.workers:
        conf.upgrade({'workers': str(cliargs.workers)})

    if cliargs.force_development_server:
        conf.upgrade({
            'force_development_server': str(cliargs.force_development_server)})

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

    if not conf.get_bool('force_development_server') and GunicornApplication:
        run_gunicorn(cliargs)
    else:
        run_flask(cliargs)


def run_gunicorn(cliargs):
    # Running a proper WSGI server is recommended in production environments
    # https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.run
    class Application(GunicornApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    Application(app, dict(
        bind='{}:{}'.format(conf['host'], conf.get_int('port')),
        workers=conf.get_int('workers'),
        keyfile=conf['ssl_key'] or None,
        certfile=conf['ssl_cert'] or None,
        loglevel='debug' if cliargs.debug else 'info',
    )).run()


def run_flask(cliargs):
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
        'init_env': str(cliargs.init_env),
        'revise': str(cliargs.revise),
        'migrate': str(cliargs.migrate),
    })

    models, api, static = _pre_run(False)

    if conf.get_bool('init_env'):
        models.init_migrations()
    elif conf.get_bool('revise'):
        models.create_revision()
    elif conf.get_bool('migrate'):
        models.create_migration()
    else:
        raise ValueError("Unspecified maintenance command")
