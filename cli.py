#!/usr/bin/env python3

import sys
import logging
import posix_ipc


if len(sys.argv) < 2:
    logging.error("No command specified")
    exit(1)

try:
    mq = posix_ipc.MessageQueue("/pitftmanager_ipc")
    mq.block = False
except posix_ipc.PermissionsError:
    print("couldn't open message queue")
    exit(1)

command_line = " ".join(sys.argv[1:])

mq.send(command_line, timeout=10)
