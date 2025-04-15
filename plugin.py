#           EspNow serial interface plugin for Domoticz
#
#           Author: Flying Domotic, November 8h, 2020
#
#

"""
<plugin key="EspNowSerial" name="EspNow serial plugin" author="Flying Domotic" version="1.2.1" externallink="https://github.com/FlyingDomotic/domoticz-espnowserial-plugin">
	<params>
		<param field="SerialPort" label="Serial Port" width="150px" required="true" default="/dev/serial0"/>
		<param field="Mode1" label="Devices definition (device#switchType|...)" width="400px" required="true" default="SW_1#2|PIR_1#8" />
		<param field="Mode6" label="Debug" width="100px">
			<options>
				<option label="True" value="Debug"/>
				<option label="File" value="File"/>
				<option label="None" value="Normal" default="true"/>
			</options>
		</param>
	</params>
</plugin>
"""

import Domoticz

SerialConn = None
isConnected = False
deviceDiscoveryDone = False
serialBuffer = ""

def onStart():
	# Startup code
	global SerialConn, deviceDiscoveryDone

	deviceDiscoveryDone = False

	if Parameters["Mode6"] != "Normal":
		Domoticz.Debugging(14)

	DumpConfigToLog()
	SerialConn = Domoticz.Connection(Name="EspNow", Transport="Serial", Protocol="line", Address=Parameters["SerialPort"], Baud=115200)
	SerialConn.Connect()
    # Enable heartbeat
    Domoticz.Heartbeat(30)

	return

def CreateDevices():
	# Get device list and parameters (i.e. SW_1#2|PIR_1#8)
	for deviceParam in Parameters["Mode1"].split("|"):
		deviceName = deviceParam.split("#")[0]
		deviceSubType = deviceParam.split("#")[1]

		# Create device if needed
		if (GetDevice(deviceName) == None):
			LogMessage("Creating device " + deviceName)
			Domoticz.Device(Name=deviceName, Unit=getNextDeviceId(), TypeName="Switch", Switchtype=int(deviceSubType), DeviceID=deviceName, Used=True).Create()

def getNextDeviceId():
	# Get next free device Id
	nextDeviceId = 1

	while True:
		exists = False
		for device in Devices:
			if (device == nextDeviceId) :
				exists = True
				break
		if (not exists):
			break;
		nextDeviceId = nextDeviceId + 1

	return nextDeviceId

def onConnect(Connection, Status, Description):
	# Serial connection callback
	global SerialConn, deviceDiscoveryDone

	if (Status == 0):
		LogMessage("Connected successfully to: "+Parameters["SerialPort"])
		SerialConn = Connection

		if (not deviceDiscoveryDone):
			CreateDevices()
			deviceDiscoveryDone = True

	else:
		LogMessage("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"])
		Domoticz.Debug("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"]+" with error: "+Description)
	return True

def onMessage(Connection, Data):
	# Serial message reception callback
	global isConnected, serialBuffer

	# Add message to buffer
	serialBuffer  += Data.decode("ascii")

	# Split buffer into lines
	messages = serialBuffer.split("\r")
	i = 0
	# Work with all messages
	while (i < len(messages) - 1):
		strData = messages[i]
		processMessage(strData)
		i += 1

	serialBuffer = messages[len(messages) - 1]


def processMessage(strData):
	# Process one message from EspNow gateway
	try:
		# Format is like "Event ESPNOW#9=PIR_8/Event=0"
		LogMessage("Received [{0}] ".format(strData.replace("\r", "<cr>")))
		# Extract device (PIR_8)
		deviceName = (strData.split("=")[1]).split("/")[0]
		# Extract event (Event)
		event = (strData.split("/")[1]).split("=")[0]
		# Extract value (0)
		value = strData.split("=")[2]
		# Find device into device list
		device = GetDevice(deviceName)
		if (device == None) :
			# Device not found
			Domoticz.Log("Can't find device '"+deviceName+"'")
			return
		if (event == "Event") :
			# This is an event message
			if (device.SwitchType == 8) :
				# PIR value = 0 means motion
				if (value == "0") :
				    state = 1
				else:
					state = 0
			else:
				# Other switches are not reversed
				if (value == "0") :
				    state = 0
				else:
					state = 1
			UpdateDevice(device, state) 
		if (event == "BatteryLow") :
			# This is a battery low message
			batLevel = 0
			UpdateBattery(device, batLevel) 
	except Exception as inst:
		# Something went wrong
		Domoticz.Error("Message '"+strData+"' analysis failed: '"+str(inst)+"'")

def onCommand(Unit, Command, Level, Color):
	Domoticz.Log("Unit " + str(Unit) + ": Command: '" + str(Command) + "'")

	if Unit in Devices:
		try:
			device = Devices[Unit]
			if (Command == "Off") :
				UpdateDevice(device, 0)
			if (Command == "On") :
				UpdateDevice(device, 1)
		except (ValueError, KeyError, TypeError) as e:
			Domoticz.Error("onCommand: Error: " + str(e))
	else:
		Domoticz.Debug("Device not found, ignoring command");

def onDisconnect(Connection):
	# Disconnect callback
	LogMessage("Connection '"+Connection.Name+"' disconnected.")
	return

def onHeartbeat():
	# Heart beat callback
	global isConnected, SerialConn
	if (not SerialConn.Connected()):
		isConnected = False
		SerialConn.Connect()
	return True

def GetDevice(deviceName):
	# Find a device by name in devices table
	for device in Devices:
		if (Devices[device].DeviceID == deviceName) :
			# Return device
			return Devices[device]
	# Return None if not found
	return None

def LogMessage(Message):
	# Log message
	if Parameters["Mode6"] == "File":
		# Log message to file if requested
		f = open(Parameters["HomeFolder"]+"plugin.log","a")
		f.write(Message+"\r\n")
		f.close()
	Domoticz.Debug(Message)

def DumpConfigToLog():
	# Dump parameters and devices to log
	for x in Parameters:
		if Parameters[x] != "":
			LogMessage( "'" + x + "':'" + str(Parameters[x]) + "'")
	for x in Devices:
		LogMessage("Device " + str(x) + ": " + str(Devices[x]) + ", switch type: " + str(Devices[x].SwitchType) + ", batteryLevel: " + str(Devices[x].BatteryLevel))
	return

def UpdateDevice(device, nValue):
	# Updates a device nValue
	Domoticz.Log("Set nValue="+str(nValue)+" ("+device.Name+")")
	device.Update(nValue=nValue, sValue="")
	return

def UpdateBattery(device, batLevel):
	# Updates a device battery level
	Domoticz.Log("Set BatteryLevel="+str(BatteryLevel)+" ("+device.Name+")")
	device.Update(nValue=device.nValue, sValue=device.sValue, BatteryLevel=str(BatteryLevel))
	return
