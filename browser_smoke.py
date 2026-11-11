#!/usr/bin/env python3
"""Optional browser smoke check using a real Firefox with isolated test profile."""
import json
import socket
import subprocess
import tempfile
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PORT=2857
with tempfile.TemporaryDirectory(prefix="failure-atlas-firefox-") as profile:
    Path(profile,"user.js").write_text(f'user_pref("marionette.port", {PORT});\n')
    with open(Path(profile,"firefox.log"),"w") as output:
        process=subprocess.Popen(["firefox","--headless","--no-remote","--marionette","--profile",profile],
                                 stdout=output,stderr=output)
        sock=None
        try:
            deadline=time.monotonic()+20
            while time.monotonic()<deadline:
                try:
                    sock=socket.create_connection(("127.0.0.1",PORT),timeout=1)
                    break
                except OSError:
                    time.sleep(.2)
            if not sock: raise RuntimeError("Firefox Marionette startup timeout")
            sock.settimeout(12)
            def recv():
                count=b""
                while not count.endswith(b":"):
                    byte=sock.recv(1)
                    if not byte: raise RuntimeError("Lost Marionette connection")
                    count+=byte
                total=int(count[:-1])
                result=b""
                while len(result)<total:
                    chunk=sock.recv(total-len(result))
                    if not chunk: raise RuntimeError("Lost Marionette body")
                    result+=chunk
                return json.loads(result)
            recv()
            serial=0
            def command(name,args):
                nonlocal_holder[0]+=1
                serial=nonlocal_holder[0]
                wire=json.dumps([0,serial,name,args]).encode()
                sock.sendall(str(len(wire)).encode()+b":"+wire)
                response=recv()
                assert response[0]==1 and response[1]==serial,response
                if response[2] is not None: raise RuntimeError(str(response[2]))
                return response[3]
            nonlocal_holder=[0]
            command("WebDriver:NewSession",{"capabilities":{"alwaysMatch":{"pageLoadStrategy":"normal"}}})
            command("WebDriver:Navigate",{"url":(ROOT/"index.html").as_uri()})
            def js(expression):
                return command("WebDriver:ExecuteScript",{
                    "script":expression,"args":[],"newSandbox":True,"sandbox":None,
                    "line":1,"filename":"failure-atlas-browser-smoke"})["value"]
            assert js('return document.querySelectorAll(".case-card").length')==3
            js('document.querySelector("[data-query]").click(); return true')
            assert js('return document.querySelectorAll(".match").length')>=1
            assert "Cloudflare" in js('return document.querySelector(".match").textContent')
            js('let q=document.querySelector("#query");q.value="xyzzynonmatchingword";document.querySelector("#search-form").dispatchEvent(new Event("submit",{cancelable:true}));return true')
            assert js('return document.querySelectorAll(".match").length')==0
            assert "No symptom keywords overlap" in js('return document.querySelector("#match-results").textContent')
            assert js('return document.documentElement.scrollWidth<=window.innerWidth') is True
            assert js('return document.querySelectorAll("a[href^=\'https://\']").length')==3
            print("PASS real Firefox: 3 incident cards, example searches, nonmatch handling, external source links, no horizontal overflow")
            command("WebDriver:DeleteSession",{})
        finally:
            if sock: sock.close()
            process.terminate()
            try: process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
