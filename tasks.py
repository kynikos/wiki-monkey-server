import os.path
from invoke import task, run

AUXDIR = './auxiliary/'
TEST_CONFIG = './auxiliary/test.conf'
TEST_DB = './auxiliary/test-database.sqlite'


@task
def gencert(ctx):
    """
    Generate the certificate to serve the app from localhost.
    """
    run('python3 -m wiki_monkey.gencert --path {}'.format(AUXDIR),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def init(ctx):
    """
    Initialize the development environment.
    """
    run('python3 -m wiki_monkey.aux --init-env --db-path {}'.format(TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def revise(ctx):
    """
    Create an empty database-migration revision script.
    """
    run('python3 -m wiki_monkey.aux --revise --db-path {}'.format(TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def migrate(ctx):
    """
    Create an automatic database-migration revision script.
    """
    run('python3 -m wiki_monkey.aux --migrate --db-path {}'.format(TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)


@task
def serve(ctx):
    """
    Serve the database on localhost.
    """
    run('python3 -m wiki_monkey.main --conf {} --db-path {} --debug'.format(
        TEST_CONFIG, TEST_DB),
        # http://www.pyinvoke.org/faq.html#calling-python-or-python-scripts-prints-all-the-output-at-the-end-of-the-run
        pty=True)
