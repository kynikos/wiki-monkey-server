import os.path
from invoke import task, run

AUXDIR = './auxiliary/'
SERVERDIR = './wiki_snake/'


@task
def gencert(ctx):
    """
    Generate the certificate to serve the app from localhost.
    """
    run('cd {} && openssl genrsa -out dev-key.pem 2048'.format(AUXDIR),
        pty=True)
    run('cd {} && openssl req -new -key dev-key.pem -out dev.csr'.format(
        AUXDIR), pty=True)
    run('cd {} && openssl x509 -req -in dev.csr -signkey dev-key.pem '
        '-out dev-cert.pem'.format(AUXDIR), pty=True)
    os.remove(os.path.join(AUXDIR, 'dev.csr'))


@task
def serve(ctx, port=13502):
    """
    Serve the database on localhost.
    """
    run('cd {} && python3 -m main --port {} '
        '--origin https://wiki.archlinux.org '
        '--origin http://wiki.archlinux.org '
        '--ssl-cert {} --ssl-key {} '
        '--db-path ../../auxiliary/test-database.sqlite '
        '--debug'.format(SERVERDIR, port,
                         os.path.join('..', AUXDIR, 'dev-cert.pem'),
                         os.path.join('..', AUXDIR, 'dev-key.pem')),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)
