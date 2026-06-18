from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)

from homeassistant.components.media_player.const import (
    MediaPlayerState,
)

from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN


DEVICES = [
    "Virtual Hub",
    "TV",
    "AVR",
    "Apple TV",
    "Music System",
    "Game Console",
]


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):
    manager = hass.data[DOMAIN][entry.entry_id]["manager"]

    entities = [
        VirtualMediaPlayer(
            manager,
            device_name,
        )
        for device_name in DEVICES
    ]

    async_add_entities(
        entities,
        True,
    )


class VirtualMediaPlayer(MediaPlayerEntity):

    def __init__(
        self,
        manager,
        device_name,
    ):
        super().__init__()

        self.manager = manager
        self.device_name = device_name

        self._attr_name = device_name

        self._attr_unique_id = (
            device_name.lower()
            .replace(" ", "_")
        )

    @property
    def supported_features(self):

        features = (
            MediaPlayerEntityFeature.TURN_ON
            |
            MediaPlayerEntityFeature.TURN_OFF
        )

        if self.device_name == "Virtual Hub":
            features |= (
                MediaPlayerEntityFeature.SELECT_SOURCE
                |
                MediaPlayerEntityFeature.PLAY
                |
                MediaPlayerEntityFeature.PAUSE
            )

        if self.device_name == "AVR":
            features |= (
                MediaPlayerEntityFeature.VOLUME_SET
            )

        return features

    @property
    def device_info(self):

        return DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    self._attr_unique_id,
                )
            },
            name=self.device_name,
            manufacturer="Virtual Hub",
        )

    @property
    def state(self):

        if self.device_name == "Virtual Hub":

            return (
                MediaPlayerState.ON
                if self.manager.power
                else MediaPlayerState.OFF
            )

        device = self.manager.devices.get(
            self.device_name,
            {},
        )

        return (
            MediaPlayerState.ON
            if device.get("power")
            else MediaPlayerState.OFF
        )

    @property
    def is_on(self):

        if self.device_name == "Virtual Hub":
            return self.manager.power

        return self.manager.devices.get(
            self.device_name,
            {},
        ).get("power", False)

    async def async_turn_on(self):

        print(
            f"TURN ON CALLED: {self.device_name}"
        )

        if self.device_name == "Virtual Hub":

            self.manager.turn_on_hub()

        elif self.device_name in [
            "Apple TV",
            "Music System",
            "Game Console",
        ]:

            self.manager.select_source(
                self.device_name
            )

        else:

            self.manager.devices[
                self.device_name
            ]["power"] = True

        self.async_write_ha_state()

    async def async_turn_off(self):

        print(
            f"TURN OFF CALLED: {self.device_name}"
        )

        if self.device_name == "Virtual Hub":

            self.manager.turn_off_hub()

        else:

            self.manager.devices[
                self.device_name
            ]["power"] = False

            if (
                self.device_name
                ==
                self.manager.active_source
            ):
                self.manager.active_source = None
                self.manager.pause()

        self.async_write_ha_state()

    @property
    def extra_state_attributes(self):

        return {
            "active_source":
                self.manager.active_source,

            "system_ready":
                self.manager.system_ready(),

            "playback_state":
                self.manager.playback_state,

            "avr_volume":
                self.manager.devices["AVR"]["volume"],

            "playback_available":
                self.manager.playback_available(),

            "hub_power":
                self.manager.power,

            "device_count":
                len(
                    self.manager.devices
                ),
        }

    @property
    def source_list(self):

        if self.device_name != "Virtual Hub":
            return None

        return [
            "Apple TV",
            "Music System",
            "Game Console",
        ]

    @property
    def source(self):
        return self.manager.active_source

    async def async_select_source(
        self,
        source,
    ):

        self.manager.select_source(
            source
        )

        self.async_write_ha_state()

    @property
    def volume_level(self):

        if self.device_name != "AVR":
            return None

        return (
            self.manager.devices["AVR"]["volume"]
            / 100
        )

    async def async_set_volume_level(
        self,
        volume,
    ):

        if self.device_name != "AVR":
            return

        self.manager.devices["AVR"]["volume"] = max(
            0,
            min(
                100,
                int(volume * 100),
            ),
        )

        self.async_write_ha_state()

    async def async_media_play(self):

        self.manager.play()

        self.async_write_ha_state()

    async def async_media_pause(self):

        self.manager.pause()

        self.async_write_ha_state()