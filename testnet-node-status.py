#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket
import sys

from protocol import (
    Connection,
    ConnectionError,
    ProtocolError,
)

CONF = {
    'user_agent': '/bitnodes.earn.com:0.1/',
    'logfile': 'log/testnet-node-status.log'
}


def main(argv):
    loglevel = logging.DEBUG
    logformat = ("[%(process)d] %(asctime)s,%(msecs)05.1f %(levelname)s "
                 "(%(funcName)s) %(message)s")
    logging.basicConfig(level=loglevel,
                        format=logformat,
                        filename=CONF['logfile'],
                        filemode='a')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter(logformat))
    logging.getLogger().addHandler(consoleHandler)
    print("Log: {}, press CTRL+C to terminate..".format(CONF['logfile']))

    address = "87.10.127.99"
    port = 18333
    to_address = (address, int(port))
    conn = Connection(
        to_addr=to_address,
        user_agent=CONF['user_agent']
    )
    try:
        logging.debug("Connecting to %s", conn.to_addr)
        conn.open()
        handshake_msgs = conn.handshake()
        logging.debug("handshake_msgs {}", handshake_msgs)

    except (ProtocolError, ConnectionError, socket.error) as err:
        logging.error("%s: %s", conn.to_addr, err)
    finally:
        conn.close()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
