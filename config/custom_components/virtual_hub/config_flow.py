import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_IP,
    CONF_OTP,
    VALID_OTP,
)


class VirtualHubConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):

    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):

        errors = {}

        if user_input is not None:

            ip = user_input[CONF_IP]
            otp = user_input[CONF_OTP]

            await self.async_set_unique_id(ip)
            self._abort_if_unique_id_configured()

            if otp != VALID_OTP:
                errors["base"] = "invalid_otp"

            else:
                return self.async_create_entry(
                    title=f"Virtual Hub ({ip})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP): str,
                    vol.Required(CONF_OTP): str,
                }
            ),
            errors=errors,
        )