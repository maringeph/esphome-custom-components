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
# Register addresses and bitmasks for Deye inverter switches
# =============================================================================

# Settings Grid group (Register 130, 145, 178)
REGISTER_GRID_CHARGE = 130
BITMASK_GRID_CHARGE = 0x0001

REGISTER_SOLAR_SELL = 145
BITMASK_SOLAR_SELL = 0x0001

# Gen Port Force On (Register 132, Bit 0)
REGISTER_GEN_PORT_FORCE_ON = 132
BITMASK_GEN_PORT_FORCE_ON = 0x0001

# Register 178 - Grid/Gen Peak Shaving and On-Grid Always On
REGISTER_GRID_PEAK_SHAVING = 178
BITMASK_GRID_PEAK_SHAVING = 0x0030  # Bits 4-5
VALUE_ENABLE_GRID_PEAK_SHAVING = 0x0030
VALUE_DISABLE_GRID_PEAK_SHAVING = 0x0020
SHIFT_GRID_PEAK_SHAVING = 4

REGISTER_GEN_PEAK_SHAVING = 178
BITMASK_GEN_PEAK_SHAVING = 0x000C  # Bits 2-3
VALUE_ENABLE_GEN_PEAK_SHAVING = 0x000C
VALUE_DISABLE_GEN_PEAK_SHAVING = 0x0008
SHIFT_GEN_PEAK_SHAVING = 2

REGISTER_ON_GRID_ALWAYS_ON = 178
BITMASK_ON_GRID_ALWAYS_ON = 0x00C0  # Bits 6-7
VALUE_ENABLE_ON_GRID_ALWAYS_ON = 0x00C0
VALUE_DISABLE_ON_GRID_ALWAYS_ON = 0x0080
SHIFT_ON_GRID_ALWAYS_ON = 6

# Settings Device group - External CT Direction Check (Register 179)
REGISTER_EXTERNAL_CT_DIRECTION_CHECK = 179
BITMASK_EXTERNAL_CT_DIRECTION_CHECK = 0x0003  # Bits 0-1
VALUE_ENABLE_CT_DIRECTION_CHECK = 0x0003
VALUE_DISABLE_CT_DIRECTION_CHECK = 0x0002
SHIFT_CT_DIRECTION_CHECK = 0

# Settings Time of Use group (Register 146)
REGISTER_TIME_OF_USE = 146
BITMASK_TIME_OF_USE = 0x0001

# Time Point Charge Enable registers (172-177) - Same registers, different bits
REGISTER_TIME_POINT_1_CHARGE = 172
REGISTER_TIME_POINT_2_CHARGE = 173
REGISTER_TIME_POINT_3_CHARGE = 174
REGISTER_TIME_POINT_4_CHARGE = 175
REGISTER_TIME_POINT_5_CHARGE = 176
REGISTER_TIME_POINT_6_CHARGE = 177

# Bitmasks for different charge sources
BITMASK_CHARGE_ENABLE_SOLAR = 0x0001  # Bit 0: Solar/General Charge Enable
BITMASK_CHARGE_ENABLE_GRID = 0x0002  # Bit 1: Grid Charge Enable
BITMASK_CHARGE_ENABLE_GEN = 0x0004  # Bit 2: Generator Charge Enable

# Weekday Enables (Register 146 - Time of Use register, Bits 1-7)
REGISTER_TIME_OF_USE_WEEKDAYS = 146
BITMASK_WEEKDAY_MONDAY = 0x0002  # Bit 1
BITMASK_WEEKDAY_TUESDAY = 0x0004  # Bit 2
BITMASK_WEEKDAY_WEDNESDAY = 0x0008  # Bit 3
BITMASK_WEEKDAY_THURSDAY = 0x0010  # Bit 4
BITMASK_WEEKDAY_FRIDAY = 0x0020  # Bit 5
BITMASK_WEEKDAY_SATURDAY = 0x0040  # Bit 6
BITMASK_WEEKDAY_SUNDAY = 0x0080  # Bit 7

# System Settings (NEW - registers 60-97)
REGISTER_SYS_BEEPER = 64
BITMASK_SYS_BEEPER = 0x0001

REGISTER_SYS_LCD_BACKLIGHT = 65
BITMASK_SYS_LCD_BACKLIGHT = 0x0001

REGISTER_SYS_DST_ENABLE = 66
BITMASK_SYS_DST_ENABLE = 0x0001

REGISTER_SYS_REMOTE_LOCK = 67
BITMASK_SYS_REMOTE_LOCK = 0x0001

# Special Functions - Register 178 (remaining functions)
REGISTER_MICROINVERTER_EXPORT_TO_GRID = 178
BITMASK_MICROINVERTER_EXPORT_TO_GRID = 0x0003  # Bits 0-1
VALUE_ENABLE_MICROINVERTER_EXPORT = 0x0003
VALUE_DISABLE_MICROINVERTER_EXPORT = 0x0002
SHIFT_MICROINVERTER_EXPORT = 0

REGISTER_EXTERNAL_RELAY = 178
BITMASK_EXTERNAL_RELAY = 0x0300  # Bits 8-9
VALUE_ENABLE_EXTERNAL_RELAY = 0x0300
VALUE_DISABLE_EXTERNAL_RELAY = 0x0200
SHIFT_EXTERNAL_RELAY = 8

REGISTER_BATTERY_LOSS_REPORT_FAULT = 178
BITMASK_BATTERY_LOSS_REPORT_FAULT = 0x0C00  # Bits 10-11
VALUE_ENABLE_BATTERY_LOSS_FAULT = 0x0C00
VALUE_DISABLE_BATTERY_LOSS_FAULT = 0x0800
SHIFT_BATTERY_LOSS_FAULT = 10

# Special Functions - Register 179 (remaining functions)
REGISTER_FORCED_OFF_GRID_WORK = 179
BITMASK_FORCED_OFF_GRID_WORK = 0x000C  # Bits 2-3
VALUE_ENABLE_FORCED_OFF_GRID = 0x000C
VALUE_DISABLE_FORCED_OFF_GRID = 0x0008
SHIFT_FORCED_OFF_GRID = 2

# Register 181 - Solar Arc Fault Mode (1-bit)
REGISTER_SOLAR_ARC_FAULT_MODE = 181
BITMASK_SOLAR_ARC_FAULT_MODE = 0x0001

# Generator Charging Enabled (Register 129)
REGISTER_GENERATOR_CHARGING_ENABLED = 129
BITMASK_GENERATOR_CHARGING_ENABLED = 0x0001


# =============================================================================
# SCHEMA DEFINITIONS
# =============================================================================

# Settings Grid Schema
SETTINGS_GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GRID_CHARGE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SOLAR_SELL): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_GRID_PEAK_SHAVING): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_GEN_PEAK_SHAVING): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_ON_GRID_ALWAYS_ON): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_MICROINVERTER_EXPORT_TO_GRID): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Device Schema
SETTINGS_DEVICE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EXTERNAL_CT_DIRECTION_CHECK): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SOLAR_ARC_FAULT_MODE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Working Mode Schema
SETTINGS_WORKING_MODE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_FORCED_OFF_GRID_WORK): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Battery Schema
SETTINGS_BATTERY_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_LOSS_REPORT_FAULT): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Generator Schema
SETTINGS_GENERATOR_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EXTERNAL_RELAY): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_GEN_PORT_FORCE_ON): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings System Schema
SETTINGS_SYSTEM_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SYS_BEEPER): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SYS_LCD_BACKLIGHT): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SYS_DST_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_SYS_REMOTE_LOCK): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
    }
)

# Settings Time of Use Schema
SETTINGS_TIME_OF_USE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_TIME_OF_USE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # Solar/General Charge Enable (Bit 0)
        cv.Optional(CONF_TIME_POINT_1_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_2_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_3_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_4_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_5_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_6_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # Grid Charge Enable (Bit 1)
        cv.Optional(CONF_TIME_POINT_1_GRID_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_2_GRID_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_3_GRID_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_4_GRID_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_5_GRID_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_6_GRID_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # Generator Charge Enable (Bit 2)
        cv.Optional(CONF_TIME_POINT_1_GEN_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_2_GEN_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_3_GEN_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_4_GEN_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_5_GEN_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_TIME_POINT_6_GEN_CHARGE_ENABLE): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        # Weekday Enables (Register 146, Bits 1-7)
        cv.Optional(CONF_WEEKDAY_MONDAY): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_TUESDAY): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_WEDNESDAY): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_THURSDAY): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_FRIDAY): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_SATURDAY): switch.switch_schema(
            DeyeSwitch,
            device_class=DEVICE_CLASS_SWITCH,
        ),
        cv.Optional(CONF_WEEKDAY_SUNDAY): switch.switch_schema(
            DeyeSwitch,
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


async def register_switch_entity(config, key, parent, address, bitmask):
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


async def register_switch_entity_2bit(
    config, key, parent, address, bitmask, value_enable, value_disable, shift
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


# =============================================================================
# CODE GENERATION
# =============================================================================


async def to_code(config):
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Settings Grid Switches
    if CONF_SETTINGS_GRID in config:
        grid_config = config[CONF_SETTINGS_GRID]

        # Grid Charge (Register 130, Bit 0)
        if CONF_GRID_CHARGE in grid_config:
            await register_switch_entity(
                grid_config,
                CONF_GRID_CHARGE,
                var,
                REGISTER_GRID_CHARGE,
                BITMASK_GRID_CHARGE,
            )

        # Solar Sell (Register 145, Bit 0)
        if CONF_SOLAR_SELL in grid_config:
            await register_switch_entity(
                grid_config,
                CONF_SOLAR_SELL,
                var,
                REGISTER_SOLAR_SELL,
                BITMASK_SOLAR_SELL,
            )

        # Grid Peak Shaving (Register 178, Bits 4-5)
        if CONF_GRID_PEAK_SHAVING in grid_config:
            await register_switch_entity_2bit(
                grid_config,
                CONF_GRID_PEAK_SHAVING,
                var,
                REGISTER_GRID_PEAK_SHAVING,
                BITMASK_GRID_PEAK_SHAVING,
                VALUE_ENABLE_GRID_PEAK_SHAVING,
                VALUE_DISABLE_GRID_PEAK_SHAVING,
                SHIFT_GRID_PEAK_SHAVING,
            )

        # Gen Peak Shaving (Register 178, Bits 2-3)
        if CONF_GEN_PEAK_SHAVING in grid_config:
            await register_switch_entity_2bit(
                grid_config,
                CONF_GEN_PEAK_SHAVING,
                var,
                REGISTER_GEN_PEAK_SHAVING,
                BITMASK_GEN_PEAK_SHAVING,
                VALUE_ENABLE_GEN_PEAK_SHAVING,
                VALUE_DISABLE_GEN_PEAK_SHAVING,
                SHIFT_GEN_PEAK_SHAVING,
            )

        # On Grid Always On (Register 178, Bits 6-7)
        if CONF_ON_GRID_ALWAYS_ON in grid_config:
            await register_switch_entity_2bit(
                grid_config,
                CONF_ON_GRID_ALWAYS_ON,
                var,
                REGISTER_ON_GRID_ALWAYS_ON,
                BITMASK_ON_GRID_ALWAYS_ON,
                VALUE_ENABLE_ON_GRID_ALWAYS_ON,
                VALUE_DISABLE_ON_GRID_ALWAYS_ON,
                SHIFT_ON_GRID_ALWAYS_ON,
            )

        # Microinverter Export to Grid (Register 178, Bits 0-1)
        if CONF_MICROINVERTER_EXPORT_TO_GRID in grid_config:
            await register_switch_entity_2bit(
                grid_config,
                CONF_MICROINVERTER_EXPORT_TO_GRID,
                var,
                REGISTER_MICROINVERTER_EXPORT_TO_GRID,
                BITMASK_MICROINVERTER_EXPORT_TO_GRID,
                VALUE_ENABLE_MICROINVERTER_EXPORT,
                VALUE_DISABLE_MICROINVERTER_EXPORT,
                SHIFT_MICROINVERTER_EXPORT,
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
                REGISTER_EXTERNAL_CT_DIRECTION_CHECK,
                BITMASK_EXTERNAL_CT_DIRECTION_CHECK,
                VALUE_ENABLE_CT_DIRECTION_CHECK,
                VALUE_DISABLE_CT_DIRECTION_CHECK,
                SHIFT_CT_DIRECTION_CHECK,
            )

        # Solar Arc Fault Mode (Register 181, 1-bit)
        if CONF_SOLAR_ARC_FAULT_MODE in device_config:
            await register_switch_entity(
                device_config,
                CONF_SOLAR_ARC_FAULT_MODE,
                var,
                REGISTER_SOLAR_ARC_FAULT_MODE,
                BITMASK_SOLAR_ARC_FAULT_MODE,
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
                REGISTER_SYS_BEEPER,
                BITMASK_SYS_BEEPER,
            )

        # System LCD Backlight (Register 65, Bit 0)
        if CONF_SYS_LCD_BACKLIGHT in system_config:
            await register_switch_entity(
                system_config,
                CONF_SYS_LCD_BACKLIGHT,
                var,
                REGISTER_SYS_LCD_BACKLIGHT,
                BITMASK_SYS_LCD_BACKLIGHT,
            )

        # System DST Enable (Register 66, Bit 0)
        if CONF_SYS_DST_ENABLE in system_config:
            await register_switch_entity(
                system_config,
                CONF_SYS_DST_ENABLE,
                var,
                REGISTER_SYS_DST_ENABLE,
                BITMASK_SYS_DST_ENABLE,
            )

        # System Remote Lock (Register 67, Bit 0)
        if CONF_SYS_REMOTE_LOCK in system_config:
            await register_switch_entity(
                system_config,
                CONF_SYS_REMOTE_LOCK,
                var,
                REGISTER_SYS_REMOTE_LOCK,
                BITMASK_SYS_REMOTE_LOCK,
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
                REGISTER_TIME_OF_USE,
                BITMASK_TIME_OF_USE,
            )

        # Time Point Solar/General Charge Enable switches (Registers 172-177, Bit 0)
        solar_charge_switches = [
            (CONF_TIME_POINT_1_CHARGE_ENABLE, REGISTER_TIME_POINT_1_CHARGE),
            (CONF_TIME_POINT_2_CHARGE_ENABLE, REGISTER_TIME_POINT_2_CHARGE),
            (CONF_TIME_POINT_3_CHARGE_ENABLE, REGISTER_TIME_POINT_3_CHARGE),
            (CONF_TIME_POINT_4_CHARGE_ENABLE, REGISTER_TIME_POINT_4_CHARGE),
            (CONF_TIME_POINT_5_CHARGE_ENABLE, REGISTER_TIME_POINT_5_CHARGE),
            (CONF_TIME_POINT_6_CHARGE_ENABLE, REGISTER_TIME_POINT_6_CHARGE),
        ]
        for conf_key, register_addr in solar_charge_switches:
            if conf_key in tou_config:
                await register_switch_entity(
                    tou_config,
                    conf_key,
                    var,
                    register_addr,
                    BITMASK_CHARGE_ENABLE_SOLAR,
                )

        # Time Point Grid Charge Enable switches (Registers 172-177, Bit 1)
        grid_charge_switches = [
            (CONF_TIME_POINT_1_GRID_CHARGE_ENABLE, REGISTER_TIME_POINT_1_CHARGE),
            (CONF_TIME_POINT_2_GRID_CHARGE_ENABLE, REGISTER_TIME_POINT_2_CHARGE),
            (CONF_TIME_POINT_3_GRID_CHARGE_ENABLE, REGISTER_TIME_POINT_3_CHARGE),
            (CONF_TIME_POINT_4_GRID_CHARGE_ENABLE, REGISTER_TIME_POINT_4_CHARGE),
            (CONF_TIME_POINT_5_GRID_CHARGE_ENABLE, REGISTER_TIME_POINT_5_CHARGE),
            (CONF_TIME_POINT_6_GRID_CHARGE_ENABLE, REGISTER_TIME_POINT_6_CHARGE),
        ]
        for conf_key, register_addr in grid_charge_switches:
            if conf_key in tou_config:
                await register_switch_entity(
                    tou_config,
                    conf_key,
                    var,
                    register_addr,
                    BITMASK_CHARGE_ENABLE_GRID,
                )

        # Time Point Generator Charge Enable switches (Registers 172-177, Bit 2)
        gen_charge_switches = [
            (CONF_TIME_POINT_1_GEN_CHARGE_ENABLE, REGISTER_TIME_POINT_1_CHARGE),
            (CONF_TIME_POINT_2_GEN_CHARGE_ENABLE, REGISTER_TIME_POINT_2_CHARGE),
            (CONF_TIME_POINT_3_GEN_CHARGE_ENABLE, REGISTER_TIME_POINT_3_CHARGE),
            (CONF_TIME_POINT_4_GEN_CHARGE_ENABLE, REGISTER_TIME_POINT_4_CHARGE),
            (CONF_TIME_POINT_5_GEN_CHARGE_ENABLE, REGISTER_TIME_POINT_5_CHARGE),
            (CONF_TIME_POINT_6_GEN_CHARGE_ENABLE, REGISTER_TIME_POINT_6_CHARGE),
        ]
        for conf_key, register_addr in gen_charge_switches:
            if conf_key in tou_config:
                await register_switch_entity(
                    tou_config,
                    conf_key,
                    var,
                    register_addr,
                    BITMASK_CHARGE_ENABLE_GEN,
                )

        # Weekday Enable switches (Register 146, Bits 1-7)
        weekday_switches = [
            (CONF_WEEKDAY_MONDAY, BITMASK_WEEKDAY_MONDAY),
            (CONF_WEEKDAY_TUESDAY, BITMASK_WEEKDAY_TUESDAY),
            (CONF_WEEKDAY_WEDNESDAY, BITMASK_WEEKDAY_WEDNESDAY),
            (CONF_WEEKDAY_THURSDAY, BITMASK_WEEKDAY_THURSDAY),
            (CONF_WEEKDAY_FRIDAY, BITMASK_WEEKDAY_FRIDAY),
            (CONF_WEEKDAY_SATURDAY, BITMASK_WEEKDAY_SATURDAY),
            (CONF_WEEKDAY_SUNDAY, BITMASK_WEEKDAY_SUNDAY),
        ]
        for conf_key, bitmask in weekday_switches:
            if conf_key in tou_config:
                await register_switch_entity(
                    tou_config,
                    conf_key,
                    var,
                    REGISTER_TIME_OF_USE_WEEKDAYS,
                    bitmask,
                )

    # Settings Working Mode - Forced Off Grid Work (Register 179, Bits 2-3)
    if CONF_SETTINGS_WORKING_MODE in config:
        working_mode_config = config[CONF_SETTINGS_WORKING_MODE]
        if CONF_FORCED_OFF_GRID_WORK in working_mode_config:
            await register_switch_entity_2bit(
                working_mode_config,
                CONF_FORCED_OFF_GRID_WORK,
                var,
                REGISTER_FORCED_OFF_GRID_WORK,
                BITMASK_FORCED_OFF_GRID_WORK,
                VALUE_ENABLE_FORCED_OFF_GRID,
                VALUE_DISABLE_FORCED_OFF_GRID,
                SHIFT_FORCED_OFF_GRID,
            )

    # Settings Battery - Battery Loss Report Fault (Register 178, Bits 10-11)
    if CONF_SETTINGS_BATTERY in config:
        battery_config = config[CONF_SETTINGS_BATTERY]
        if CONF_BATTERY_LOSS_REPORT_FAULT in battery_config:
            await register_switch_entity_2bit(
                battery_config,
                CONF_BATTERY_LOSS_REPORT_FAULT,
                var,
                REGISTER_BATTERY_LOSS_REPORT_FAULT,
                BITMASK_BATTERY_LOSS_REPORT_FAULT,
                VALUE_ENABLE_BATTERY_LOSS_FAULT,
                VALUE_DISABLE_BATTERY_LOSS_FAULT,
                SHIFT_BATTERY_LOSS_FAULT,
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
                REGISTER_EXTERNAL_RELAY,
                BITMASK_EXTERNAL_RELAY,
                VALUE_ENABLE_EXTERNAL_RELAY,
                VALUE_DISABLE_EXTERNAL_RELAY,
                SHIFT_EXTERNAL_RELAY,
            )

        # Gen Port Force On (Register 132, Bit 0)
        if CONF_GEN_PORT_FORCE_ON in generator_config:
            await register_switch_entity(
                generator_config,
                CONF_GEN_PORT_FORCE_ON,
                var,
                REGISTER_GEN_PORT_FORCE_ON,
                BITMASK_GEN_PORT_FORCE_ON,
            )
