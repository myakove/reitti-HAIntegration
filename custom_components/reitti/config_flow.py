# File: custom_components/reitti/config_flow.py
# Date: 2025-09-14

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN, CONF_URL, CONF_DEVICE, CONF_PORT

class ReittiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_reconfigure(self, user_input=None):
        """Handle reconfiguration of the integration."""
        errors = {}
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])

        if user_input is not None:
            # Validate the input
            try:
                # Basic validation - you can add more sophisticated checks here
                if not user_input[CONF_URL]:
                    errors[CONF_URL] = "url_required"
                elif not user_input["api_key"]:
                    errors["api_key"] = "api_key_required"
                elif not user_input[CONF_DEVICE]:
                    errors[CONF_DEVICE] = "device_required"
                else:
                    # Update the config entry with new data
                    new_data = {
                        CONF_URL: user_input[CONF_URL],
                        "api_key": user_input["api_key"],
                        CONF_DEVICE: user_input[CONF_DEVICE],
                        CONF_PORT: user_input.get(CONF_PORT, 8080),
                    }

                    # Update options
                    new_options = {
                        "interval_seconds": user_input.get("interval_seconds", 30),
                        "enable_debug_logging": user_input.get("enable_debug_logging", False),
                        "enable_push": user_input.get("enable_push", True),
                        "friendly_name": user_input.get("friendly_name", "Reitti Integration"),
                    }

                    # Update the entry with both data and options
                    self.hass.config_entries.async_update_entry(
                        entry,
                        data=new_data,
                        options=new_options,
                        title=user_input.get("friendly_name", entry.title)
                    )

                    # Reload the integration to apply changes
                    await self.hass.config_entries.async_reload(entry.entry_id)

                    return self.async_create_entry(
                        title=user_input.get("friendly_name", entry.title),
                        data={}
                    )
            except Exception as ex:
                errors["base"] = "unknown_error"

        # Pre-populate form with current values
        current_data = entry.data
        current_options = entry.options
        schema = vol.Schema(
            {
                vol.Required(CONF_URL, default=current_data.get(CONF_URL, "http://reitti")): str,
                vol.Optional(CONF_PORT, default=current_data.get(CONF_PORT, 8080)): int,
                vol.Required("api_key", default=current_data.get("api_key", "")): str,
                vol.Required(CONF_DEVICE, default=current_data.get(CONF_DEVICE, "")): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="device_tracker")
                ),
                vol.Optional("interval_seconds", default=current_options.get("interval_seconds", 30)): vol.All(int, vol.Range(min=5, max=3600)),
                vol.Optional("enable_debug_logging", default=current_options.get("enable_debug_logging", False)): bool,
                vol.Optional("enable_push", default=current_options.get("enable_push", True)): bool,
                vol.Optional("friendly_name", default=current_options.get("friendly_name", "Reitti Integration")): str,
            }
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "integration_name": entry.title or "Reitti Integration"
            }
        )

    async def async_step_user(self, user_input=None):
        """Initial configuration step for user input."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get("friendly_name", "Reitti Integration"),
                data={
                    CONF_URL: user_input[CONF_URL],
                    "api_key": user_input["api_key"],
                    CONF_DEVICE: user_input[CONF_DEVICE],
                    CONF_PORT: user_input.get(CONF_PORT, 8080),
                },
                options={
                    "interval_seconds": user_input.get("interval_seconds", 30),
                    "enable_debug_logging": user_input.get("enable_debug_logging", False),
                    "enable_push": user_input.get("enable_push", True),
                    "friendly_name": user_input.get("friendly_name", "Reitti Integration"),
                },
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_URL, default="http://reitti"): str,
                vol.Optional(CONF_PORT, default=8080): int,
                vol.Required("api_key"): str,
                vol.Required(CONF_DEVICE): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="device_tracker")
                ),
                vol.Optional("interval_seconds", default=30): int,
                vol.Optional("enable_debug_logging", default=False): bool,
                vol.Optional("enable_push", default=True): bool,
                vol.Optional("friendly_name", default="Reitti Integration"): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ReittiOptionsFlow(config_entry)



class ReittiOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Reitti integration."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        super().__init__()
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            # Validate the options
            try:
                if user_input.get("interval_seconds", 30) < 5:
                    errors["interval_seconds"] = "interval_too_short"
                else:
                    # Handle device tracker change if provided
                    if CONF_DEVICE in user_input:
                        # Update config data with new device tracker
                        new_data = dict(self.config_entry.data)
                        new_data[CONF_DEVICE] = user_input[CONF_DEVICE]

                        # Remove device from user_input as it goes to data, not options
                        options_data = {k: v for k, v in user_input.items() if k != CONF_DEVICE}

                        # Update both data and options
                        self.hass.config_entries.async_update_entry(
                            self.config_entry,
                            data=new_data,
                            options=options_data
                        )

                        # Reload the integration to apply changes
                        await self.hass.config_entries.async_reload(self.config_entry.entry_id)

                    return self.async_create_entry(title="", data=user_input if CONF_DEVICE not in user_input else {k: v for k, v in user_input.items() if k != CONF_DEVICE})
            except Exception:
                errors["base"] = "unknown_error"

        # Get current options with defaults
        current_options = self.config_entry.options
        current_data = self.config_entry.data
        schema = vol.Schema(
            {
                vol.Optional(
                    "interval_seconds",
                    default=current_options.get("interval_seconds", 30),
                    description={"suggested_value": current_options.get("interval_seconds", 30)}
                ): vol.All(int, vol.Range(min=5, max=3600)),
                vol.Optional(
                    "enable_debug_logging",
                    default=current_options.get("enable_debug_logging", False)
                ): bool,
                vol.Optional(
                    "enable_push",
                    default=current_options.get("enable_push", True)
                ): bool,
                vol.Optional(
                    "friendly_name",
                    default=current_options.get("friendly_name", "Reitti Integration")
                ): str,
                vol.Optional(
                    CONF_DEVICE,
                    default=current_data.get(CONF_DEVICE, ""),
                    description={"suggested_value": current_data.get(CONF_DEVICE, "")}
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="device_tracker")
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "integration_name": self.config_entry.title or "Reitti Integration"
            }
        )
