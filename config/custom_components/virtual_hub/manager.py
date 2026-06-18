from typing import Dict


class VirtualHubManager:
    def __init__(self):
        self.power = False
        self.active_source = None
        self.playback_state = "idle"
        self.listeners = []

        self.devices: Dict = {
            "TV": {
                "power": False
            },
            "AVR": {
                "power": False,
                "volume": 25,
            },
            "Apple TV": {
                "power": False,
                "playing": False,
            },
            "Music System": {
                "power": False,
                "playing": False,
            },
            "Game Console": {
                "power": False,
                "playing": False,
            },
        }

    def play(self):
        self.playback_state = "playing"

    def pause(self):
        self.playback_state = "paused"

    def volume_up(self):
        self.devices["AVR"]["volume"] = min(
            100,
            self.devices["AVR"]["volume"] + 5,
        )

    def volume_down(self):
        self.devices["AVR"]["volume"] = max(
            0,
            self.devices["AVR"]["volume"] - 5,
        )

    def turn_on_hub(self):
        self.power = True

        self.devices["TV"]["power"] = True
        self.devices["AVR"]["power"] = True

    def turn_off_hub(self):
        self.power = False

        for device in self.devices.values():
            device["power"] = False

        self.active_source = None
        self.playback_state = "idle"

    def select_source(self, source):
        self.power = True
        self.active_source = source

        self.devices["TV"]["power"] = True
        self.devices["AVR"]["power"] = True

        for name in [
            "Apple TV",
            "Music System",
            "Game Console",
        ]:
            self.devices[name]["power"] = (
                name == source
            )

        self.play()

    def system_ready(self):
        return (
            self.devices["TV"]["power"]
            and
            self.devices["AVR"]["power"]
        )

    def playback_available(self):
        return self.devices["AVR"]["power"]