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

import os.path
import subprocess
import argparse
import xdg.BaseDirectory

datadir = xdg.BaseDirectory.save_data_path('wiki-monkey')
KEY = 'wiki-monkey-key.pem'
CSR = 'wiki-monkey.csr'
CERT = 'wiki-monkey-cert.pem'

# TODO: Remind in documentation that the ssl_key and ssl_cert options must be
#       updated in the configuration file, and the certificate must be stored
#       in the browser

argparser = argparse.ArgumentParser(
    description="Wiki Monkey database server - Generate SSL certificate",
    epilog="""After generating the key and the certificate, their paths must be
either passed to the command line when launching the server
(see wiki-monkey --help), or more conveniently added to the server's
configuration file (ssl_key and ssl_cert options). Moreover, since this is
a self-signed certificate, the browser will very likely refuse to connect
to the server until the certificate is manually accepted; this can be done
for example by visiting the user-script's location and following the browser's
prompts to store the certificate.""",
    add_help=True,
)

argparser.add_argument('--path', metavar='PATH', action='store',
                       default=datadir,
                       help='the path to the directory where the key and '
                       'certificate files will be saved '
                       '(default: %(default)s)')


# setuptools' Automatic Script Creation requires a main function
# https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation
def main():
    cliargs = argparser.parse_args()

    for args in (
        ('openssl', 'genrsa', '-out', KEY, '2048'),
        ('openssl', 'req', '-new', '-key', KEY, '-out', CSR),
        ('openssl', 'x509', '-req', '-in', CSR, '-signkey', KEY, '-out', CERT),
    ):
        subprocess.run(args, cwd=cliargs.path)

    os.remove(os.path.join(cliargs.path, CSR))

    print("""
The key and certificate files have been successfully created, but
their paths must be either passed to the command line when launching the server
(see wiki-monkey --help), or more conveniently added to the server's
configuration file, for example:

  ssl_key = {}
  ssl_cert = {}

Moreover, since this is a self-signed certificate, the browser will very likely
refuse to connect to the server until the certificate is manually accepted;
this can be done for example by visiting the user-script's location and
following the browser's prompts to store the certificate.
""".format(
    os.path.join(cliargs.path, KEY), os.path.join(cliargs.path, CERT)))


if __name__ == "__main__":
    main()
