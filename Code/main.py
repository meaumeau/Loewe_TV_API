import requests
import xml.etree.ElementTree as xml_parse
import random
from wakeonlan import send_magic_packet
from RC import RC_DICT

print(RC_DICT.ZERO.value)


class LOEWE_API:  
                     
            def __init__(self, host, own_mac, own_device_name, REGISTER_NAME="testing"): 
                self.host = host                           # the IP Adress of the device
                self.port = "905"                          # The port of the soap endpoint
                self.soap_endpoint = "loewe_tablet_0001"   # The soap endpoint it self
                self.fcid = str(random.randrange(8000,10000))       # The fcid can be any number its use for acces request and set and get commands
                self.clientid = "?"                         # the clientid is empty at start wil be served by the device after acces request
                self.own_MAC =  own_mac    
                self.own_device_name = own_device_name
                self.reg_name = REGISTER_NAME           


            def API_CALL(self,SOAP_ACTION, BODY_DATA):
                # Basic HTTP header execpt for the SOAPaction this is importend has to be the same as THE ltv: param in the body
                HTTP_Headers = {"Host" : self.host, "Content-Type" : "application/soap+xml; charset=utf-8", "SOAPAction" : f"{SOAP_ACTION}"}
                
                # The soap header is the same in every post request 
                soap_header = f"""<SOAP-ENV:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                                    <soap:Body>
                                    <ltv:{SOAP_ACTION} xmlns:ltv="urn:loewe.de:RemoteTV:Tablet">
                                        <ltv:fcid>{self.fcid}</ltv:fcid>
                                        <ltv:ClientId>{self.clientid}</ltv:ClientId>
                                        """
                soap_end   = f"""
                                        </ltv:{SOAP_ACTION}>
                                        </soap:Body>
                                        </SOAP-ENV:Envelope>
                """
                try:
                    print(f"{soap_header}{BODY_DATA}{soap_end}")
                    response = requests.post(f"http://{self.host}:{self.port}/{self.soap_endpoint}", headers = HTTP_Headers, data=f"{soap_header}{BODY_DATA}{soap_end}")
                    #print(response.text)
                    #self.PARSE_XML(response.text)
                    return response
                    #print( CALL.text)
                
                except:
                    return "Connection error!"
                

            def PARSE_XML(self, XML_DATA):
                  for i in XML_DATA[1][0]:
                    print(i.tag[30:])
                  
                  
                  
                

            def Check_connection(self):              # Simple test for checking if the connection en right device are setup
                    CMD  = "GetDeviceData"
                    BODY_DATA   = ""
                    response = self.API_CALL(CMD, BODY_DATA)
                    if (response.status_code == 200):
                          pass
                          #print(response.text)
                    else:
                          print("Error") 
                          #print(response.text)           
                              
                          
                    

            def RequestAcces(self):              #Request an client id
                    CMD = "RequestAccess"
                    BODY_DATA   = f"""      <ltv:DeviceType>Ap</ltv:DeviceType>
				                            <ltv:DeviceName>{self.own_device_name}</ltv:DeviceName>
				                            <ltv:DeviceUUID>{self.own_MAC}</ltv:DeviceUUID>
				                            <ltv:RequesterName>{self.reg_name}</ltv:RequesterName>			                            
                                  """
                    
                    response = self.API_CALL("RequestAccess", BODY_DATA).text
                    
                    parsed = xml_parse.fromstring(response)

                    if (parsed[1][0][0].text == str(self.fcid) and "LRemoteClient" in parsed[1][0][1].text):
                          self.clientid = parsed[1][0][1].text
                          #print("granted")
           
           
           
           
            def SUBSCRIBE(self): # This stil gives an error urn NOT FOUND!
                
                  BODY_DATA = f"""
                                <env:Envelope 
                                    xmlns:SOAP="http://schemas.xmlsoap.org/soap/envelope/"            
                                    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"                                    
                                    xmlns:ltv="urn:loewe.de:RemoteTV:Tablet">                                    
                                    xmlns:wsa="http'//schemas.xmlsoap.org/ws/2004/08/addressing"                                             
                                    <env:Body>
                                        <wse:Subscribe>
                                            <wse:Delivery>
                                                <wse:NotifyTo>
                                                    <wsa:Address>
                                                        soap.udp://{"192.168.10.198"}:4023/udp-sink/{self.host}
                                                    </wsa:Address>
                                                    <wsa:ReferenceProperties>
                                                    </wsa:ReferenceProperties>
                                                </wse:NotifyTo>
                                            </wse:Delivery>
                                        </wse:Subscribe>
                                    </env:Body>
                                </env:Envelope>"""
                  response = self.API_CALL("Subscribe", BODY_DATA).text
                  print(response)
                  
            
            
            
            def Wake_up(self):             #The TV goes in deep sleep after power down WOL has to beused to get it in a network state so we can feed it commands
                  send_magic_packet('F8:35:DD:1F:58:AA')
                  
            
            
            def RC(self, BUTTON=None):
                  CMD = "InjectRCKey"
                  BODY_DATA = f"""
                                <InputEventSequence>
			                                <RCKeyEvent alphabet="l2700" value="{BUTTON}" mode="press"/>
                                            <RCKeyEvent alphabet="l2700" value="{BUTTON}" mode="delayed"/>
                                            <RCKeyEvent alphabet="l2700" value="{BUTTON}" mode="repeat"/>
                                            <RCKeyEvent alphabet="l2700" value="{BUTTON}" mode="release"/>
                                        </InputEventSequence>
                                """
                  self.API_CALL(CMD, BODY_DATA).text        

            def GET_CURRENT_STATUS(self): # This commands doe not work at the moment!
                  CMD = "GetCurrentstatus"
                  BODY_DATA = ""
                  self.API_CALL(CMD, BODY_DATA).text  

            def GET_CURRENT_PLAYBACK(self):
                  CMD = "GetCurrentPlayback"
                  BODY_DATA = ""
                  self.API_CALL(CMD, BODY_DATA).text       

            def SET_ACTION_FIELD(self, MSG, TIMEOUT):
                  CMD = "SetActionField"
                  BODY_DATA = f"""<ltv:InputText>{MSG}</ltv:InputText>
                                    <ltv:IsTimeout>{TIMEOUT}</ltv:IsTimeout>
                                    <ltv:Selectors>
                                        <ltv:Selector>OK</ltv:Selector>
                                        <ltv:Selector>Escape</ltv:Selector> 
                                    </ltv:Selectors>                                
                                """
                  self.API_CALL(CMD, BODY_DATA)   


            def GET_ACTION_FIELD(self, ID):
                  CMD = "GetActionField"
                  BODY_DATA = f"<ltv:Requestld>{str(ID)}</ltv:RequestId>"
                  self.API_CALL(CMD, BODY_DATA)       


            def GET_VOLUME(self):
                  CMD = "GetVolume"
                  BODY_DATA = ""                        
                  self.API_CALL(CMD, BODY_DATA)
                  

            def SET_VOLUME(self, VOLUME = 100000):  # Volume range is from 0 to 999999 Currently the APl discards the last 4 decimal places. 
                  CMD = "SetVolume"
                  BODY_DATA = f"<ltv:Value>{VOLUME}</ltv:Value>"
                  self.API_CALL(CMD, BODY_DATA).text 

            def ZAP_TO_BROWSER(self, URL = "http://192.168.10.4:8123"):
                  CMD = "ZapToApplication"
                  BODY_DATA = f"""<ltv:Application>browser</ltv:Application>
                                  <ltv:ContentURI>{URL}</ltv:ContentURI>                                                         
                                """
                  self.API_CALL(CMD, BODY_DATA) 
                      
                             



        
        
    
c= LOEWE_API("192.168.10.37", "40-5B-D8-87-53-6a", "homeassistant")
# print(c.fcid, c.clientid) 
c.RequestAcces()
#c.SET_VOLUME()
# print(c.fcid, c.clientid)
#c.RC(RC_DICT.TV_OFF.value)
c.GET_CURRENT_PLAYBACK()
