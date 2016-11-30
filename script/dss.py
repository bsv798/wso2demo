#!/usr/bin/python

import sys
import wso2

carbonPath = sys.argv[1]

wso2.setPortOffset(carbonPath, 10003)
wso2.setMasterDatasource(carbonPath, 'jdbc:postgresql:wso2dss', 'org.postgresql.Driver', 'postgres', 'postgres')
wso2.copyJdbcDriverFromLocalMavenRepo(carbonPath, 'org.postgresql', 'postgresql', '9.4.1212')
wso2.setIsAsLdapUserStore(carbonPath, 'localhost', 10000)
wso2.setSsoUsingIs(carbonPath, 'dss', 'localhost', 10000, 'localhost', 10003)
