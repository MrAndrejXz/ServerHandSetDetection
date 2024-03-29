"""Module server"""

import logging

from bottle import *
from collections import namedtuple
from uuid import uuid4

user_data = namedtuple(
    "user_data", "uuid date remote_ip user_agent accept accept_encoding accept_language"
)


class Server(Bottle):
    """Class to run server"""

    @staticmethod
    @get("/get_uuid")
    def ads():
        """
        Save request
        """
        uuid = str(uuid4())

        user_data.uuid = uuid
        user_data.date = time.strftime("%Y-%m-%d %H:%M:%S")
        user_data.remote_ip = request.environ.get("REMOTE_ADDR")
        user_data.user_agent = request.get_header("USER_AGENT")
        user_data.accept = request.get_header("ACCEPT")
        user_data.accept_encoding = request.get_header("ACCEPT_ENCODING")
        user_data.accept_language = request.get_header("ACCEPT_LANGUAGE")

        logging.info(
            '{} "{} {} HTTP/1.1" {}'.format(
                user_data.remote_ip,
                request.method,
                request.fullpath,
                response.status_code,
            )
        )

        Server.client_my_sql.add_record(user_data)
        return '<p align="center" style="color: #000000;font-size: 35px;margin: 10%;">{uuid}</p>'.format(
            uuid=uuid
        )

    @staticmethod
    @get("/status")
    def ads():
        """
        Save request
        """

        response.status = 200

        return (
            "<pre>"
            "service.name:ServerHandSetDetection\n"
            "service.status:ok\n"
            "service.mysql.status:{mysql_status}\n"
            "service.mysql.hostname:{mysql_hostname}\n"
            "service.mysql.port:{mysql_port}\n"
            "</pre>".format(
                mysql_status=Server.client_my_sql.connected_status(),
                mysql_hostname=Server.client_my_sql.host,
                mysql_port=Server.client_my_sql.port,
            )
        )

    @staticmethod
    @error(400)
    @error(401)
    @error(402)
    @error(403)
    @error(404)
    @error(500)
    @error(501)
    @error(502)
    @error(503)
    def _error(ex):
        logging.error(
            '{} "{} {} HTTP/1.1" {}'.format(
                request.environ.get("REMOTE_ADDR"),
                request.method,
                request.fullpath,
                response.status_code,
            )
        )
        return ex.status

    def run(self, host, port, client_my_sql):
        """Run server"""
        try:
            Server.client_my_sql = client_my_sql
            run(host=host, port=port, debug=True, server="cherrypy")
        except Exception as ex:
            logging.getLogger(__name__).error(ex)

