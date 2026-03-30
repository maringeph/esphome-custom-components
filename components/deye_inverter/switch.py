"""Switch platform for Deye Inverter component."""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_SWITCH,
)

from . import (
    CONF_DEYE_INVERTER_ID,
    CONF_DEVICE_ID,
    DeyeInverter,
)

# Namespace for DeyeSwitch
DeyeSwitch = cg.esphome_ns.namespace("deye_inverter").class_(
    "DeyeSwitch", switch.Switch, cg.Component
)

# =============================================================================
# CONF CONSTANTS - Switches (lokal definiert)
# =============================================================================
CONF_SETTINGS_GRID = "settings_grid"
CONF_SETTINGS_DEVICE = "settings_device"
CONF_SETTINGS_TIME_OF_USE = "settings_time_of_use"
CONF_SETTINGS_SYSTEM = "settings_system"
CONF_SETTINGS_WORKING_MODE = "settings_working_mode"
CONF_SETTINGS_BATTERY = "settings_battery"
CONF_SETTINGS_GENERATOR = "settings_generator"

# Grid switches
CONF_GRID_CHARGE = "grid_charge"
CONF_SOLAR_SELL = "solar_sell"
CONF_GRID_PEAK_SHAVING = "grid_peak_shaving"
CONF_GEN_PEAK_SHAVING = "gen_peak_shaving"
CONF_ON_GRID_ALWAYS_ON = "on_grid_always_on"
CONF_MICROINVERTER_EXPORT_TO_GRID = "microinverter_export_to_grid"

# Device switches
CONF_EXTERNAL_CT_DIRECTION_CHECK = "external_ct_direction_check"
CONF_SOLAR_ARC_FAULT_MODE = "solar_arc_fault_mode"

# Working mode switches
CONF_FORCED_OFF_GRID_WORK = "forced_off_grid_work"

# Battery switches
CONF_BATTERY_LOSS_REPORT_FAULT = "battery_loss_report_fault"

# Generator switches
CONF_EXTERNAL_RELAY = "external_relay"
CONF_GEN_PORT_FORCE_ON = "gen_port_force_on"
CONF_GEN_PORT_COUPLE_FREQUENCY_LIMIT = "gen_port_couple_frequency_limit"

# Time of Use switches
CONF_TIME_OF_USE = "time_of_use"

# Solar/General Charge Enable
CONF_TIME_POINT_1_CHARGE_ENABLE = "time_point_1_charge_enable"
CONF_TIME_POINT_2_CHARGE_ENABLE = "time_point_2_charge_enable"
CONF_TIME_POINT_3_CHARGE_ENABLE = "time_point_3_charge_enable"
CONF_TIME_POINT_4_CHARGE_ENABLE = "time_point_4_charge_enable"
CONF_TIME_POINT_5_CHARGE_ENABLE = "time_point_5_charge_enable"
CONF_TIME_POINT_6_CHARGE_ENABLE = "time_point_6_charge_enable"

# Grid Charge Enable
CONF_TIME_POINT_1_GRID_CHARGE_ENABLE = "time_point_1_grid_charge_enable"
CONF_TIME_POINT_2_GRID_CHARGE_ENABLE = "time_point_2_grid_charge_enable"
CONF_TIME_POINT_3_GRID_CHARGE_ENABLE = "time_point_3_grid_charge_enable"
CONF_TIME_POINT_4_GRID_CHARGE_ENABLE = "time_point_4_grid_charge_enable"
CONF_TIME_POINT_5_GRID_CHARGE_ENABLE = "time_point_5_grid_charge_enable"
CONF_TIME_POINT_6_GRID_CHARGE_ENABLE = "time_point_6_grid_charge_enable"

# Generator Charge Enable
CONF_TIME_POINT_1_GEN_CHARGE_ENABLE = "time_point_1_gen_charge_enable"
CONF_TIME_POINT_2_GEN_CHARGE_ENABLE = "time_point_2_gen_charge_enable"
CONF_TIME_POINT_3_GEN_CHARGE_ENABLE = "time_point_3_gen_charge_enable"
CONF_TIME_POINT_4_GEN_CHARGE_ENABLE = "time_point_4_gen_charge_enable"
CONF_TIME_POINT_5_GEN_CHARGE_ENABLE = "time_point_5_gen_charge_enable"
CONF_TIME_POINT_6_GEN_CHARGE_ENABLE = "time_point_6_gen_charge_enable"

# Weekday Enables
CONF_WEEKDAY_MONDAY = "weekday_monday"
CONF_WEEKDAY_TUESDAY = "weekday_tuesday"
CONF_WEEKDAY_WEDNESDAY = "weekday_wednesday"
CONF_WEEKDAY_THURSDAY = "weekday_thursday"
CONF_WEEKDAY_FRIDAY = "weekday_friday"
CONF_WEEKDAY_SATURDAY = "weekday_saturday"
CONF_WEEKDAY_SUNDAY = "weekday_sunday"

# System switches
CONF_SYS_BEEPER = "sys_beeper"
CONF_SYS_LCD_BACKLIGHT = "sys_lcd_backlight"
CONF_SYS_DST_ENABLE = "sys_dst_enable"
CONF_SYS_REMOTE_LOCK = "sys_remote_lock"

# =============================================================================
# SCHEMA DEFINITIONS
# =============================================================================


# Helper schema that creates switch schema with DeyeSwitch class
def deye_switch_schema(**kwargs):
    return switch.switch_schema(DeyeSwitch, **kwargs)


# Settings Grid Schema
SETTINGS_GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GRID_CHARGE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SOLAR_SELL): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_GRID_PEAK_SHAVING): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_GEN_PEAK_SHAVING): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_ON_GRID_ALWAYS_ON): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_MICROINVERTER_EXPORT_TO_GRID): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Device Schema
SETTINGS_DEVICE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EXTERNAL_CT_DIRECTION_CHECK): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SOLAR_ARC_FAULT_MODE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Working Mode Schema
SETTINGS_WORKING_MODE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_FORCED_OFF_GRID_WORK): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Battery Schema
SETTINGS_BATTERY_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_LOSS_REPORT_FAULT): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Generator Schema
SETTINGS_GENERATOR_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EXTERNAL_RELAY): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_GEN_PORT_FORCE_ON): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_GEN_PORT_COUPLE_FREQUENCY_LIMIT): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings System Schema
SETTINGS_SYSTEM_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SYS_BEEPER): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SYS_LCD_BACKLIGHT): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SYS_DST_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SYS_REMOTE_LOCK): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Time of Use Schema
SETTINGS_TIME_OF_USE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_TIME_OF_USE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # Solar/General Charge Enable (Bit 0)
        cv.Optional(CONF_TIME_POINT_1_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_2_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_3_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_4_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_5_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_6_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # Grid Charge Enable (Bit 1)
        cv.Optional(CONF_TIME_POINT_1_GRID_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_2_GRID_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_3_GRID_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_4_GRID_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_5_GRID_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_6_GRID_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # Generator Charge Enable (Bit 2)
        cv.Optional(CONF_TIME_POINT_1_GEN_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_2_GEN_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_3_GEN_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_4_GEN_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_5_GEN_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_6_GEN_CHARGE_ENABLE): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # Weekday Enables (Register 146, Bits 1-7)
        cv.Optional(CONF_WEEKDAY_MONDAY): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_TUESDAY): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_WEDNESDAY): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_THURSDAY): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_FRIDAY): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_SATURDAY): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_SUNDAY): deye_switch_schema(
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# =============================================================================
# PLATFORM SCHEMA
# =============================================================================

CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_DEVICE_ID): cv.string,
        cv.Optional(CONF_SETTINGS_GRID): SETTINGS_GRID_SCHEMA,
        cv.Optional(CONF_SETTINGS_DEVICE): SETTINGS_DEVICE_SCHEMA,
        cv.Optional(CONF_SETTINGS_WORKING_MODE): SETTINGS_WORKING_MODE_SCHEMA,
        cv.Optional(CONF_SETTINGS_BATTERY): SETTINGS_BATTERY_SCHEMA,
        cv.Optional(CONF_SETTINGS_GENERATOR): SETTINGS_GENERATOR_SCHEMA,
        cv.Optional(CONF_SETTINGS_SYSTEM): SETTINGS_SYSTEM_SCHEMA,
        cv.Optional(CONF_SETTINGS_TIME_OF_USE): SETTINGS_TIME_OF_USE_SCHEMA,
    }
)


# =============================================================================
# HELPER FUNCTIONS FOR to_code
# =============================================================================


async def register_switch_entity(
    config, key, parent, address, bitmask, device_obj=None
):
    """Register a single switch entity with the parent component."""
    if key not in config:
        return

    conf = config[key]
    sw = await switch.new_switch(conf)
    cg.add(sw.set_parent(parent))
    cg.add(sw.set_address(address))
    cg.add(sw.set_bitmask(bitmask))

    # Register with parent's switch list
    cg.add(parent.register_switch(sw))

    # Set device for Home Assistant grouping
    if device_obj is not None:
        cg.add(sw.set_device(device_obj))


async def register_switch_entity_2bit(
    config,
    key,
    parent,
    address,
    bitmask,
    value_enable,
    value_disable,
    shift,
    device_obj=None,
):
    """Register a 2-bit field switch entity with the parent component.

    For 2-bit fields:
    - 00/01 = disabled (undefined state)
    - 10 (0x02) = disable (OFF)
    - 11 (0x03) = enable (ON)
    """
    if key not in config:
        return

    conf = config[key]
    sw = await switch.new_switch(conf)
    cg.add(sw.set_parent(parent))
    cg.add(sw.set_address(address))
    cg.add(sw.set_bitmask(bitmask))
    cg.add(sw.set_is_2bit_field(True))
    cg.add(sw.set_value_enable(value_enable))
    cg.add(sw.set_value_disable(value_disable))
    cg.add(sw.set_bit_shift(shift))

    # Register with parent's switch list
    cg.add(parent.register_switch(sw))

    # Set device for Home Assistant grouping
    if device_obj is not None:
        cg.add(sw.set_device(device_obj))


# =============================================================================
# CODE GENERATION
# =============================================================================


async def to_code(config):
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Handle device_id for Home Assistant grouping
    from . import get_or_create_device

    device_id = config.get(CONF_DEVICE_ID)
    device_obj = await get_or_create_device(device_id)

    # Settings Grid Switches
    if CONF_SETTINGS_GRID in config:
        grid_config = config[CONF_SETTINGS_GRID]

        # Grid Charge (Register 130, Bit 0)
        if CONF_GRID_CHARGE in grid_config:
            await register_switch_entity(
                grid_config,
                CONF_GRID_CHARGE,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_GRID_CHARGE"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                device_obj,
            )

        # Solar Sell (Register 145, Bit 0)
        if CONF_SOLAR_SELL in grid_config:
            await register_switch_entity(
                grid_config,
                CONF_SOLAR_SELL,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SOLAR_SELL"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                device_obj,
            )

        # Grid Peak Shaving (Register 178, Bits 4-5)
        if CONF_GRID_PEAK_SHAVING in grid_config:
            await register_switch_entity_2bit(
                grid_config,
                CONF_GRID_PEAK_SHAVING,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_1"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_4_5"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE << 4"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE << 4"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_GRID_PEAK_SHAVING"),
                device_obj,
            )

        # Gen Peak Shaving (Register 178, Bits 2-3)
        if CONF_GEN_PEAK_SHAVING in grid_config:
            await register_switch_entity_2bit(
                grid_config,
                CONF_GEN_PEAK_SHAVING,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_1"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_2_3"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE << 2"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE << 2"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_GEN_PEAK_SHAVING"),
                device_obj,
            )

        # On Grid Always On (Register 178, Bits 6-7)
        if CONF_ON_GRID_ALWAYS_ON in grid_config:
            await register_switch_entity_2bit(
                grid_config,
                CONF_ON_GRID_ALWAYS_ON,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_1"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_6_7"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE << 6"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE << 6"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_ON_GRID_ALWAYS_ON"),
                device_obj,
            )

        # Microinverter Export to Grid (Register 178, Bits 0-1)
        if CONF_MICROINVERTER_EXPORT_TO_GRID in grid_config:
            await register_switch_entity_2bit(
                grid_config,
                CONF_MICROINVERTER_EXPORT_TO_GRID,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_1"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_0_1"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_MICROINVERTER_EXPORT"),
                device_obj,
            )

    # Settings Device Switches
    if CONF_SETTINGS_DEVICE in config:
        device_config = config[CONF_SETTINGS_DEVICE]

        # External CT Direction Check (Register 179, Bits 0-1)
        if CONF_EXTERNAL_CT_DIRECTION_CHECK in device_config:
            await register_switch_entity_2bit(
                device_config,
                CONF_EXTERNAL_CT_DIRECTION_CHECK,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_2"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_0_1"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_CT_DIRECTION_CHECK"),
                device_obj,
            )

        # Solar Arc Fault Mode (Register 181, 1-bit)
        if CONF_SOLAR_ARC_FAULT_MODE in device_config:
            await register_switch_entity(
                device_config,
                CONF_SOLAR_ARC_FAULT_MODE,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SOLAR_ARC_FAULT_MODE"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                device_obj,
            )

    # Settings System Switches
    if CONF_SETTINGS_SYSTEM in config:
        system_config = config[CONF_SETTINGS_SYSTEM]

        # System Beeper (Register 64, Bit 0)
        if CONF_SYS_BEEPER in system_config:
            await register_switch_entity(
                system_config,
                CONF_SYS_BEEPER,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SYSTEM_TIME_BYTE5"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                device_obj,
            )

        # System LCD Backlight (Register 65, Bit 0)
        if CONF_SYS_LCD_BACKLIGHT in system_config:
            await register_switch_entity(
                system_config,
                CONF_SYS_LCD_BACKLIGHT,
                var,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_INSULATION_RESISTANCE_LIMIT"
                ),
                cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                device_obj,
            )

        # System DST Enable (Register 66, Bit 0)
        if CONF_SYS_DST_ENABLE in system_config:
            await register_switch_entity(
                system_config,
                CONF_SYS_DST_ENABLE,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_RESERVED_66"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                device_obj,
            )

        # System Remote Lock (Register 60)
        # Special values: 0x0000 = on (locked), 0x0002 = off (unlocked)
        if CONF_SYS_REMOTE_LOCK in system_config:
            await register_switch_entity_2bit(
                system_config,
                CONF_SYS_REMOTE_LOCK,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_REMOTE_LOCK"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_FULL_REGISTER"),
                cg.RawExpression("esphome::deye_inverter::VALUE_REMOTE_LOCK_ON"),
                cg.RawExpression("esphome::deye_inverter::VALUE_REMOTE_LOCK_OFF"),
                0,  # shift
                device_obj,
            )

    # Settings Time of Use Switches
    if CONF_SETTINGS_TIME_OF_USE in config:
        tou_config = config[CONF_SETTINGS_TIME_OF_USE]

        # Time of Use (Register 146, Bit 0)
        if CONF_TIME_OF_USE in tou_config:
            await register_switch_entity(
                tou_config,
                CONF_TIME_OF_USE,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_TIME_OF_USE"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                device_obj,
            )

        # Time Point Solar/General Charge Enable switches (Registers 172-177, Bit 0)
        solar_charge_switches = [
            (
                CONF_TIME_POINT_1_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_1_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_2_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_2_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_3_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_3_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_4_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_4_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_5_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_5_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_6_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_6_CHARGE_ENABLE"
                ),
            ),
        ]
        for conf_key, register_addr in solar_charge_switches:
            if conf_key in tou_config:
                await register_switch_entity(
                    tou_config,
                    conf_key,
                    var,
                    register_addr,
                    cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                    device_obj,
                )

        # Time Point Grid Charge Enable switches (Registers 172-177, Bit 1)
        grid_charge_switches = [
            (
                CONF_TIME_POINT_1_GRID_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_1_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_2_GRID_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_2_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_3_GRID_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_3_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_4_GRID_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_4_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_5_GRID_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_5_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_6_GRID_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_6_CHARGE_ENABLE"
                ),
            ),
        ]
        for conf_key, register_addr in grid_charge_switches:
            if conf_key in tou_config:
                await register_switch_entity(
                    tou_config,
                    conf_key,
                    var,
                    register_addr,
                    cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_1"),
                    device_obj,
                )

        # Time Point Generator Charge Enable switches (Registers 172-177, Bit 2)
        gen_charge_switches = [
            (
                CONF_TIME_POINT_1_GEN_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_1_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_2_GEN_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_2_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_3_GEN_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_3_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_4_GEN_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_4_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_5_GEN_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_5_CHARGE_ENABLE"
                ),
            ),
            (
                CONF_TIME_POINT_6_GEN_CHARGE_ENABLE,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_TIME_POINT_6_CHARGE_ENABLE"
                ),
            ),
        ]
        for conf_key, register_addr in gen_charge_switches:
            if conf_key in tou_config:
                await register_switch_entity(
                    tou_config,
                    conf_key,
                    var,
                    register_addr,
                    cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_2"),
                    device_obj,
                )

        # Weekday Enable switches (Register 146, Bits 1-7)
        weekday_switches = [
            (
                CONF_WEEKDAY_MONDAY,
                cg.RawExpression("esphome::deye_inverter::BITMASK_WEEKDAY_MONDAY"),
            ),
            (
                CONF_WEEKDAY_TUESDAY,
                cg.RawExpression("esphome::deye_inverter::BITMASK_WEEKDAY_TUESDAY"),
            ),
            (
                CONF_WEEKDAY_WEDNESDAY,
                cg.RawExpression("esphome::deye_inverter::BITMASK_WEEKDAY_WEDNESDAY"),
            ),
            (
                CONF_WEEKDAY_THURSDAY,
                cg.RawExpression("esphome::deye_inverter::BITMASK_WEEKDAY_THURSDAY"),
            ),
            (
                CONF_WEEKDAY_FRIDAY,
                cg.RawExpression("esphome::deye_inverter::BITMASK_WEEKDAY_FRIDAY"),
            ),
            (
                CONF_WEEKDAY_SATURDAY,
                cg.RawExpression("esphome::deye_inverter::BITMASK_WEEKDAY_SATURDAY"),
            ),
            (
                CONF_WEEKDAY_SUNDAY,
                cg.RawExpression("esphome::deye_inverter::BITMASK_WEEKDAY_SUNDAY"),
            ),
        ]
        for conf_key, bitmask in weekday_switches:
            if conf_key in tou_config:
                await register_switch_entity(
                    tou_config,
                    conf_key,
                    var,
                    cg.RawExpression("esphome::deye_inverter::REG_TIME_OF_USE"),
                    bitmask,
                    device_obj,
                )

        # Settings Working Mode - Forced Off Grid Work (Register 179, Bits 2-3)
    if CONF_SETTINGS_WORKING_MODE in config:
        working_mode_config = config[CONF_SETTINGS_WORKING_MODE]
        if CONF_FORCED_OFF_GRID_WORK in working_mode_config:
            await register_switch_entity_2bit(
                working_mode_config,
                CONF_FORCED_OFF_GRID_WORK,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_2"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_2_3"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE << 2"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE << 2"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_FORCED_OFF_GRID"),
                device_obj,
            )

    # Settings Battery - Battery Loss Report Fault (Register 178, Bits 10-11)
    if CONF_SETTINGS_BATTERY in config:
        battery_config = config[CONF_SETTINGS_BATTERY]
        if CONF_BATTERY_LOSS_REPORT_FAULT in battery_config:
            await register_switch_entity_2bit(
                battery_config,
                CONF_BATTERY_LOSS_REPORT_FAULT,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_1"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_10_11"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE << 10"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE << 10"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_BATTERY_LOSS_FAULT"),
                device_obj,
            )

    # Settings Generator - External Relay (Register 178, Bits 8-9) & Gen Port Force On
    if CONF_SETTINGS_GENERATOR in config:
        generator_config = config[CONF_SETTINGS_GENERATOR]

        # External Relay (Register 178, Bits 8-9)
        if CONF_EXTERNAL_RELAY in generator_config:
            await register_switch_entity_2bit(
                generator_config,
                CONF_EXTERNAL_RELAY,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_1"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_8_9"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE << 8"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE << 8"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_EXTERNAL_RELAY"),
                device_obj,
            )

        # Gen Port Force On (Register 132, Bit 0)
        if CONF_GEN_PORT_FORCE_ON in generator_config:
            await register_switch_entity(
                generator_config,
                CONF_GEN_PORT_FORCE_ON,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_GEN_PORT_FORCE_ON"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_BIT_0"),
                device_obj,
            )

        # Gen Port Couple Frequency Limit (Register 178, Bits 12-13)
        if CONF_GEN_PORT_COUPLE_FREQUENCY_LIMIT in generator_config:
            await register_switch_entity_2bit(
                generator_config,
                CONF_GEN_PORT_COUPLE_FREQUENCY_LIMIT,
                var,
                cg.RawExpression("esphome::deye_inverter::REG_SPECIAL_FUNCTION_1"),
                cg.RawExpression("esphome::deye_inverter::BITMASK_2BIT_12_13"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_ENABLE << 12"),
                cg.RawExpression("esphome::deye_inverter::VALUE_2BIT_DISABLE << 12"),
                cg.RawExpression("esphome::deye_inverter::SHIFT_GEN_PORT_COUPLE_FREQ"),
                device_obj,
            )
