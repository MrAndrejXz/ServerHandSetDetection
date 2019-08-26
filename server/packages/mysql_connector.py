"""Module for work with MySQL"""

import logging

import mysql.connector


class ClientMysql(object):
    def __init__(self, host, port, auth_plugin, user, passwd, database, table):
        """

        :param host: host MySQL server
        :param port: port MySQL server
        :param auth_plugin: auth plugin for MySQL server (example: mysql_native_password)
        :param user: login for authorization
        :param passwd: passwd for authorization
        :param database: name database
        """
        self.host = host
        self.port = port
        logging.basicConfig(level=logging.INFO)
        try:
            logging.info(msg="Try connect to MySQL database {}:{}".format(host, port))
            self.db = mysql.connector.connect(
                host=host,
                port=port,
                auth_plugin=auth_plugin,
                user=user,
                passwd=passwd,
                database=database,
            )
            self.table = table
            logging.info(msg="Successful connect to database")
        except Exception as ex:
            logging.error(msg="Error while connect to database, {}".format(ex))
            exit(1)

    def add_record(self, user_data):
        """
        Add test data to table test
        :return:
        """
        try:
            logging.info(msg="Try to add record in table")
            cursor = self.db.cursor()
            sql = (
                "INSERT INTO {}(uuid, date, remote_ip, user_agent, accept, accept_encoding, accept_language) "
                " VALUES (%s, %s, %s, %s, %s, %s, %s)".format(self.table)
            )
            val = [
                (
                    user_data.uuid,
                    user_data.date,
                    user_data.remote_ip,
                    user_data.user_agent,
                    user_data.accept,
                    user_data.accept_encoding,
                    user_data.accept_language,
                )
            ]
            cursor.executemany(sql, val)
            self.db.commit()
            logging.info("Successful add record")
        except Exception as ex:
            logging.error(msg="Error while added record, {}".format(ex))
            exit(1)

    def connected_status(self):
        return self.db.is_connected()

