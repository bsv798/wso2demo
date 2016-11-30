#!/usr/bin/python

import xml.etree.ElementTree as XET
import os.path
import shutil

def setPortOffset(carbonPath, offset):
    carbonNamespace = {'cns':'http://wso2.org/projects/carbon/carbon.xml'}
    carbonXmlPath = os.path.join(carbonPath, 'repository/conf/carbon.xml')
    
    root = XET.parse(carbonXmlPath)
    
    root.find('./cns:Ports/cns:Offset', carbonNamespace).text = str(offset)
    
    root.write(carbonXmlPath)

def setMasterDatasource(carbonPath, connUrl, driverClass, user, password):
    carbonXmlPath = os.path.join(carbonPath, 'repository/conf/datasources/master-datasources.xml')
    
    root = XET.parse(carbonXmlPath)
    
    element = root.find('./datasources//datasource[name="WSO2_CARBON_DB"]/definition/configuration')
    element.find('./url').text = connUrl
    element.find('./driverClassName').text = driverClass
    element.find('./username').text = user
    element.find('./password').text = password
 
    root.write(carbonXmlPath)

def copyJdbcDriverFromLocalMavenRepo(carbonPath, groupId, artifactId, version):
    jarName = artifactId + '-' + version + '.jar'
    mavenJarPath = os.path.join(os.path.expanduser('~'), '.m2/repository', groupId.replace('.', '/'), artifactId, version, jarName);
    carbonJarPath = os.path.join(carbonPath, 'repository/components/lib', jarName)
    
    if (not os.path.isfile(carbonJarPath)):
        shutil.copy(mavenJarPath, carbonJarPath)

def setIsAsLdapUserStore(carbonPath, isHost, isPortOffset):
    carbonXmlPath = os.path.join(carbonPath, 'repository/conf/user-mgt.xml')
    stringXml = _readFileToString(carbonXmlPath)
    stringXml = _uncommentXmlTag(stringXml, '<!--UserStoreManager class="org.wso2.carbon.user.core.ldap.ReadOnlyLDAPUserStoreManager">', '<UserStoreManager class="org.wso2.carbon.user.core.ldap.ReadOnlyLDAPUserStoreManager">', '</UserStoreManager-->', '</UserStoreManager>')
    
    root = XET.ElementTree(XET.fromstring(stringXml))
    
    element = root.find('./Realm/UserStoreManager[@class="org.wso2.carbon.user.core.jdbc.JDBCUserStoreManager"]')
    if (not element is None):
        root.find('./Realm').remove(element)
        
    element = root.find('./Realm/UserStoreManager[@class="org.wso2.carbon.user.core.ldap.ReadOnlyLDAPUserStoreManager"]/Property[@name="ConnectionURL"]')
    element.text = 'ldap://' + isHost + ':' + str(isPortOffset + 10389)
    
    root.write(carbonXmlPath)

def setSsoUsingIs(carbonPath, providerId, isHost, isPortOffset, providerHost, providerPortOffset):
    carbonNamespace = {'cns':'http://wso2.org/projects/carbon/authenticators.xml'}
    carbonXmlPath = os.path.join(carbonPath, 'repository/conf/security/authenticators.xml')
    
    root = XET.parse(carbonXmlPath)
    
    element = root.find('./cns:Authenticator[@name="SAML2SSOAuthenticator"]', carbonNamespace)
    element.attrib['disabled'] = 'false'
    element = root.find('./cns:Authenticator[@name="SAML2SSOAuthenticator"]/cns:Config/cns:Parameter[@name="ServiceProviderID"]', carbonNamespace)
    element.text = providerId
    element = root.find('./cns:Authenticator[@name="SAML2SSOAuthenticator"]/cns:Config/cns:Parameter[@name="IdentityProviderSSOServiceURL"]', carbonNamespace)
    element.text = 'https://' + isHost + ':' + str(isPortOffset + 9443) + '/samlsso'
    element = root.find('./cns:Authenticator[@name="SAML2SSOAuthenticator"]/cns:Config/cns:Parameter[@name="AssertionConsumerServiceURL"]', carbonNamespace)
    element.text = 'https://' + providerHost + ':' + str(providerPortOffset + 9443) + '/acs'
    
    root.write(carbonXmlPath)

def addServiceProvider(carbonPath, providerId, providerHost, providerPortOffset):
    carbonXmlPath = os.path.join(carbonPath, 'repository/conf/identity/sso-idp-config.xml')
    acsUrl = 'https://' + providerHost + ':' + str(providerPortOffset + 9443) + '/acs'
    
    newElement = XET.Element('ServiceProvider')
    XET.SubElement(newElement, 'Issuer').text = providerId
    child = XET.SubElement(newElement, 'AssertionConsumerServiceURLs')
    XET.SubElement(child, 'AssertionConsumerServiceURL').text = acsUrl
    XET.SubElement(newElement, 'DefaultAssertionConsumerServiceURL').text = acsUrl
    XET.SubElement(newElement, 'SignResponse').text = 'true'
    XET.SubElement(newElement, 'EnableSingleLogout').text = 'true'
    
    root = XET.parse(carbonXmlPath)
    element = root.find('./ServiceProviders/ServiceProvider[Issuer="' + providerId + '"]')
    if (element is None):
        root.find('./ServiceProviders').append(newElement)
    
    root.write(carbonXmlPath)

def _readFileToString(path):
    with open(path) as file:
        return file.read()

def _uncommentXmlTag(stringXml, startComment, startTag, endComment, endTag):
    newStringXml = stringXml
    startCommentIdx = stringXml.find(startComment)
    endCommentIdx = stringXml.find(endComment, startCommentIdx + 1)
    
    if (startCommentIdx > -1 and endCommentIdx > -1):
        newStringXml = newStringXml[:endCommentIdx] + endTag + newStringXml[endCommentIdx + len(endComment):]
        newStringXml = newStringXml[:startCommentIdx] + startTag + newStringXml[startCommentIdx + len(startComment):]
        
    return newStringXml
