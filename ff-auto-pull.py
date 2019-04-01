#!/usr/bin/python3

import http.server
import socketserver
import subprocess
import os
import sys
import pwd
import syslog
import time
import threading

def drop_privs(user):
    pwnam = pwd.getpwnam(user)
    if os.getgid() != pwnam.pw_gid:
        os.setgid(pwnam.pw_gid)
    if os.getuid() != pwnam.pw_uid:
        os.setuid(pwnam.pw_uid)

drop_privs("fastd")

syslog.openlog(logoption=syslog.LOG_PID | syslog.LOG_PERROR)
syslog.syslog("daemon started")

PORT = 11684

WAIT_TIME = 5

GITBASEDIR="/etc/fastd/.peers/fastd-peers-clients"

if not os.path.isdir(GITBASEDIR):
    syslog.syslog("git basedir at "+GITBASEDIR+" does not exist")
    sys.exit("missing repo basedir")

os.chdir(GITBASEDIR)

if not os.path.isdir(".git"):
    syslog.syslog("git basedir at "+GITBASEDIR+" is missing a .git subdirectory")
    sys.exit("bad repo basedir")

if len(subprocess.check_output(["git", "status", "--porcelain"])) != 0:
    syslog.syslog("git is not clean")
    sys.exit("git is not clean")

class WebhookHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        response ="ok\n".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)
        self.server.schedule_pull_from_github()

    def do_POST(self):
        # handle POST just like GET
        self.do_GET()


class WatchdogServer(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        self.timer = None
        self.lastrun = 0
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def schedule_pull_from_github(self):
        """Trigger a call to pull_from_github, but not more often than once a minute."""
        now = time.time()
        diff = now - self.lastrun
        if diff > WAIT_TIME:
            self.pull_from_github()
        else:
            if self.timer != None:
                syslog.syslog("pull from github skipped, timer is already running")
            else:
                self.timer = threading.Timer(WAIT_TIME - diff, self.pull_from_github)
                self.timer.start()
                syslog.syslog("pull from github scheduled")

    def pull_from_github(self):
        syslog.syslog("pull from github triggered")
        self.lastrun = time.time()
        self.timer = None
        try:
            old_commit = subprocess.check_output(["git", "rev-parse", "HEAD"])
            subprocess.call(["git", "pull"])
            new_commit = subprocess.check_output(["git", "rev-parse", "HEAD"])
            syslog.syslog("old commit: {}, new commit: {}".format(old_commit, new_commit))
            if old_commit != new_commit:
                self.reload()
        except Exception as e:
            syslog.syslog("git pull caused exception: {}".format(str(e)))
            raise

    def reload(self):
        syslog.syslog("triggering fastd config reload")
        for seg in range(1,10):
            fn = "/var/run/fastd/fastd.{0:02}-clients.pid".format(seg)
            subprocess.call(["pkill", "-HUP", "-F", fn])
        for fn in ["/var/run/fastd/fastd.00-clients.pid"]:
            subprocess.call(["pkill", "-USR2", "-F", fn])



Handler = WebhookHTTPRequestHandler
Handler.timeout = 10

httpd = WatchdogServer(("", PORT), Handler)

syslog.syslog("serving at port {}".format(PORT))
httpd.serve_forever()

