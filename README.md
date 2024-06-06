# Self Hosting Solution

I have a VPS (Virtual Private Server) and I have a server at home. The goal of
this project is to host services like Syncthing, Transmission, Immich, etc on my
server at home and access it remotely.

Here are some names to make it easier to talk about:

- Astrax: the physical server at my house (does not have a static IP address).
- VPS: the server in the cloud (has a static IP address).
- Stellix: a personal computer (may or may not be on the same network as Astrax).

Astrax has services running on ports like `9091` (Transmission), `2020`
(Syncthing), `2283` (Immich), etc. I want to access these remotely, in a simple
way.

### The idea right now

1. Stellix makes a request to `https://suchicodes.com/user/astrax/syncthing/`
2. `nginx` on the VPS reverse proxies this request to port `8080` where a
   python-flask server handles the request.
3. The python-flask application authenticates the user.
4. Once authenticated, this endpoint reverse proxies to port `33333`.
5. Astrax has a reverse ssh connection listening on port `33333` (VPS) where the
   traffic is forwarded to port `80` (Astrax). (Command used: 
   `ssh -R 33333:localhost:80 -N user@suchicodes.com` run on Astrax)
6. Nginx on Astrax gets request on port `80` and reverse proxies it to the
   corresponding service.
7. Server on the corresponding port is going to reply.

(Sometimes Stellix and Astrax will be on the same network where Astrax Nginx
will be access/connected to directly.)

### Things to keep in mind

1. Multiple services run on the VPS machine therefore I need Nginx to decipher
   the domain to service mapping. 
2. Astrax has multiple services running on it therefore I need a way to map each
   of them.
3. I do not want to have multiple active SSH tunnels from Astrax to the VPS.
4. I need it to be HTTPS whenever the connection is not either within the same
   machine or within an SSH tunnel. 


### Problems I face

1. Some services have weird assumptions that they make about how they will be
   accessed - cannot assume they have a "reverse proxy mode".

2. With so many levels of proxies, I have a hard time debugging this. Redirects
   cause problems at almost each level.

3. Some services may use web sockets and the proxy would have to support that.
   Some services have file upload, their own authentication, their own TLS
   layer, etc

**CURRENT ISSUE**: Astrax's nginx works as expected when accessing locally. But
when trying to access it though the SSH tunnel it breaks down, some redirect
causes it to just redirect it to the base domain. I'm ABLE to access the website
at `suchicodes.com:33333/user/astrax/` (which is the base website on Astrax) but
I'm unable to access `suchicodes.com:33333/user/astrax/syncthing/` which just
redirects to `suchicodes.com/`.

### Files In Repository

- `python-reverse-proxy.py` -> proxy configuration for the python server running
  on the VPS.
- `astrax-nginx-config` -> proxy configuration for the NGINX on Astrax.
- `vps-nginx-config` -> proxy configuration for the NGINX on the VPS.
