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

    def parseJsonData(self, data):

        logger.debug("Parsing json data")
        suiteData =  data['robot']['suite']
        suiteData = self.parseSuiteData(data['robot']['suite'])
        logger.debug("Suite data: " + json.dumps(suiteData, indent=4))

    def parseSuiteData(self, suiteData):

        logger.debug("Parsing suite data")

        data = {}
        data['source'] = suiteData['@source']
        data['name'] = suiteData['@name']
        data['latest-summary'] = {}
        data['latest-summary']['status'] = suiteData['status']['@status']
        data['latest-summary']['start-time'] = suiteData['status']['@starttime']
        data['latest-summary']['end-time'] = suiteData['status']['@endtime']
        tests = suiteData['test']
        testSummary = []
        for test in tests:
            testDetail = {}
            testDetail['name'] = test['@name']
            testDetail['status'] = test['status']['@status']
            testDetail['start-time'] =  test['status']['@starttime']
            testDetail['end-time'] =  test['status']['@endtime']
            testSummary.append(testDetail)
            testData = self.parseTestData(test, data['name'])
            logger.debug("Test data: " + json.dumps(testData, indent=4))
        data['latest-summary']['test-summary'] = testSummary

        logger.debug("Finished parsing suite data")
        return data

    def parseTestData(self, testData, suiteName):

        logger.debug("Parsing test data")

        data = {}
        data['name'] = testData['@name']
        data['Description'] = testData.get('doc', "")
        data['latest-summary'] = {}
        data['latest-summary']['executed-suite'] = suiteName
        data['latest-summary']['status'] = testData['status']['@status']
        data['latest-summary']['start-time'] = testData['status']['@endtime']
        data['latest-summary']['end-time'] = testData['status']['@starttime']
        keywords = testData['kw']
        keywordSummary = []
        for kw in keywords:
            keywordDetail = {}
            keywordDetail['name'] = kw['@name']
            keywordDetail['library'] = kw.get('@library', '')
            keywordDetail['status'] = kw['status']['@status']
            keywordDetail['start-time'] = kw['status']['@starttime']
            keywordDetail['end-time'] = kw['status']['@endtime']
            keywordSummary.append(keywordDetail)
        data['latest-summary']['keyword-summary'] = keywordSummary
        logger.debug("Finished parsing test data")
        return data

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
    reportParser = ReportParser('../reports/20170414_012800/output.xml')
    data = reportParser.convertXmlToJson()
    reportParser.writeJsonToFile(data)
    reportParser.parseJsonData(json.loads(data))
    logger.info("End xml to json test")




