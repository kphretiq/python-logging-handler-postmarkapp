import sys
import logging
import json 
import requests
import platform

class PMAHandler(logging.Handler):
    """
    logging handler uses postmarkapp to send email at a given log level.
    """

    def __init__(self, config):
        """
        accepts {config}
        inititializes Handler
        """
        self.config = config
        logging.Handler.__init__(self)

    def emit(self, record):
        """
        accepts record logging message object
        calls self.send for each recipient
        """
        for addr in self.config["To"]:
            try:
                self.send(addr, record)
            except(KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)

    def send(self, addr, record):
        """
        accepts
            addr string email address
            record logging message object 

        calls postmarkapp send endpoint
        """
        subject = " - ".join([record.message, platform.node()])

        textbody = json.dumps({
            "host": platform.node(),
            "time": record.asctime,
            "logger name": record.name,
            "error level": record.levelname,
            "file": record.pathname,
            "module": record.module,
            "function": record.funcName,
            "message": record.message,
                },
            indent=True
            )

        headers = {
                "X-Postmark-Server-Token": self.config["token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
                }

        data = {
                "From": self.config["From"],
                "To": addr,
                "Subject": subject,
                "TextBody": textbody,
                }

        if "ReplyTo" in self.config:
            data["ReplyTo"] = self.config["ReplyTo"]

        reply = requests.post(
                self.config["url"],
                headers=headers,
                data=json.dumps(data),
                )

        if not reply.status_code == 200:
            sys.stderr.write(reply.text + "\n")
