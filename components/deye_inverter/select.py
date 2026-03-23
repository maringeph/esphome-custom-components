"""Select platform for Deye Inverter component."""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select

from . import (
    CONF_DEYE_INVERTER_ID,
    CONF_SETTINGS_DEVICE,
    CONF_SETTINGS_GRID,
    CONF_SETTINGS_BATTERY,
    CONF_SETTINGS_WORKING_MODE,
    CONF_SETTINGS_SYSTEM,
    CONF_SETTINGS_CALIFORNIA,
    CONF_GRID_TYPE,
    CONF_GRID_MODE,
    CONF_GRID_CHECK_SOURCE,
    CONF_BATTERY_TYPE,
    CONF_BATTERY_CONTROL_MODE,
    CONF_GRID_NOMINAL_VOLTAGE,
    CONF_GRID_NOMINAL_FREQUENCY,
    CONF_GRID_PHASE_SEQUENCE,
    CONF_GEN_PORT_CONTROL_MODE,
    CONF_ENERGY_PRIORITY,
    CONF_LIMIT_CONTROL_MODE,
    CONF_WORKING_MODE,
    CONF_EXT_BAUD_RATE,
    CONF_EXT_PARITY,
    CONF_EXT_STOP_BITS,
    CONF_EXT_PROTOCOL,
    CONF_SYS_LANGUAGE,
    CONF_SETTINGS_GEN_PORT,
    CONF_CA_RULE21_CATEGORY,
    CONF_CA_NORMAL_OP_CAT,
    CONF_CA_ABNORMAL_OP_CAT,
    DeyeInverter,
)

# Namespace for DeyeSelect
DeyeSelect = cg.esphome_ns.namespace("deye_inverter").class_(
    "DeyeSelect", select.Select, cg.Component
)

# =============================================================================
# Register addresses for Deye inverter select entities
# =============================================================================

# Settings Grid group
REGISTER_GRID_TYPE = 184
REGISTER_GRID_MODE = 182
REGISTER_GRID_NOMINAL_VOLTAGE = 138
REGISTER_GRID_NOMINAL_FREQUENCY = 183
REGISTER_GRID_PHASE_SEQUENCE = 147

# Settings Battery group
REGISTER_BATTERY_TYPE = 98
REGISTER_BATTERY_CONTROL_MODE = 111

# Generator Port Control Mode
REGISTER_GEN_PORT_CONTROL_MODE = 133

# Settings Working Mode
REGISTER_ENERGY_PRIORITY = 141
REGISTER_LIMIT_CONTROL_MODE = 142
REGISTER_WORKING_MODE = 142

# System Settings
REGISTER_SYS_LANGUAGE = 60

# Grid Check Source (Register 344 - Ex-Zähler/CT Auswahl)
REGISTER_GRID_CHECK_SOURCE = 344

# Device Settings (Extended)
REGISTER_EXT_BAUD_RATE = 231
REGISTER_EXT_PARITY = 232
REGISTER_EXT_STOP_BITS = 233
REGISTER_EXT_PROTOCOL = 234

# California Settings
REGISTER_CA_RULE21_CATEGORY = 341
REGISTER_CA_NORMAL_OP_CAT = 342
REGISTER_CA_ABNORMAL_OP_CAT = 343

# Options maps for select entities
# Grid Type options (Register 184)
GRID_TYPE_OPTIONS = {
    0: "Einphasig 220V/230V/240V",
    1: "Zweiphasig 120V/240V",
    2: "Dreiphasig 208V 120°",
    3: "120V Einphasig",
}

# Grid Mode options (Register 182)
GRID_MODE_OPTIONS = {
    0: "Allgemeiner Standard",
    1: "UL1741 & IEEE1547",
    2: "CPUC Rule21",
    3: "SRD-UL1741",
    10: "VDE 4105",
}

# Battery Type options (Register 98)
BATTERY_TYPE_OPTIONS = {
    0: "Blei",
    1: "Lithium",
}

# Battery Control Mode options (Register 111)
BATTERY_CONTROL_MODE_OPTIONS = {
    0: "Spannung",
    1: "Ladezustand",
    2: "Keine Batterie",
}

# Grid Nominal Voltage options (Register 138)
GRID_NOMINAL_VOLTAGE_OPTIONS = {
    0: "220V",
    1: "230V",
    2: "240V",
    3: "120V",
}

# Grid Nominal Frequency options (Register 183)
GRID_NOMINAL_FREQUENCY_OPTIONS = {
    0: "50Hz",
    1: "60Hz",
}

# Grid Phase Sequence options (Register 147)
GRID_PHASE_SEQUENCE_OPTIONS = {
    0: "0-120-240",
    1: "0-240-120",
}

# Grid Check Source options (Register 344 - CT or Smart Meter)
GRID_CHECK_SOURCE_OPTIONS = {
    0: "CT (Stromwandler)",
    1: "Meter (Ex-Zähler)",
}

# Generator Port Control Mode options (Register 133)
GEN_PORT_CONTROL_MODE_OPTIONS = {
    0: "Generatoreingang",
    1: "Smart-Last-Ausgang",
    2: "Mikro-Wechselrichter-Eingang",
}

# Energy Priority options (Register 141)
ENERGY_PRIORITY_OPTIONS = {
    0: "Battery first",
    1: "Load first",
}

# Limit Control Mode options (Register 142)
LIMIT_CONTROL_MODE_OPTIONS = {
    0: "Verkauf zuerst",
    1: "Zero Export an Last",
}

# Working Mode options (Register 142 - Bit 0-1)
WORKING_MODE_OPTIONS = {
    0: "Selling First",
    1: "Zero Export to CT",
    2: "Zero Export to Load",
    3: "Unknown",
}

# System Language options (Register 60)
SYS_LANGUAGE_OPTIONS = {
    0: "English",
    1: "Deutsch",
    2: "Español",
    3: "Français",
    4: "Italiano",
    5: "Português",
}

# Extended Baud Rate options (Register 231)
EXT_BAUD_RATE_OPTIONS = {
    0: "9600",
    1: "19200",
    2: "38400",
    3: "57600",
    4: "115200",
}

# Extended Parity options (Register 232)
EXT_PARITY_OPTIONS = {
    0: "None",
    1: "Even",
    2: "Odd",
}

# Extended Stop Bits options (Register 233)
EXT_STOP_BITS_OPTIONS = {
    0: "1",
    1: "2",
}

# Extended Protocol options (Register 234)
EXT_PROTOCOL_OPTIONS = {
    0: "Modbus RTU",
    1: "Modbus ASCII",
    2: "Modbus TCP",
}

# California Rule21 Category options (Register 341)
CA_RULE21_CATEGORY_OPTIONS = {
    0: "Category I",
    1: "Category II",
    2: "Category III",
}

# California Normal Operation Category options (Register 342)
CA_NORMAL_OP_CAT_OPTIONS = {
    0: "Default",
    1: "Category A",
    2: "Category B",
}

# California Abnormal Operation Category options (Register 343)
CA_ABNORMAL_OP_CAT_OPTIONS = {
    0: "Default",
    1: "Must Trip",
    2: "May Trip",
}


# =============================================================================
# SCHEMA DEFINITIONS (lokal in select.py)
# =============================================================================

# Settings Grid Select Schema
SETTINGS_GRID_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GRID_TYPE): select.select_schema(DeyeSelect),
        cv.Optional(CONF_GRID_MODE): select.select_schema(DeyeSelect),
        cv.Optional(CONF_GRID_NOMINAL_VOLTAGE): select.select_schema(DeyeSelect),
        cv.Optional(CONF_GRID_NOMINAL_FREQUENCY): select.select_schema(DeyeSelect),
        cv.Optional(CONF_GRID_PHASE_SEQUENCE): select.select_schema(DeyeSelect),
        cv.Optional(CONF_GRID_CHECK_SOURCE): select.select_schema(DeyeSelect),
    }
)

# Settings Device Select Schema
SETTINGS_DEVICE_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EXT_BAUD_RATE): select.select_schema(DeyeSelect),
        cv.Optional(CONF_EXT_PARITY): select.select_schema(DeyeSelect),
        cv.Optional(CONF_EXT_STOP_BITS): select.select_schema(DeyeSelect),
        cv.Optional(CONF_EXT_PROTOCOL): select.select_schema(DeyeSelect),
    }
)

# Settings Battery Select Schema
SETTINGS_BATTERY_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_TYPE): select.select_schema(DeyeSelect),
        cv.Optional(CONF_BATTERY_CONTROL_MODE): select.select_schema(DeyeSelect),
    }
)

# Settings Generator Port Select Schema
SETTINGS_GEN_PORT_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_PORT_CONTROL_MODE): select.select_schema(DeyeSelect),
    }
)

# Settings Working Mode Select Schema
SETTINGS_WORKING_MODE_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_WORKING_MODE): select.select_schema(DeyeSelect),
        cv.Optional(CONF_ENERGY_PRIORITY): select.select_schema(DeyeSelect),
        cv.Optional(CONF_LIMIT_CONTROL_MODE): select.select_schema(DeyeSelect),
    }
)

# Settings System Select Schema
SETTINGS_SYSTEM_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SYS_LANGUAGE): select.select_schema(DeyeSelect),
    }
)

# Settings California Select Schema
SETTINGS_CALIFORNIA_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_CA_RULE21_CATEGORY): select.select_schema(DeyeSelect),
        cv.Optional(CONF_CA_NORMAL_OP_CAT): select.select_schema(DeyeSelect),
        cv.Optional(CONF_CA_ABNORMAL_OP_CAT): select.select_schema(DeyeSelect),
    }
)


# =============================================================================
# PLATFORM SCHEMA
# =============================================================================

CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_SETTINGS_GRID): SETTINGS_GRID_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_DEVICE): SETTINGS_DEVICE_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_BATTERY): SETTINGS_BATTERY_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_GEN_PORT): SETTINGS_GEN_PORT_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_WORKING_MODE): SETTINGS_WORKING_MODE_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_SYSTEM): SETTINGS_SYSTEM_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_CALIFORNIA): SETTINGS_CALIFORNIA_SELECT_SCHEMA,
    }
)


# =============================================================================
# HELPER FUNCTIONS FOR to_code
# =============================================================================


def build_options_map(options_dict):
    """Build a C++ map from a Python dict for options mapping."""
    map_entries = []
    for value, label in options_dict.items():
        map_entries.append(f'{{{value}, "{label}"}}')
    return ", ".join(map_entries)


async def register_select_entity(config, key, parent, address, options_map):
    """Register a single select entity with the parent component."""
    if key not in config:
        return

    conf = config[key]
    sel = await select.new_select(
        conf,
        options=list(options_map.values()),
    )
    cg.add(sel.set_parent(parent))
    cg.add(sel.set_address(address))

    # Build and set the options map
    options_map_str = build_options_map(options_map)
    cg.add(sel.set_options_map(f"std::map<uint16_t, std::string>{{{options_map_str}}}"))

    # Register with parent's select list
    cg.add(parent.register_select(sel))


# =============================================================================
# CODE GENERATION
# =============================================================================


async def to_code(config):
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Settings Grid
    if CONF_SETTINGS_GRID in config:
        grid_config = config[CONF_SETTINGS_GRID]

        # Grid Type (Register 184)
        if CONF_GRID_TYPE in grid_config:
            await register_select_entity(
                grid_config,
                CONF_GRID_TYPE,
                var,
                REGISTER_GRID_TYPE,
                GRID_TYPE_OPTIONS,
            )

        # Grid Mode (Register 182)
        if CONF_GRID_MODE in grid_config:
            await register_select_entity(
                grid_config,
                CONF_GRID_MODE,
                var,
                REGISTER_GRID_MODE,
                GRID_MODE_OPTIONS,
            )

        # Grid Nominal Voltage (Register 138)
        if CONF_GRID_NOMINAL_VOLTAGE in grid_config:
            await register_select_entity(
                grid_config,
                CONF_GRID_NOMINAL_VOLTAGE,
                var,
                REGISTER_GRID_NOMINAL_VOLTAGE,
                GRID_NOMINAL_VOLTAGE_OPTIONS,
            )

        # Grid Nominal Frequency (Register 183)
        if CONF_GRID_NOMINAL_FREQUENCY in grid_config:
            await register_select_entity(
                grid_config,
                CONF_GRID_NOMINAL_FREQUENCY,
                var,
                REGISTER_GRID_NOMINAL_FREQUENCY,
                GRID_NOMINAL_FREQUENCY_OPTIONS,
            )

        # Grid Phase Sequence (Register 147)
        if CONF_GRID_PHASE_SEQUENCE in grid_config:
            await register_select_entity(
                grid_config,
                CONF_GRID_PHASE_SEQUENCE,
                var,
                REGISTER_GRID_PHASE_SEQUENCE,
                GRID_PHASE_SEQUENCE_OPTIONS,
            )

        # Grid Check Source (Register 344 - CT or Smart Meter)
        if CONF_GRID_CHECK_SOURCE in grid_config:
            await register_select_entity(
                grid_config,
                CONF_GRID_CHECK_SOURCE,
                var,
                REGISTER_GRID_CHECK_SOURCE,
                GRID_CHECK_SOURCE_OPTIONS,
            )

    # Settings Device (ext_* settings)
    if CONF_SETTINGS_DEVICE in config:
        device_config = config[CONF_SETTINGS_DEVICE]

        if CONF_EXT_BAUD_RATE in device_config:
            await register_select_entity(
                device_config,
                CONF_EXT_BAUD_RATE,
                var,
                REGISTER_EXT_BAUD_RATE,
                EXT_BAUD_RATE_OPTIONS,
            )

        if CONF_EXT_PARITY in device_config:
            await register_select_entity(
                device_config,
                CONF_EXT_PARITY,
                var,
                REGISTER_EXT_PARITY,
                EXT_PARITY_OPTIONS,
            )

        if CONF_EXT_STOP_BITS in device_config:
            await register_select_entity(
                device_config,
                CONF_EXT_STOP_BITS,
                var,
                REGISTER_EXT_STOP_BITS,
                EXT_STOP_BITS_OPTIONS,
            )

        if CONF_EXT_PROTOCOL in device_config:
            await register_select_entity(
                device_config,
                CONF_EXT_PROTOCOL,
                var,
                REGISTER_EXT_PROTOCOL,
                EXT_PROTOCOL_OPTIONS,
            )

    # Settings Battery
    if CONF_SETTINGS_BATTERY in config:
        battery_config = config[CONF_SETTINGS_BATTERY]

        # Battery Type (Register 98)
        if CONF_BATTERY_TYPE in battery_config:
            await register_select_entity(
                battery_config,
                CONF_BATTERY_TYPE,
                var,
                REGISTER_BATTERY_TYPE,
                BATTERY_TYPE_OPTIONS,
            )

        # Battery Control Mode (Register 111)
        if CONF_BATTERY_CONTROL_MODE in battery_config:
            await register_select_entity(
                battery_config,
                CONF_BATTERY_CONTROL_MODE,
                var,
                REGISTER_BATTERY_CONTROL_MODE,
                BATTERY_CONTROL_MODE_OPTIONS,
            )

    # Generator Port Control Mode
    if CONF_SETTINGS_GEN_PORT in config:
        gen_port_config = config[CONF_SETTINGS_GEN_PORT]
        if CONF_GEN_PORT_CONTROL_MODE in gen_port_config:
            await register_select_entity(
                gen_port_config,
                CONF_GEN_PORT_CONTROL_MODE,
                var,
                REGISTER_GEN_PORT_CONTROL_MODE,
                GEN_PORT_CONTROL_MODE_OPTIONS,
            )

    # Settings Working Mode
    if CONF_SETTINGS_WORKING_MODE in config:
        working_mode_config = config[CONF_SETTINGS_WORKING_MODE]

        # Working Mode (Register 142)
        if CONF_WORKING_MODE in working_mode_config:
            await register_select_entity(
                working_mode_config,
                CONF_WORKING_MODE,
                var,
                REGISTER_WORKING_MODE,
                WORKING_MODE_OPTIONS,
            )

        # Energy Priority (Register 141)
        if CONF_ENERGY_PRIORITY in working_mode_config:
            await register_select_entity(
                working_mode_config,
                CONF_ENERGY_PRIORITY,
                var,
                REGISTER_ENERGY_PRIORITY,
                ENERGY_PRIORITY_OPTIONS,
            )

        # Limit Control Mode (Register 142)
        if CONF_LIMIT_CONTROL_MODE in working_mode_config:
            await register_select_entity(
                working_mode_config,
                CONF_LIMIT_CONTROL_MODE,
                var,
                REGISTER_LIMIT_CONTROL_MODE,
                LIMIT_CONTROL_MODE_OPTIONS,
            )

    # Settings System
    if CONF_SETTINGS_SYSTEM in config:
        system_config = config[CONF_SETTINGS_SYSTEM]
        if CONF_SYS_LANGUAGE in system_config:
            await register_select_entity(
                system_config,
                CONF_SYS_LANGUAGE,
                var,
                REGISTER_SYS_LANGUAGE,
                SYS_LANGUAGE_OPTIONS,
            )

    # Settings California
    if CONF_SETTINGS_CALIFORNIA in config:
        ca_config = config[CONF_SETTINGS_CALIFORNIA]

        if CONF_CA_RULE21_CATEGORY in ca_config:
            await register_select_entity(
                ca_config,
                CONF_CA_RULE21_CATEGORY,
                var,
                REGISTER_CA_RULE21_CATEGORY,
                CA_RULE21_CATEGORY_OPTIONS,
            )

        if CONF_CA_NORMAL_OP_CAT in ca_config:
            await register_select_entity(
                ca_config,
                CONF_CA_NORMAL_OP_CAT,
                var,
                REGISTER_CA_NORMAL_OP_CAT,
                CA_NORMAL_OP_CAT_OPTIONS,
            )

        if CONF_CA_ABNORMAL_OP_CAT in ca_config:
            await register_select_entity(
                ca_config,
                CONF_CA_ABNORMAL_OP_CAT,
                var,
                REGISTER_CA_ABNORMAL_OP_CAT,
                CA_ABNORMAL_OP_CAT_OPTIONS,
            )
