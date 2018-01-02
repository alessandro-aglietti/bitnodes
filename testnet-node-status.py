#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import socket
import sys
from binascii import unhexlify

from protocol import (
    Connection,
    ConnectionError,
    ProtocolError,
)

CONF = {
    'user_agent': '/bitnodes.earn.com:0.1/',
    'logfile': 'log/testnet-node-status.log',
    # see Know magic values https://en.bitcoin.it/wiki/Protocol_documentation#Message_structure
    'testnet3_magicnumber': unhexlify("0b110907")
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
        user_agent=CONF['user_agent'],
        magic_number=CONF['testnet3_magicnumber'],
    )
    try:
        logging.debug("Connecting to %s", conn.to_addr)
        conn.open()
        handshake_msgs = conn.handshake()
        logging.debug("handshake_msgs {}".format(handshake_msgs))

        logging.debug("ULTIMO BLOCCO RILEVATO https://www.blocktrail.com/tBTC/block/{}".format(handshake_msgs[0]['height']))
        logging.debug("VERSIONE {} {}".format(handshake_msgs[0]['user_agent'], handshake_msgs[0]['version']))

        addr_msgs = conn.getaddr()
        logging.debug("addr_msgs {}".format(addr_msgs))

    except (ProtocolError, ConnectionError, socket.error) as err:
        logging.error("%s: %s", conn.to_addr, err)
    finally:
        conn.close()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
