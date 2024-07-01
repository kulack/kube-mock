# Summary

Simple python server applications built into stand alone containers which
can be configured in simple ways to serve as a mock for TCP/IP providing services.

Implements echo servers using HTTP/HTTPS and TCP

# Build

You will have to set set environment variables as needed
for your deployment. The build.bash script is designed to be run from the root of the repository.

* VERSION: version/tag of the container (also pushes "latest")
* HUB_USER: docker hub username
* HUB_PASS: docker hub password
* HUB_REPO: docker hub repository name

```
pip -m venv tools.venv
. ./tools.venv/bin/activate
pip install -r requirements.txt

./build.bash

# For Web HTTP or HTTPS application:

docker run --env PORT=80 --env SECURE=no -p 8181:80 -it kube-mock-web:latest
OR
docker run --env PORT=443 --env SECURE=yes -p 8181:443 -it kube-mock-web:latest

# For TCP application:

docker run -p 3197:3197 -it kube-mock-tcp:latest
```

# Testing

```
pip -m venv tools.venv
. ./tools.venv/bin/activate
pip install -r requirements.txt

fastapi run --reload --host 0.0.0.0 --port 8181
OR
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8181 --ssl-keyfile=dev-key.pem --ssl-certfile=dev-cert.pem
```

## Verification

### Verify HTTP/HTTPS with httpie:

Or curl (not shown).

```
➜ https --verify=no localhost:8181/ws/v1/devices/inventory query=="a=2" size==2 cursor==cursor
HTTP/1.1 200 OK

{
    "api": "/ws/v1/devices/inventory",
    "headers": {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
...snip...
```

#### Verify HTTPs with openssl:

```
➜ echo "" | openssl s_client -connect localhost:8181
Connecting to 127.0.0.1
CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 C=US, ST=Minnesota, L=Hopkins, O=Digi International, OU=Remote Manager, CN=dev team, emailAddress=cloud.operations@digi.com
verify error:num=18:self-signed certificate
...snip...
```

#### Verify TCP with socat:

```
➜ echo "Hello" | socat STDIO TCP:localhost:3197
Hello
```

# HTTPS / Secure

We are using a self-signed certificate for HTTPS. The certificate is generated from
the private key and csr in the root directory. Nothing special about the certificate
other than it is self-signed and the private key is used no-where else, feel free to 
replace it with your own certificate.

For example:

```
➜ openssl genrsa -out dev-key.pem 2048
➜ openssl req -new -key dev-key.pem -out dev-csr.pem
# Answer the questions
➜ openssl x509 -req -in dev-csr.pem -signkey dev-key.pem -out dev-cert.pem -days 10000
```
