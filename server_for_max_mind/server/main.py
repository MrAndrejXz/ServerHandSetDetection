"""Main module"""

import json
import logging
import os

from server import Server
from mysql_connector import ClientMysql

logging.basicConfig(
    format=u"%(asctime)s\t[%(filename)s]\t%(levelname)s\t%(message)s",
    level=logging.DEBUG,
)


class ExecutionConfig:
    def __init__(self):
        try:
            with open("server/config.json", "r") as conf_file:
                logging.info("Try open config.json")
                config_data = json.load(conf_file)

            self.server_port = config_data["server"]["port"]

            self.mysql_host = config_data["mysql"]["host"]
            self.mysql_port = config_data["mysql"]["port"]
            self.mysql_auth_plugin = config_data["mysql"]["auth_plugin"]
            self.mysql_user = config_data["mysql"]["user"]
            self.mysql_password = config_data["mysql"]["password"]
            self.mysql_database = config_data["mysql"]["database"]
            self.mysql_table = config_data["mysql"]["table"]
            logging.info(json.dumps(self.__dict__, sort_keys=True, indent=4))
            logging.info("Successfully opened")
        except Exception as ex:
            logging.getLogger(__name__).error(ex)
            exit(1)


config = ExecutionConfig()
client_my_sql = ClientMysql(
    config.mysql_host,
    config.mysql_port,
    config.mysql_auth_plugin,
    config.mysql_user,
    config.mysql_password,
    config.mysql_database,
    config.mysql_table
)

if __name__ == "__main__":
    url = "0.0.0.0"
    port = config.server_port
    logging.info("Start server 0.0.0.0:{}".format(port))
    Server().run(url, port, client_my_sql)


