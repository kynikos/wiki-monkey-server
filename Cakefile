path = require('path')
fs = require('fs')
{spawnSync} = require('child_process')

AUXDIR = './auxiliary/'


run = (command, args..., options) ->
    return spawnSync(command, args, {
        stdio: [process.stdin, process.stdout, process.stderr]
        options...
    })


task('gencert', "generate the certificate to serve the scripts on
     localhost", (options) ->
    run('openssl', 'genrsa', '-out', 'dev-key.pem', '2048', {cwd: AUXDIR})
    run('openssl', 'req', '-new', '-key', 'dev-key.pem', '-out', 'dev.csr',
        {cwd: AUXDIR})
    run('openssl', 'x509', '-req', '-in', 'dev.csr', '-signkey', 'dev-key.pem',
        '-out', 'dev-cert.pem', {cwd: AUXDIR})
    fs.unlinkSync(path.join(AUXDIR, 'dev.csr'))
)
