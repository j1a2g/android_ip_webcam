"""Coordinator object for the Android IP Webcam integration."""

from datetime import timedelta
import logging

from pydroid_ipcam import PyDroidIPCam
from pydroid_ipcam.exceptions import PyDroidIPCamException

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

type AndroidIPCamConfigEntry = ConfigEntry[AndroidIPCamDataUpdateCoordinator]


class AndroidIPCamDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Coordinator class for the Android IP Webcam."""

    config_entry: AndroidIPCamConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: AndroidIPCamConfigEntry,
        cam: PyDroidIPCam,
    ) -> None:
        """Initialize the Android IP Webcam."""
        self.hass = hass
        self.cam = cam
        super().__init__(
            self.hass,
            _LOGGER,
            name=f"{DOMAIN} {config_entry.data[CONF_HOST]}",
            update_interval=timedelta(seconds=2),
        )

    async def _async_update_data(self) -> None:
        """Update Android IP Webcam entities."""
        try:
            await self.cam.update()
        except PyDroidIPCamException as err:
            raise UpdateFailed(err) from err
