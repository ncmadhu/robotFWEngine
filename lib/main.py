# Author: Madhu Chakravarthy
# Date: 12-04-2017

import os
import rabbitMQ
import ConfigParser
import logging
import logging.config

#Initialize logger

logging.config.fileConfig(os.path.join(os.getcwd(),'..', 'config', 'logging.conf'))
logger = logging.getLogger('appLogger')

class AppMain(object):
    
    def __init__(self):

        logger.info("Info Starting App")
        self.rabbitMQ = None
        self.config = self.loadConfig()
        self.framework = self.config.get('Framework', 'name')
        self.initRabbitMQConfig()

    def loadConfig(self):

        logger.debug("Loading configuration")
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.getcwd(), '..', 'config', 'config.ini'))
        logger.debug("Config Sections: " + str(config.sections()))
        return config

    def initRabbitMQConfig(self):

        logger.debug("Initializing rabbitMQ config")
        self.rabbitMQHost = self.config.get('RabbitMQ', 'host')
        self.rabbitMQPort = int(self.config.get('RabbitMQ', 'port'))
        self.rabbitMQUserName = self.config.get('RabbitMQ', 'username')
        self.rabbitMQPassword = self.config.get('RabbitMQ', 'password')
        receiveRoutingKeys = self.config.get('Framework', 'receiveRoutingKeys')
        self.rabbitMQReceiveRoutingKeys = receiveRoutingKeys.split(',')

    def connectToRabbitMQ(self):

        logger.debug("Connecting to rabbitMQ")
        self.rabbitMQ = rabbitMQ.RabbitMQ(self.rabbitMQHost,
                                 self.rabbitMQPort,
                                 self.rabbitMQUserName,
                                 self.rabbitMQPassword)
        return self.rabbitMQ

if __name__ == "__main__":

    app = AppMain()
    appRabbitMQ = app.connectToRabbitMQ()
    appRabbitMQ.connect()
    appRabbitMQ.receive('robot', 'task', app.rabbitMQReceiveRoutingKeys)
    appRabbitMQ.close()
