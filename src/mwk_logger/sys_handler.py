import datetime
import logging.handlers
import socket
import ssl
import certifi


class SysLogHandlerSSL(logging.handlers.SysLogHandler):

    def __init__(self, host='', port=0, system=None,
                 facility=logging.handlers.SysLogHandler.LOG_USER,
                 secure=True):

        if not system:
            system = socket.gethostname()
        if host and port:
            self.system = system
            self.secure = secure
            super().__init__((host, port), facility, socket.SOCK_STREAM)
        else:
            raise OSError('Host and Port must be set.')

    def createSocket(self):
        address = self.address
        socktype = self.socktype
        if socktype is None:
            socktype = socket.SOCK_STREAM
        host, port = address
        ress = socket.getaddrinfo(host, port, 0, socktype)
        if not ress:
            raise OSError("getaddrinfo returns an empty list")
        for res in ress:
            af, socktype, proto, _, sa = res
            err = sock = None
            try:
                sock = socket.socket(af, socktype, proto)
                # SSL
                # --------------------------------------------------------------------------------------------------
                if self.secure:
                    context = ssl.create_default_context(cafile=certifi.where())
                    sock = context.wrap_socket(sock, server_hostname=host)
                # --------------------------------------------------------------------------------------------------
                sock.connect(sa)
                break
            except OSError as exc:
                err = exc
                if sock is not None:
                    sock.close()
        if err is not None:
            raise err
        self.socket = sock
        self.socktype = socktype

    def emit(self, record):
        try:
            msg = self.format(record)
            if self.ident:
                msg = self.ident + msg
            if self.append_nul:
                msg += '\n'
            # rsyslog format RFC 5424
            # --------------------------------------------------------------------------------------------------
            prio = f'<{self.encodePriority(self.facility, self.mapPriority(record.levelname))}>'
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            logger = record.__dict__['name']
            ssl_tag = '@ssl' if self.secure else ''
            system = self.system + ssl_tag
            msg = prio + timestamp + ' ' + system + ' ' + logger + ' ' + msg
            msg = msg.encode('utf-8')
            # --------------------------------------------------------------------------------------------------
            if not self.socket:
                self.createSocket()

            self.socket.sendall(msg)
        except Exception:
            self.handleError(record)
