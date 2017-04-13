# Author: Madhu Chakravarthy
# Date: 12-04-2017

import os
import json 
import logging
import sshConnector

#Initialize logger
logger = logging.getLogger('appLogger')

class TaskExecutor(object):

    def __init__(self):

        logger.debug("Initializing task executor")

        self.tasks = {"start": self.taskStart,
                      "stop": self.taskStop,
                      "status": self.taskStatus,
                      "addHost": self.taskAddHost}

    def taskStart(self,body):

        logger.info("Executing start")
        if body:
            data = json.loads(body)
            host = data['host']
            sshConn = sshConnector.SSHConnector(host)
            sshConn.connectToHost()
            sshConn.executeCommandInHost(data['command'])
            sshConn.closeConnectionToHost()


    def taskStop(self,body):

        logger.info("Executing stop")

    def taskStatus(self,body):

        logger.info("Executing status")

    def taskAddHost(self,body):

        logger.info("Executing task addHost")
        if body:
            data = json.loads(body)
            host = data['host']
            filePath = os.path.join(os.getcwd(),'..', 'config', host + '.json')
            with open(filePath, 'w') as outFile:
                json.dump(data, outFile, indent=4)
            logger.debug("Written " + host + " info to file " + host + ".json")


    def executeTask(self, task, body):

        logger.debug("Received task: " +  task)
        self.tasks[task](body)


if __name__ == "__main__":

    import logging.config

    logging.config.fileConfig(os.path.join(os.getcwd(),'..',
                                           'config', 'logging.conf'))
    logger = logging.getLogger('appLogger')

    logger.info("Started testing TaskExecutor")
    taskExec = TaskExecutor()
    taskExec.executeTask("addHost", json.dumps({"host": "10.0.0.3",
                                                "username": "madhu",
                                                "password": "calsoftlabs"}))
    logger.info("Finished testing TaskExecutor")

