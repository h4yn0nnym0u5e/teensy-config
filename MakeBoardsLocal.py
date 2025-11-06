import json
import re
import argparse
import os

###################################################################
# New menu entries
menuAudio = {
    "header":
    """## Audio
# Extra menu entries to tune the behaviour of the Audio library
""",
    "entries": [
        {
            "id": "audiorate",
            "name": "Audio sample rate",
            "boards": ["teensy41", "teensy40", "teensyMM"],
            "options": [
                {"id": 44, "text": "44.1kHz",
                 "entries": ["build.flags.audiorate=44100.0f"]},
                {"id": 48, "text": "48kHz",
                 "entries": ["build.flags.audiorate=48000.0f"]},
                {"id": 96, "text": "96kHz",
                 "entries": ["build.flags.audiorate=96000.0f"]}
            ]
        },
        {
            "id": "audioblocksize",
            "name": "Audio block size",
            "boards": ["teensy41", "teensy40", "teensyMM"],
            "options": [
                {"id": "normal", "text": "128 samples (normal)",
                 "entries": ["build.flags.audioblocksize=128"]},
                {"id": 16, "text": "16 samples",
                 "entries": ["build.flags.audioblocksize=16"]},
                {"id": 256, "text": "256 samples",
                 "entries": ["build.flags.audioblocksize=256"]}
            ]
        },
        {
            "id": "USBchannelcount",
            "name": "USB channels",
            "boards": ["teensy41", "teensy40", "teensyMM"],
            "options": [
                {"id": 2, "text": 2,
                 "entries": ["build.flags.USBchannelcount=2"]
                },
                {"id": 4, "text": 4,
                 "entries": ["build.flags.USBchannelcount=4"]
                },
                {"id": 6, "text": 6,
                 "entries": ["build.flags.USBchannelcount=6"]
                },
                {"id": 8, "text": 8,
                 "entries": ["build.flags.USBchannelcount=8"]
                },
            ]
        }
    ]
}

menuGDB = {
    "header":
    """## GDB
# Extra menu entries to tune the behaviour of the TeensyDebug library
""",
    "entries": [
        {
            "id": "gdb",
            "name": "GDB",
            "boards": ["teensy41", "teensy40", "teensyMM", "teensy31", "teensy36"],
            "options": [
                {"id": "off", "text": "Off",
                 "entries": ["build.gdb=0"]},
                {"id": "serial", "text": "Take over Serial",
                 "entries": ["build.gdb=2",
                             "build.flags.optimize=-Og -g -DGDB_TAKE_OVER_SERIAL",
                             "upload.tool=gdbtool"
                             ]},
                {"id": "dual", "text": "Use Dual Serial",
                 "entries": ["build.gdb=1",
                             "build.flags.optimize=-Og -g -DGDB_DUAL_SERIAL",
                             "upload.tool=gdbtool"
                             ]},
                {"id": "manual", "text": "Manual device selection",
                 "entries": ["build.gdb=3",
                             "build.flags.optimize=-Og -g -DGDB_MANUAL_SELECTION",
                             "upload.tool=gdbtool"
                             ]},
                {"id": "compile", "text": "Just compile",
                 "entries": ["build.gdb=0",
                             "build.flags.optimize=-Og -g -DGDB_MANUAL_SELECTION",
                             "upload.tool=gdbtool"
                             ]}
            ]
        }

    ]
}

menuUSB = {
    "header":
    """## USB
# Extra menu entries for custom USB devices
""",
    "entries": [
        {
            "id": "usb",
            # "name": "commented out so no additional top-level menu item",
            "boards": ["teensy41", "teensy40", "teensyMM"],
            "options": [
                {"id": "serialmtpaudio", "text": "Serial + MTP + Audio",
                 "entries": ["build.usbtype=USB_SERIAL_MTP_AUDIO",
                             "upload_port.usbtype=USB_SERIAL_MTP_AUDIO",
                             ]},
                {"id": "mtpaudiomidi", "text": "MTP + Audio + MIDI",
                 "entries": ["build.usbtype=USB_MTP_AUDIO_MIDI",
                             "upload_port.usbtype=USB_MTP_AUDIO_MIDI",
                             "fake_serial=teensy_gateway"
                             ]},
            ]
        }

    ]
}
###################################################################

###################################################################
# New USB options - must match entries in menuUSB
#
# Note: to use SEREMU the PRODUCT_ID must have one of the
# following values: 
#   0x0482, 0x0484, 0x0485, 0x0486, 0x0488 or
#   0x04D0, 0x04D1, 0x04D2, 0x04D3, 0x04D4
# (This is undocumented at the time of writing, AFAIK)
# Of these, only 0x0484 is unused, as of Teensyduino 1.59-ish
# This is by hex inspection of teensy_gateway.exe and some testing
# Use teensy_ports.exe to observe behaviour; unrecognised PID values
# are reported as an Unknown device type, the PRODUCT_NAME is
# not shown.
USBdescExtras = {
    "USB_SERIAL_MTP_AUDIO": """
        #define VENDOR_ID        0x16C0
        #define PRODUCT_ID       0x048A
        #define MANUFACTURER_NAME    {'T','e','e','n','s','y','d','u','i','n','o'}
        #define MANUFACTURER_NAME_LEN    11
        #define PRODUCT_NAME        {'T','e','e','n','s','y',' ','M','T','P','/','A','u','d','i','o'}
        #define PRODUCT_NAME_LEN    16
        #define EP0_SIZE        64
        #define NUM_ENDPOINTS         7
        #define NUM_INTERFACE        6
        #define CDC_IAD_DESCRIPTOR    1
        #define CDC_STATUS_INTERFACE    0
        #define CDC_DATA_INTERFACE    1    // Serial
        #define CDC_ACM_ENDPOINT    2
        #define CDC_RX_ENDPOINT       3
        #define CDC_TX_ENDPOINT       3
        #define CDC_ACM_SIZE          16
        #define CDC_RX_SIZE_480       512
        #define CDC_TX_SIZE_480       512
        #define CDC_RX_SIZE_12        64
        #define CDC_TX_SIZE_12        64
        
        #define MTP_INTERFACE        2    // MTP
        #define MTP_TX_ENDPOINT      4
        #define MTP_TX_SIZE_12       64
        #define MTP_TX_SIZE_480      512
        #define MTP_RX_ENDPOINT      4
        #define MTP_RX_SIZE_12       64
        #define MTP_RX_SIZE_480      512
        #define MTP_EVENT_ENDPOINT    7
        #define MTP_EVENT_SIZE    32
        #define MTP_EVENT_INTERVAL_12    10    // 10 = 10 ms
        #define MTP_EVENT_INTERVAL_480 7    // 7 = 8 ms
        
        #define AUDIO_INTERFACE    3    // Audio (uses 3 consecutive interfaces)
        #define AUDIO_TX_ENDPOINT     5
        #define AUDIO_TX_SIZE         180
        #define AUDIO_RX_ENDPOINT     5
        #define AUDIO_RX_SIZE         180
        #define AUDIO_SYNC_ENDPOINT    6
        
        #define ENDPOINT2_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_INTERRUPT
        #define ENDPOINT3_CONFIG    ENDPOINT_RECEIVE_BULK + ENDPOINT_TRANSMIT_BULK
        #define ENDPOINT4_CONFIG    ENDPOINT_RECEIVE_BULK + ENDPOINT_TRANSMIT_BULK
        #define ENDPOINT5_CONFIG    ENDPOINT_RECEIVE_ISOCHRONOUS + ENDPOINT_TRANSMIT_ISOCHRONOUS
        #define ENDPOINT6_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_ISOCHRONOUS
        #define ENDPOINT7_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_INTERRUPT
        """,

    "USB_MTP_AUDIO_MIDI": """
        #define VENDOR_ID        0x16C0
        #define PRODUCT_ID       0x0484
        #define BCD_DEVICE		 0x0210
        #define MANUFACTURER_NAME    {'T','e','e','n','s','y','d','u','i','n','o'}
        #define MANUFACTURER_NAME_LEN    11
        #define PRODUCT_NAME        {'T','e','e','n','s','y',' ','M','T','P','/','A','u','d','i','o','/','M','I','D','I'}
        #define PRODUCT_NAME_LEN    21
        #define EP0_SIZE            64
        #define NUM_ENDPOINTS          7
        #define NUM_INTERFACE         6

        #define SEREMU_INTERFACE      0	// Serial emulation
        #define SEREMU_TX_ENDPOINT     2
        #define SEREMU_TX_SIZE          64
        #define SEREMU_TX_INTERVAL      1
        #define SEREMU_RX_ENDPOINT     2
        #define SEREMU_RX_SIZE          32
        #define SEREMU_RX_INTERVAL      2

        #define MTP_INTERFACE        1    // MTP
        #define MTP_TX_ENDPOINT       3
        #define MTP_TX_SIZE_12         64
        #define MTP_TX_SIZE_480        512
        #define MTP_RX_ENDPOINT       3
        #define MTP_RX_SIZE_12         64
        #define MTP_RX_SIZE_480        512
        #define MTP_EVENT_ENDPOINT    4
        #define MTP_EVENT_SIZE         32
        #define MTP_EVENT_INTERVAL_12  10    // 10 = 10 ms
        #define MTP_EVENT_INTERVAL_480 7    // 7 = 8 ms
        
        #define MIDI_INTERFACE       2	// MIDI
        #define MIDI_NUM_CABLES        1
        #define MIDI_TX_ENDPOINT      5
        #define MIDI_TX_SIZE_12        64
        #define MIDI_TX_SIZE_480       512
        #define MIDI_RX_ENDPOINT      5
        #define MIDI_RX_SIZE_12        64
        #define MIDI_RX_SIZE_480       512

        #define AUDIO_INTERFACE      3    // Audio (uses 3 consecutive interfaces)
        #define AUDIO_TX_ENDPOINT     6
        #define AUDIO_TX_SIZE          180
        #define AUDIO_RX_ENDPOINT     6
        #define AUDIO_RX_SIZE          180
        #define AUDIO_SYNC_ENDPOINT   7

        #define ENDPOINT2_CONFIG	ENDPOINT_RECEIVE_INTERRUPT + ENDPOINT_TRANSMIT_INTERRUPT // Serial emulation
        #define ENDPOINT3_CONFIG    ENDPOINT_RECEIVE_BULK + ENDPOINT_TRANSMIT_BULK // MTP TX/RX
        #define ENDPOINT4_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_INTERRUPT  // MTP event
        #define ENDPOINT5_CONFIG    ENDPOINT_RECEIVE_BULK + ENDPOINT_TRANSMIT_BULK // MIDI
        #define ENDPOINT6_CONFIG    ENDPOINT_RECEIVE_ISOCHRONOUS + ENDPOINT_TRANSMIT_ISOCHRONOUS // Audio TX/RX
        #define ENDPOINT7_CONFIG    ENDPOINT_RECEIVE_UNUSED + ENDPOINT_TRANSMIT_ISOCHRONOUS // Audio sync
        """
}
###################################################################

def insertUSBdescs(target,descs):
    for desc in descs:
        for entry in target['entries']:
            for option in entry['options']:
                optionEntries = option['entries']
                for optionEntry in optionEntries:
                    if optionEntry.find(desc) >= 0:
                        option['desc'] = descs[desc]
                        option['define'] = desc



insertUSBdescs(menuUSB,USBdescExtras)
menuAll = { "audio": menuAudio, "GDB": menuGDB, "USB": menuUSB}


# Convert JSON description of boards.local.txt
# into the text of the file itself, returning it
# in a string
def json2txt(d):
    s=""
    s += d["header"]
    for entry in d["entries"]:
        entryID = entry['id']
        if 'name' in entry:
            s += f"\nmenu.{entryID}={entry['name']}\n"
        for board in entry["boards"]:
            s += "\n"
            for option in entry["options"]:
                optionID = option['id']
                root = f"{board}.menu.{entryID}.{optionID}"
                s += f"{root}={option['text']}\n"
                for ee in option["entries"]:
                    s += f"{root}.{ee}\n"
        s += "\n"
    return s


# Tidy up USB descriptor defines
def descTidy(s):
#    return re.sub("^\s+","  ",s,flags=re.MULTILINE)
    s = re.sub("^\n+","//\n",s,flags=re.MULTILINE) # retain blank lines
    s = re.sub("^\\s+\n","//\n",s,flags=re.MULTILINE) # retain blank lines
    s = re.sub("^\\s+","  ",s,flags=re.MULTILINE) # indent 2 spaces
    s = re.sub("//$","",s,flags=re.MULTILINE) # remove blank retainer
    return s

# Return all USB descriptor configurations
def json2desc(d):
    s=""
    for entry in d["entries"]:
        for option in entry["options"]:
            if 'desc' in option:
                s += f"\n#elif defined({option['define']})"
                s += descTidy(option['desc'])

    if "" != s:
        s = "#if 0" + s + "\n#endif\n"
    return s

# Save output
def saveOutput(root,extn,output):
    if extn: 
        if "." != extn[0]:
            extn = "." + extn
        ffp = root + extn
    else:
        ffp = root        
    of = open(ffp, "w")
    of.write(output)
    of.close()

    if args.verbose:
        print(f"Saved {ffp}")


parser = argparse.ArgumentParser(
    description="Create modified Tools menu items for Teensyduino"
)
parser.add_argument("-l", "--load", help="load modifications from LOAD file (JSON format, as saved using --json option)")
parser.add_argument("-s", "--save", nargs='?', const='boards.local', help="save outputs to this file [default boards.local]; if omitted output is to the console")
parser.add_argument("-b", "--boards", action='store_true', help="save <SAVE>.txt")
parser.add_argument("-j", "--json", action='store_true', help="save to <SAVE>.json file for later re-load")
parser.add_argument("-e", "--extra", nargs='?', const='usb_extra.h', help="save extra USB configurations to EXTRA file [default usb_extra.h]")
parser.add_argument("-v", "--verbose", action='store_true')
args = parser.parse_args()

# Convert description of menu options into JSON or text
# Use command line options to decide where output goes
if args.load:    
    menuAll=json.load(open(args.load)) # load pre-built set of options from JSON file

root = None
if args.save:
    root = args.save
    root = re.sub("[.](json|h|txt)$", "", root) # remove file type if provided


if args.json: # create a JSON file
    output = json.dumps(menuAll,indent=2) + "\n"
    if root:
        saveOutput(root,"json",output)
    else:        
        print(output) 

if args.boards: # create the boards.local.txt file
    output = ""
    for idx in menuAll:
        output += json2txt(menuAll[idx]) + "\n"
    if root:
        saveOutput(root,"txt",output)
    else:        
        print(output)

if args.extra: # create the extras for usb_desc.h file
    output = ""
    for idx in menuAll:
        s = json2desc(menuAll[idx])
        if "" != s:
            output += s
    if root:
        saveOutput(args.extra,None,output)
    else:
        print(output)

# print(args,root)
