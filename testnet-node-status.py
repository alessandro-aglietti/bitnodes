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
    'socket_timeout': 30,
    'protocol_version': 70015,
    'services': 0,
    'user_agent': '/bitnodes.earn.com:0.1/',
    'relay': 0,
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
    print("Log: {}, press CTRL+C to terminate..".format(CONF['logfile']))

    address = "87.10.127.99"
    port = 18333
    height = 5
    to_address = (address, int(port))
    conn = Connection(to_addr=to_address,
                      socket_timeout=CONF['socket_timeout'],
                      proxy=None,
                      protocol_version=CONF['protocol_version'],
                      from_services=CONF['services'],
                      user_agent=CONF['user_agent'],
                      height=height,
                      relay=CONF['relay'])
    try:
        logging.debug("Connecting to %s", conn.to_addr)
        conn.open()
        handshake_msgs = conn.handshake()
        print("handshake_msgs {}", handshake_msgs)

        # addr_msgs = conn.getaddr()
        # print("addr_msgs {}", addr_msgs)

        # verack = conn.verack()
        # print("verack {}", verack)

    except (ProtocolError, ConnectionError, socket.error) as err:
        logging.debug("%s: %s", conn.to_addr, err)
    finally:
        conn.close()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
