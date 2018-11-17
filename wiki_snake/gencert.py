# Wiki Snake - Wiki Monkey's database server
# Copyright (C) 2018 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Wiki Snake.
#
# Wiki Snake is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wiki Snake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wiki Snake.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import subprocess
import argparse
import xdg.BaseDirectory

datadir = xdg.BaseDirectory.save_data_path('wiki-monkey')

# TODO: Remind in documentation that the ssl_key and ssl_cert options must be
#       updated in the configuration file, and the certificate must be stored
#       in the browser

argparser = argparse.ArgumentParser(
    description="wiki-snake - Wiki Monkey database server - Generate SSL certificate",
    add_help=True,
)

argparser.add_argument('--path', metavar='PATH', action='store',
                       default=os.path.join(datadir, 'db.sqlite'),
                       help='the path to the SQLite database file '
                       '(default: %(default)s)')

if __name__ == "__main__":
    cliargs = argparser.parse_args()

    KEY = 'wiki-monkey-key.pem'
    CSR = 'wiki-monkey.csr'
    CERT = 'wiki-monkey-cert.pem'

    for args in (
        ('openssl', 'genrsa', '-out', KEY, '2048'),
        ('openssl', 'req', '-new', '-key', KEY, '-out', CSR),
        ('openssl', 'x509', '-req', '-in', CSR, '-signkey', KEY, '-out', CERT),
    ):
        subprocess.run(args, cwd=cliargs.path)

    os.remove(os.path.join(cliargs.path, CSR))
