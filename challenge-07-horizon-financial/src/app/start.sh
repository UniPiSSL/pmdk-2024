#!/bin/bash
while [ true ]; do
    su -l ctflib -c "socat -dd TCP4-LISTEN:4242,reuseaddr,fork SYSTEM:'(cd /opt/app >/dev/null && exec /opt/app/bank-app 2>&1)',pty,echo=0,raw,iexten=0"
done;
