# Author: Madhu Chakravarthy
# Date: 12-04-2017

import os
import json
import xmltodict
import logging

#Initialize logger
logger = logging.getLogger('appLogger')


class ReportParser(object):

    def __init__(self, fileName):

        logger.info("Initializing parsing of output.xml")
        self.fileName = fileName


    def convertXmlToJson(self):

        logger.debug("Converting xml to json")
        with open(self.fileName, "rb") as f:
            data = xmltodict.parse(f, xml_attribs=True)
            return json.dumps(data, indent=4)


    def writeJsonToFile(self, data):
        
        logger.debug("Writing to output xml to Json file")
        fileName, fileExtension = os.path.splitext(self.fileName)
        fileName = fileName + '.json' 
        with open(fileName, 'w') as outFile:
            outFile.write(data)


if __name__ == "__main__":

    import logging.config
    logging.config.fileConfig(os.path.join(os.getcwd(),'..',
                                               'config', 'logging.conf'))
    logger.info("Start xml to json test")
    reportParser = ReportParser('../reports/20170414_004546/output.xml')
    data = reportParser.convertXmlToJson()
    reportParser.writeJsonToFile(data)
    logger.info("End xml to json test")




