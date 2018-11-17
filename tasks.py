import os.path
from invoke import task, run

AUXDIR = './auxiliary/'
PKGDIR = './wiki_snake/'
TEST_CONFIG = '../auxiliary/test.conf'
TEST_DB = '../auxiliary/test-database.sqlite'


@task
def gencert(ctx):
    """
    Generate the certificate to serve the app from localhost.
    """
    run('cd {} && python3 -m gencert --path {}'.format(PKGDIR, AUXDIR),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def init(ctx):
    """
    Initialize the development environment.
    """
    run('cd {} && python3 -m aux --init-env --db-path {}'.format(
        PKGDIR, TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def revise(ctx):
    """
    Create an empty database-migration revision script.
    """
    run('cd {} && python3 -m aux --revise --db-path {}'.format(
        PKGDIR, TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def migrate(ctx):
    """
    Create an automatic database-migration revision script.
    """
    run('cd {} && python3 -m aux --migrate --db-path {}'.format(
        PKGDIR, TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def serve(ctx):
    """
    Serve the database on localhost.
    """
    run('cd {} && python3 -m main --conf {} --db-path {} --debug'.format(
        PKGDIR, TEST_CONFIG, TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)
