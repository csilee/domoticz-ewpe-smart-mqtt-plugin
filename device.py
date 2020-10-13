import Domoticz
import json
import math

class Device():
    def __init__(self, domoticz_devices, mqtt_base_topic, device):
        self.devices = domoticz_devices
        self.topic = mqtt_base_topic + '/' + device['mac']
        self._register(device)

    def get_first_available_unit(self):
        for i in range(1, 255):
            if i not in self.devices:
                return i

    def get_device(self, address, alias):
        device_id = address + '_' + alias

        for unit, device in self.devices.items():
            if device.DeviceID == device_id:
                return device

    def _register(self, device):
        address = device['mac']
        name = device['name'].strip()

        if self.get_device(address, 'switch') == None:
            device_id = address + '_switch'
            Domoticz.Debug('Domoticz eszköz létrehozása az eszköz be/ki kapcsolásának kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Kapcsoló', TypeName="Switch", Image=9).Create()

        if self.get_device(address, 'turbo') == None:
            device_id = address + '_turbo'
            Domoticz.Debug('Domoticz eszköz létrehozása a turbó mód kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Turbó mód', TypeName="Switch", Image=9).Create()

        if self.get_device(address, 'quiet') == None:
            device_id = address + '_quiet'
            options = {}
            options['LevelActions'] = ''
            options['LevelNames'] = '|'.join(['Off', 'Csendes 1', 'Csendes 2'])
            options['SelectorStyle'] = '1'
            Domoticz.Debug('Domoticz eszköz létrehozása a csendes mód kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Csendes mód', TypeName="Selector Switch", Options=options, Image=9).Create()
			
        if self.get_device(address, 'sleep') == None:
            device_id = address + '_sleep'
            Domoticz.Debug('Domoticz eszköz létrehozása a alvó mód kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Alvó mód', TypeName="Switch", Image=9).Create()

        if self.get_device(address, 'health') == None:
            device_id = address + '_health'
            Domoticz.Debug('Domoticz eszköz létrehozása az egészség (hideg plazma) mód kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Hideg plazma', TypeName="Switch", Image=9).Create()

        if self.get_device(address, 'economy') == None:
            device_id = address + '_economy'
            Domoticz.Debug('Domoticz eszköz létrehozása a energia takarékos mód kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Energia takarékos mód', TypeName="Switch", Image=9).Create()

        if self.get_device(address, 'display') == None:
            device_id = address + '_display'
            Domoticz.Debug('Domoticz eszköz létrehozása a kijelzők láthatóságának kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Kijelző', TypeName="Switch", Image=9).Create()

        if self.get_device(address, 'temp') == None:
            device_id = address + '_temp'
            Domoticz.Debug('Domoticz eszköz létrehozása a hőmérséklet kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Hőmérséklet', Type=242, Subtype=1).Create()

        if self.get_device(address, 'mode') == None:
            device_id = address + '_mode'
            options = {}
            options['LevelActions'] = ''
            options['LevelNames'] = '|'.join(['Automatikus', 'Hűtés', 'Szárítás', 'Keringetés', 'Fűtés'])
            options['SelectorStyle'] = '0'
            Domoticz.Debug('Domoticz eszköz létrehozása az eszköz mód kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Üzemmód', TypeName="Selector Switch", Options=options, Image=15).Create()

        if self.get_device(address, 'bladesUD') == None:
            device_id = address + '_bladesUD'
            options = {}
            options['LevelActions'] = ''
            options['LevelNames'] = '|'.join([
                'Alapértelmezett', 
                'Teljes legyezés', 
                'A legfelső helyzetben rögzítve (1/5)', 
                'Középső-fenti helyzetben rögzítve (2/5)', 
                'Középső helyzetben rögzítve (3/5)', 
                'Középső-lenti helyzetben rögzítve (4/5)',
                'Alsó helyzetben rögzítve (5/5)',
                'Legyezés a legalsó régióban(5/5)',
                'Legyezés a középső-lenti régióban(4/5)',
                'Legyezés a középső régióban (3/5)',
                'Legyezés a középső-fenti régióban (2/5)',
                'Legyezés a legfelső régióban(1/5)'
            ])
            options['SelectorStyle'] = '1'
            Domoticz.Debug('Domotikus eszköz létrehozása a lapátok függőleges helyzetének kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Lapátok függőleges', TypeName="Selector Switch", Options=options, Image=9).Create()

        if self.get_device(address, 'bladesLR') == None:
            device_id = address + '_bladesLR'
            options = {}
            options['LevelActions'] = ''
            options['LevelNames'] = '|'.join([
                'Alapértelmezett', 
                'Teljes legyezés', 
                'A legfelső helyzetben rögzítve (1/5)', 
                'Középső-fenti helyzetben rögzítve (2/5)', 
                'Középső helyzetben rögzítve (3/5)', 
                'Középső-lenti helyzetben rögzítve (4/5)',
                'Alsó helyzetben rögzítve (5/5)',
                'Legyezés a legalsó régióban(5/5)',
                'Legyezés a középső-lenti régióban(4/5)',
                'Legyezés a középső régióban (3/5)',
                'Legyezés a középső-fenti régióban (2/5)',
                'Legyezés a legfelső régióban(1/5)'
            ])
            options['SelectorStyle'] = '1'
            Domoticz.Debug('Domotikus eszköz létrehozása a lapátok vízszintes helyzetének kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Lapátok vízszintes', TypeName="Selector Switch", Options=options, Image=9).Create()

        if self.get_device(address, 'fan') == None:
            device_id = address + '_fan'
            options = {}
            options['LevelActions'] = ''
            options['LevelNames'] = '|'.join(['Autómatikus', 'Gyenge', 'Közepessen gyenge', 'Közepes', 'Közepessen erős', 'Erős'])
            options['SelectorStyle'] = '1'
            Domoticz.Debug('Domoticz eszköz létrehozása az eszköz ventilátor sebességének kezelésére')
            Domoticz.Device(Unit=self.get_first_available_unit(), DeviceID=device_id, Name=name + ' - Ventilátor sebessége', TypeName="Selector Switch", Options=options, Image=7).Create()

        self.device = device

    def _update_device(self, device_key, n_value, s_value):
        device = self.get_device(self.device['mac'], device_key)

        if (s_value == None):
            s_value = device.sValue

        if (device.nValue != n_value or device.sValue != s_value):
            device.Update(nValue=n_value, sValue=s_value)
        else:
            device.Touch()

    def _update_state(self, state):
        address = self.device['mac']
        Domoticz.Debug(json.dumps(state))

        if "Pow" in state:
            n_value = int(state['Pow'])

            self._update_device('switch', n_value, str(n_value))
            self._update_device('mode', n_value, None)
            self._update_device('fan', n_value, None)
            self._update_device('bladesUD', n_value, None)

        if "Tur" in state:
            self._update_device('turbo', int(state['Tur']), str(state['Tur']))

        if "Quiet" in state:
            n_value = self.get_device(address, 'switch').nValue
            s_value = str(state["Quiet"] * 10)
            self._update_device('quiet', n_value, s_value)
			
        if "Health" in state:
            self._update_device('health', int(state['Health']), str(state['Health']))

        if "SwhSlp" in state:
            self._update_device('sleep', int(state['SwhSlp']), str(state['SwhSlp']))

        if "Lig" in state:
            self._update_device('display', int(state['Lig']), str(state['Lig']))

        if "SvSt" in state:
            self._update_device('economy', int(state['SvSt']), str(state['SvSt']))

        if "SetTem" in state and "TemRec" in state:
            temperature = state['SetTem'] + (0.5 if state['TemRec'] == 1 else 0)
            self._update_device('temp', 0, str(temperature))

        if "Mod" in state:
            n_value = self.get_device(address, 'switch').nValue
            s_value = str(state["Mod"] * 10)
            self._update_device('mode', n_value, s_value)

        if "WdSpd" in state:
            n_value = self.get_device(address, 'switch').nValue
            s_value = str(state["WdSpd"] * 10)
            self._update_device('fan', n_value, s_value)

        if "SwUpDn" in state:
            n_value = self.get_device(address, 'switch').nValue
            s_value = str(state["SwUpDn"] * 10)
            self._update_device('bladesUD', n_value, s_value)

        if "SwingLfRig" in state:
            n_value = self.get_device(address, 'switch').nValue
            s_value = str(state["SwingLfRig"] * 10)
            self._update_device('bladesLR', n_value, s_value)

    def handle_message(self, topic, message):
        if topic == self.topic + '/status':
            self._update_state(message)

    def handle_command(self, alias, command, level, color):
        cmd = command.upper()
        commands = {}

        Domoticz.Debug('Command "' + command + ' (' + str(level) + ')" from device "' + self.device['name'] + '" alias: ' + alias)

        if alias == 'switch' and (cmd == 'ON' or cmd == 'OFF'):
            commands['Pow'] = 1 if cmd == 'ON' else 0

        if alias == 'turbo' and (cmd == 'ON' or cmd == 'OFF'):
            commands['Tur'] = 1 if cmd == 'ON' else 0

        if alias == 'quiet':
            commands['Quiet'] = level / 10
			
        if alias == 'health' and (cmd == 'ON' or cmd == 'OFF'):
            commands['Health'] = 1 if cmd == 'ON' else 0

        if alias == 'sleep' and (cmd == 'ON' or cmd == 'OFF'):
            commands['SwhSlp'] = 1 if cmd == 'ON' else 0

        if alias == 'economy' and (cmd == 'ON' or cmd == 'OFF'):
            commands['SvSt'] = 1 if cmd == 'ON' else 0

        if alias == 'display' and (cmd == 'ON' or cmd == 'OFF'):
            commands['Lig'] = 1 if cmd == 'ON' else 0

        if alias == 'temp' and cmd == 'SET LEVEL':
            commands['TemUn'] = 0
            commands['SetTem'] = math.floor(level)
            commands['TemRec'] = 1 if (level - math.floor(level)) > 0 else 0

        if alias == 'mode':
            commands['Mod'] = level / 10

        if alias == 'fan':
            commands['WdSpd'] = level / 10

        if alias == 'bladesUD':
            commands['SwUpDn'] = level / 10

        if alias == 'bladesLR':
            commands['SwingLfRig'] = level / 10

        return commands
    
