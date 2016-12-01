# wso2demo
WSO2 demo using ESB, DSS, IS with guaranteed delivery

## Initial setup

- download postgresql jdbc driver to local maven repository using command
`mvn org.apache.maven.plugins:maven-dependency-plugin:2.10:get -Dartifact=org.postgresql:postgresql:9.4.1212`
- download and unzip latest versions of wso2 esb, dss, is
- run python configuration scripts 'dss.py', 'esb.py' and 'is.py' from 'script' folder. All scripts should be run with one argument - a path pointing to 'carbon.home' of appropriate server
- start wso2 servers. First run should be done with option -Dsetup
- check sso is working. Log in to any server. After than other servers shoul not request authentication

## Configuration scripts

Simple python scripts that modify wso2 configuratin xml files. They are doing:
- set port offsets for servers running on one machine
- change master datasource to postgresql database
- set servers to use ldap authentication
- set single sign on across servers
