import os.path
from invoke import task, run

AUXDIR = './auxiliary/'
SERVERDIR = './wiki_snake/'
PORT = 13502
TEST_DB = '../auxiliary/test-database.sqlite'


@task
def gencert(ctx):
    """
    Generate the certificate to serve the app from localhost.
    """
    run('cd {} && python3 -m gencert --path {}'.format(SERVERDIR, AUXDIR),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def init(ctx):
    """
    Initialize the development environment.
    """
    run('cd {} && python3 -m aux --init-env --db-path {}'.format(
        SERVERDIR, TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def revise(ctx):
    """
    Create an empty database-migration revision script.
    """
    run('cd {} && python3 -m aux --revise --db-path {}'.format(
        SERVERDIR, TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def migrate(ctx):
    """
    Create an automatic database-migration revision script.
    """
    run('cd {} && python3 -m aux --migrate --db-path {}'.format(
        SERVERDIR, TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def serve(ctx, port=PORT):
    """
    Serve the database on localhost.
    """
    run('cd {} && python3 -m main --port {} '
        '--origin https://wiki.archlinux.org '
        '--origin http://wiki.archlinux.org '
        '--ssl-cert {} --ssl-key {} '
        '--db-path {} '
        '--debug'.format(SERVERDIR, port,
                         os.path.join('..', AUXDIR, 'dev-cert.pem'),
                         os.path.join('..', AUXDIR, 'dev-key.pem'),
                         TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)
