# Loewe_TV_API
A module for controlling Loewe TVs


Disclaimer this is at the moment a proof of concept im still working on it and i am not a programmer just trying
to integrate my TV in to homeassistant so this is a start 

its also only syncronus at this time its wil become async but is just want the first basic control covert
and to uderstand how the soap protocol works because the documention of the loewe remote api is very unclear if u dont know anything about soap
there a two pdf's included one is the orginal API manual and the second one is an OCR scanned
version to make it searchable there are alot of Erors in that one

What work at this time =

- Requesting acces nothing more then getting a clientid to be used in other commands
- Getting general data about the device this data is is not yet parsed tho
    - fcid ****
    - ClientId LRemoteClient-**************
    - Chassis SL210
    - SW-Version 10.2.4.55
    - MAC-Address 00:09:82:**:**:**
    - MAC-Address-LAN 00:09:82:**:**:**
    - MAC-Address-WLAN f8:35:dd:1f:58:aa
    - Location Netherlands
- Power Control
- Set/Get Mute
- Set/Get Volume
- Send Remote control Commands
- Open a URL in the browser of the tv
- Display a message in the UP-RIGHT corner of the Tv

  As i said is al a work in progress the bare minimum is here
  for anyone who's intrested te help be my guest
  or anyone has comments about how i can improve my programmins or things that i should have done difrent please let me know
  


