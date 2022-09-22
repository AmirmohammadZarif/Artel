#!/usr/bin/env python3

import sys
import evdev
import pprint

print('All devices:')
for name in evdev.list_devices():
    print(name)
print()

print('This device')
dev1 = evdev.device.InputDevice(sys.argv[1])
caps = dev1.capabilities(True, True)
pprint.pprint(caps)


ff_key = None
ff_modes = []
for k, v in caps.items():
    if k[0] == 'EV_FF':
        ff_key = k[1]
        ff_modes = v
        break

print(ff_key)
pprint.pprint(ff_modes)

rumb_id = None
gain_id = None
for i in ff_modes:
    if i[0] == 'FF_RUMBLE' or 'FF_RUMBLE' in i[0]:
        rumb_id = i[1]
    if i[0] == 'FF_GAIN' or 'FF_GAIN' in i[0]:
        gain_id = i[1]

print('Rumble:', rumb_id)
print('Gain:', gain_id)

#gain = evdev.ff.Gain()
rumble = evdev.ff.Rumble()
