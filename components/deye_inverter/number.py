import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import (
    CONF_ID,
    UNIT_AMPERE,
    UNIT_VOLT,
    UNIT_PERCENT,
    UNIT_MINUTE,
    UNIT_HOUR,
    UNIT_SECOND,
    UNIT_HERTZ,
    UNIT_WATT,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_FREQUENCY,
)

from . import (
    CONF_DEYE_INVERTER_ID,
    CONF_DEVICE_ID,
    DeyeInverter,
)

# Namespace for DeyeNumber
DeyeNumber = cg.esphome_ns.namespace("deye_inverter").class_(
    "DeyeNumber", number.Number, cg.Component
)

# =============================================================================
# CONF CONSTANTS FOR NUMBER
# =============================================================================

# Settings Battery (currents)
CONF_MAX_CHARGE_CURRENT = "max_charge_current"
CONF_MAX_DISCHARGE_CURRENT = "max_discharge_current"

# Settings Battery Voltage group
CONF_EQUALIZATION_VOLTAGE = "equalization_voltage"
CONF_ABSORPTION_VOLTAGE = "absorption_voltage"
CONF_FLOAT_VOLTAGE = "float_voltage"
CONF_EMPTY_VOLTAGE = "empty_voltage"
CONF_SHUTDOWN_VOLTAGE = "shutdown_voltage"
CONF_RESTART_VOLTAGE = "restart_voltage"
CONF_LOW_VOLTAGE_WARNING = "low_voltage_warning"

# Settings Battery SOC group
CONF_SHUTDOWN_SOC = "shutdown_soc"
CONF_RESTART_SOC = "restart_soc"
CONF_LOW_SOC_WARNING = "low_soc_warning"

# Settings Battery Additional
CONF_BATTERY_CAPACITY_AH = "battery_capacity_ah"
CONF_EQUALIZATION_DAY_CYCLE = "equalization_day_cycle"
CONF_EQUALIZATION_TIME = "equalization_time"
CONF_TEMPCO = "tempco"
CONF_BATTERY_WAKE_UP = "battery_wake_up"
CONF_BATTERY_RESISTANCE = "battery_resistance"
CONF_BATTERY_CHARGING_EFFICIENCY = "battery_charging_efficiency"

# Settings Generator group
CONF_GEN_MAX_RUN_TIME = "gen_max_run_time"
CONF_GEN_COOLDOWN_TIME = "gen_cooldown_time"
CONF_GEN_MIN_POWER = "gen_min_power"
CONF_GEN_START_VOLTAGE = "gen_start_voltage"
CONF_GEN_START_SOC = "gen_start_soc"
CONF_GEN_CHARGING_CURRENT = "gen_charging_current"
CONF_GEN_ENABLE = "gen_enable"

# Settings Generator 2 group
CONF_GEN_MAX_TIME = "gen_max_time"
CONF_GEN_COOLDOWN = "gen_cooldown"
CONF_GEN_START_VOLTAGE_225 = "gen_start_voltage_225"
CONF_GEN_START_SOC_226 = "gen_start_soc_226"
CONF_GEN_CHARGE_CURRENT_227 = "gen_charge_current_227"

# Settings Smart Load
CONF_SMART_LOAD_OFF_VOLTAGE = "smart_load_off_voltage"
CONF_SMART_LOAD_OFF_SOC = "smart_load_off_capacity_soc"
CONF_SMART_LOAD_ON_VOLTAGE = "smart_load_on_voltage"
CONF_SMART_LOAD_ON_SOC = "smart_load_on_capacity_soc"

# Settings Grid Charge
CONF_MAXIMUM_BATTERY_GRID_CHARGE_CURRENT = "maximum_battery_grid_charge_current"
CONF_GRID_CHARGE_START_VOLTAGE = "grid_charge_start_voltage"
CONF_GRID_CHARGE_START_SOC = "grid_charge_start_soc"
CONF_GRID_CHARGE_CURRENT = "grid_charge_current"

# Settings Grid Numbers (distributed from settings_special)
CONF_ZERO_EXPORT_POWER = "zero_export_power"
CONF_MAX_SOLAR_SELL_POWER = "max_solar_sell_power"
CONF_GRID_MAX_POWER = "grid_max_power"
CONF_RESTORE_CONNECTION_TIME = "restore_connection_time"

# Settings Generator Numbers (distributed from settings_special)
CONF_GEN_PORT_COUPLE_FREQ_LIMIT = "gen_port_couple_freq_limit"
CONF_GENERATOR_REQUIRED_POWER_START = "generator_required_power_start"

# Settings Time of Use (start times moved to datetime.py)
CONF_TIME_POINT_1_POWER = "time_point_1_power"
CONF_TIME_POINT_2_POWER = "time_point_2_power"
CONF_TIME_POINT_3_POWER = "time_point_3_power"
CONF_TIME_POINT_4_POWER = "time_point_4_power"
CONF_TIME_POINT_5_POWER = "time_point_5_power"
CONF_TIME_POINT_6_POWER = "time_point_6_power"

CONF_TIME_POINT_1_MIN_BATTERY_VOLTAGE = "time_point_1_min_battery_voltage"
CONF_TIME_POINT_2_MIN_BATTERY_VOLTAGE = "time_point_2_min_battery_voltage"
CONF_TIME_POINT_3_MIN_BATTERY_VOLTAGE = "time_point_3_min_battery_voltage"
CONF_TIME_POINT_4_MIN_BATTERY_VOLTAGE = "time_point_4_min_battery_voltage"
CONF_TIME_POINT_5_MIN_BATTERY_VOLTAGE = "time_point_5_min_battery_voltage"
CONF_TIME_POINT_6_MIN_BATTERY_VOLTAGE = "time_point_6_min_battery_voltage"

CONF_TIME_POINT_1_CAPACITY = "time_point_1_capacity"
CONF_TIME_POINT_2_CAPACITY = "time_point_2_capacity"
CONF_TIME_POINT_3_CAPACITY = "time_point_3_capacity"
CONF_TIME_POINT_4_CAPACITY = "time_point_4_capacity"
CONF_TIME_POINT_5_CAPACITY = "time_point_5_capacity"
CONF_TIME_POINT_6_CAPACITY = "time_point_6_capacity"

# Settings System Numbers (NEW - registers 60-97)
CONF_SYS_SELF_CHECK_TIME = "sys_self_check_time"  # Register 61: [0,1000] seconds
CONF_SYS_INSULATION_RESISTANCE = (
    "sys_insulation_resistance"  # Register 65: [100,20000] (0.1KΩ)
)

# Settings Grid Protection Numbers (NEW - registers 185-200)
CONF_GP_OVER_VOLTAGE_PROTECTION = "gp_over_voltage_protection"
CONF_GP_UNDER_VOLTAGE_PROTECTION = "gp_under_voltage_protection"
CONF_GP_OVER_FREQUENCY_PROTECTION = "gp_over_frequency_protection"
CONF_GP_UNDER_FREQUENCY_PROTECTION = "gp_under_frequency_protection"
CONF_GP_VOLTAGE_RECONNECT = "gp_voltage_reconnect"
CONF_GP_FREQUENCY_RECONNECT = "gp_frequency_reconnect"
CONF_GP_RECONNECT_TIME = "gp_reconnect_time"
CONF_GP_RAMP_RATE = "gp_ramp_rate"
CONF_GP_STARTUP_TIME = "gp_startup_time"

# Settings California Numbers (NEW - registers 340-499)
CONF_CA_VOLTAGE_POINT_1 = "ca_voltage_point_1"
CONF_CA_VOLTAGE_POINT_2 = "ca_voltage_point_2"
CONF_CA_VOLTAGE_POINT_3 = "ca_voltage_point_3"
CONF_CA_VOLTAGE_POINT_4 = "ca_voltage_point_4"
CONF_CA_VOLTAGE_POINT_5 = "ca_voltage_point_5"
CONF_CA_VOLTAGE_POINT_6 = "ca_voltage_point_6"

CONF_CA_POWER_POINT_1 = "ca_power_point_1"
CONF_CA_POWER_POINT_2 = "ca_power_point_2"
CONF_CA_POWER_POINT_3 = "ca_power_point_3"
CONF_CA_POWER_POINT_4 = "ca_power_point_4"
CONF_CA_POWER_POINT_5 = "ca_power_point_5"
CONF_CA_POWER_POINT_6 = "ca_power_point_6"

CONF_CA_RAMP_RATE = "ca_ramp_rate"
CONF_CA_RECONNECT_TIME = "ca_reconnect_time"

# Settings Group Keys
CONF_SETTINGS_BATTERY = "settings_battery"
CONF_SETTINGS_BATTERY_VOLTAGE = "settings_battery_voltage"
CONF_SETTINGS_BATTERY_SOC = "settings_battery_soc"
CONF_SETTINGS_BATTERY_ADDITIONAL = "settings_battery_additional"
CONF_SETTINGS_GENERATOR = "settings_generator"
CONF_SETTINGS_GENERATOR_2 = "settings_generator_2"
CONF_SETTINGS_SMART_LOAD = "settings_smart_load"
CONF_SETTINGS_GRID_CHARGE = "settings_grid_charge"
CONF_SETTINGS_GRID = "settings_grid"
CONF_SETTINGS_TIME_OF_USE_NUMBERS = "settings_time_of_use_numbers"
CONF_SETTINGS_SYSTEM_NUMBERS = "settings_system_numbers"
CONF_SETTINGS_GRID_PROTECTION = "settings_grid_protection"
CONF_SETTINGS_CALIFORNIA = "settings_california"


# =============================================================================
# SCHEMA DEFINITIONS
# =============================================================================


# Helper schema that creates number schema with DeyeNumber class
def deye_number_schema(**kwargs):
    return number.number_schema(DeyeNumber, **kwargs)


# Settings Battery (Currents)
SETTINGS_BATTERY_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_MAX_CHARGE_CURRENT): deye_number_schema(
            unit_of_measurement=UNIT_AMPERE,
            device_class=DEVICE_CLASS_CURRENT,
        ),
        cv.Optional(CONF_MAX_DISCHARGE_CURRENT): deye_number_schema(
            unit_of_measurement=UNIT_AMPERE,
            device_class=DEVICE_CLASS_CURRENT,
        ),
    }
)

# Settings Battery Voltage
SETTINGS_BATTERY_VOLTAGE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EQUALIZATION_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_ABSORPTION_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_FLOAT_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_EMPTY_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_SHUTDOWN_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_RESTART_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_LOW_VOLTAGE_WARNING): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
    }
)

# Settings Battery SOC
SETTINGS_BATTERY_SOC_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SHUTDOWN_SOC): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_RESTART_SOC): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_LOW_SOC_WARNING): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
    }
)

# Settings Battery Additional
SETTINGS_BATTERY_ADDITIONAL_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_CAPACITY_AH): deye_number_schema(
            unit_of_measurement="Ah",
        ),
        cv.Optional(CONF_EQUALIZATION_DAY_CYCLE): deye_number_schema(
            unit_of_measurement="Tage",
        ),
        cv.Optional(CONF_EQUALIZATION_TIME): deye_number_schema(
            unit_of_measurement=UNIT_HOUR,
        ),
        cv.Optional(CONF_TEMPCO): deye_number_schema(
            unit_of_measurement="mV/°C",
        ),
        cv.Optional(CONF_BATTERY_WAKE_UP): deye_number_schema(),
        cv.Optional(CONF_BATTERY_RESISTANCE): deye_number_schema(
            unit_of_measurement="mΩ",
        ),
        cv.Optional(CONF_BATTERY_CHARGING_EFFICIENCY): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
        ),
    }
)

# Settings Generator
SETTINGS_GENERATOR_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_MAX_RUN_TIME): deye_number_schema(
            unit_of_measurement=UNIT_HOUR,
        ),
        cv.Optional(CONF_GEN_COOLDOWN_TIME): deye_number_schema(
            unit_of_measurement=UNIT_MINUTE,
        ),
        cv.Optional(CONF_GEN_MIN_POWER): deye_number_schema(
            unit_of_measurement="W",
            device_class=DEVICE_CLASS_POWER,
        ),
        cv.Optional(CONF_GEN_START_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_GEN_START_SOC): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_GEN_CHARGING_CURRENT): deye_number_schema(
            unit_of_measurement=UNIT_AMPERE,
            device_class=DEVICE_CLASS_CURRENT,
        ),
        cv.Optional(CONF_GEN_ENABLE): deye_number_schema(),
        cv.Optional(CONF_GENERATOR_REQUIRED_POWER_START): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
    }
)

# Settings Generator 2
SETTINGS_GENERATOR_2_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_MAX_TIME): deye_number_schema(
            unit_of_measurement=UNIT_HOUR,
        ),
        cv.Optional(CONF_GEN_COOLDOWN): deye_number_schema(
            unit_of_measurement=UNIT_HOUR,
        ),
        cv.Optional(CONF_GEN_START_VOLTAGE_225): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_GEN_START_SOC_226): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_GEN_CHARGE_CURRENT_227): deye_number_schema(
            unit_of_measurement=UNIT_AMPERE,
            device_class=DEVICE_CLASS_CURRENT,
        ),
    }
)

# Settings Smart Load
SETTINGS_SMART_LOAD_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SMART_LOAD_OFF_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_SMART_LOAD_OFF_SOC): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_SMART_LOAD_ON_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_SMART_LOAD_ON_SOC): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
    }
)

# Settings Grid Charge
SETTINGS_GRID_CHARGE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_MAXIMUM_BATTERY_GRID_CHARGE_CURRENT): deye_number_schema(
            unit_of_measurement=UNIT_AMPERE,
            device_class=DEVICE_CLASS_CURRENT,
        ),
        cv.Optional(CONF_GRID_CHARGE_START_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_GRID_CHARGE_START_SOC): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_GRID_CHARGE_CURRENT): deye_number_schema(
            unit_of_measurement=UNIT_AMPERE,
            device_class=DEVICE_CLASS_CURRENT,
        ),
    }
)

# Settings Grid Numbers
SETTINGS_GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_ZERO_EXPORT_POWER): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
        ),
        cv.Optional(CONF_MAX_SOLAR_SELL_POWER): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
        cv.Optional(CONF_GRID_MAX_POWER): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
        cv.Optional(CONF_RESTORE_CONNECTION_TIME): deye_number_schema(
            unit_of_measurement=UNIT_SECOND,
        ),
    }
)

# Settings Time of Use Numbers
SETTINGS_TIME_OF_USE_NUMBERS_SCHEMA = cv.Schema(
    {
        # Time Point Power values (addresses 154-159)
        cv.Optional(CONF_TIME_POINT_1_POWER): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
        cv.Optional(CONF_TIME_POINT_2_POWER): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
        cv.Optional(CONF_TIME_POINT_3_POWER): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
        cv.Optional(CONF_TIME_POINT_4_POWER): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
        cv.Optional(CONF_TIME_POINT_5_POWER): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
        cv.Optional(CONF_TIME_POINT_6_POWER): deye_number_schema(
            unit_of_measurement=UNIT_WATT,
            device_class=DEVICE_CLASS_POWER,
        ),
        # Time Point Min Battery Voltage (addresses 160-165)
        cv.Optional(CONF_TIME_POINT_1_MIN_BATTERY_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_TIME_POINT_2_MIN_BATTERY_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_TIME_POINT_3_MIN_BATTERY_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_TIME_POINT_4_MIN_BATTERY_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_TIME_POINT_5_MIN_BATTERY_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_TIME_POINT_6_MIN_BATTERY_VOLTAGE): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        # Time Point Capacity (addresses 166-171)
        cv.Optional(CONF_TIME_POINT_1_CAPACITY): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_TIME_POINT_2_CAPACITY): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_TIME_POINT_3_CAPACITY): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_TIME_POINT_4_CAPACITY): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_TIME_POINT_5_CAPACITY): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
        cv.Optional(CONF_TIME_POINT_6_CAPACITY): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
            device_class=DEVICE_CLASS_BATTERY,
        ),
    }
)

# Settings System Numbers
SETTINGS_SYSTEM_NUMBERS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SYS_SELF_CHECK_TIME): deye_number_schema(
            unit_of_measurement=UNIT_SECOND,
        ),
        cv.Optional(CONF_SYS_INSULATION_RESISTANCE): deye_number_schema(
            unit_of_measurement="0.1kΩ",
        ),
    }
)

# Settings Grid Protection Numbers
SETTINGS_GRID_PROTECTION_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GP_OVER_VOLTAGE_PROTECTION): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_GP_UNDER_VOLTAGE_PROTECTION): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_GP_OVER_FREQUENCY_PROTECTION): deye_number_schema(
            unit_of_measurement=UNIT_HERTZ,
            device_class=DEVICE_CLASS_FREQUENCY,
        ),
        cv.Optional(CONF_GP_UNDER_FREQUENCY_PROTECTION): deye_number_schema(
            unit_of_measurement=UNIT_HERTZ,
            device_class=DEVICE_CLASS_FREQUENCY,
        ),
        cv.Optional(CONF_GP_VOLTAGE_RECONNECT): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_GP_FREQUENCY_RECONNECT): deye_number_schema(
            unit_of_measurement=UNIT_HERTZ,
            device_class=DEVICE_CLASS_FREQUENCY,
        ),
        cv.Optional(CONF_GP_RECONNECT_TIME): deye_number_schema(
            unit_of_measurement=UNIT_SECOND,
        ),
        cv.Optional(CONF_GP_RAMP_RATE): deye_number_schema(
            unit_of_measurement="%/s",
        ),
        cv.Optional(CONF_GP_STARTUP_TIME): deye_number_schema(
            unit_of_measurement=UNIT_SECOND,
        ),
    }
)

# Settings California Numbers
SETTINGS_CALIFORNIA_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_CA_VOLTAGE_POINT_1): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_CA_VOLTAGE_POINT_2): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_CA_VOLTAGE_POINT_3): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_CA_VOLTAGE_POINT_4): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_CA_VOLTAGE_POINT_5): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_CA_VOLTAGE_POINT_6): deye_number_schema(
            unit_of_measurement=UNIT_VOLT,
            device_class=DEVICE_CLASS_VOLTAGE,
        ),
        cv.Optional(CONF_CA_POWER_POINT_1): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
        ),
        cv.Optional(CONF_CA_POWER_POINT_2): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
        ),
        cv.Optional(CONF_CA_POWER_POINT_3): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
        ),
        cv.Optional(CONF_CA_POWER_POINT_4): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
        ),
        cv.Optional(CONF_CA_POWER_POINT_5): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
        ),
        cv.Optional(CONF_CA_POWER_POINT_6): deye_number_schema(
            unit_of_measurement=UNIT_PERCENT,
        ),
        cv.Optional(CONF_CA_RAMP_RATE): deye_number_schema(
            unit_of_measurement="%/s",
        ),
        cv.Optional(CONF_CA_RECONNECT_TIME): deye_number_schema(
            unit_of_measurement=UNIT_SECOND,
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
        cv.Optional(CONF_SETTINGS_BATTERY): SETTINGS_BATTERY_SCHEMA,
        cv.Optional(CONF_SETTINGS_BATTERY_VOLTAGE): SETTINGS_BATTERY_VOLTAGE_SCHEMA,
        cv.Optional(CONF_SETTINGS_BATTERY_SOC): SETTINGS_BATTERY_SOC_SCHEMA,
        cv.Optional(
            CONF_SETTINGS_BATTERY_ADDITIONAL
        ): SETTINGS_BATTERY_ADDITIONAL_SCHEMA,
        cv.Optional(CONF_SETTINGS_GENERATOR): SETTINGS_GENERATOR_SCHEMA,
        cv.Optional(CONF_SETTINGS_GENERATOR_2): SETTINGS_GENERATOR_2_SCHEMA,
        cv.Optional(CONF_SETTINGS_SMART_LOAD): SETTINGS_SMART_LOAD_SCHEMA,
        cv.Optional(CONF_SETTINGS_GRID_CHARGE): SETTINGS_GRID_CHARGE_SCHEMA,
        cv.Optional(CONF_SETTINGS_GRID): SETTINGS_GRID_SCHEMA,
        cv.Optional(
            CONF_SETTINGS_TIME_OF_USE_NUMBERS
        ): SETTINGS_TIME_OF_USE_NUMBERS_SCHEMA,
        cv.Optional(CONF_SETTINGS_SYSTEM_NUMBERS): SETTINGS_SYSTEM_NUMBERS_SCHEMA,
        cv.Optional(CONF_SETTINGS_GRID_PROTECTION): SETTINGS_GRID_PROTECTION_SCHEMA,
        cv.Optional(CONF_SETTINGS_CALIFORNIA): SETTINGS_CALIFORNIA_SCHEMA,
    }
)


# =============================================================================
# HELPER FUNCTIONS FOR to_code
# =============================================================================


async def register_number_entity(
    config, key, parent, address, min_value, max_value, step, scale, device_obj=None
):
    """Register a single number entity with the parent component."""
    if key not in config:
        return

    conf = config[key]
    # Create DeyeNumber instead of base number
    num = cg.new_Pvariable(conf[CONF_ID])
    await number.register_number(
        num, conf, min_value=min_value, max_value=max_value, step=step
    )
    cg.add(num.set_parent(parent))
    cg.add(num.set_address(address))
    cg.add(num.set_scale(scale))

    # Register with parent's number list
    cg.add(parent.register_number(num))

    # Set device for Home Assistant grouping
    if device_obj is not None:
        cg.add(num.set_device(device_obj))


# =============================================================================
# CODE GENERATION
# =============================================================================


async def to_code(config):
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Handle device_id for Home Assistant grouping
    from . import get_or_create_device

    device_id = config.get(CONF_DEVICE_ID)
    device_obj = await get_or_create_device(device_id)

    # Settings Battery (Currents)
    if CONF_SETTINGS_BATTERY in config:
        battery_config = config[CONF_SETTINGS_BATTERY]

        # Max Charge Current (Register 108, 0-185A, step 0.1, scale 10)
        if CONF_MAX_CHARGE_CURRENT in battery_config:
            await register_number_entity(
                battery_config,
                CONF_MAX_CHARGE_CURRENT,
                var,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_BATTERY_MAX_CHARGE_CURRENT"
                ),
                cg.RawExpression(
                    "esphome::deye_inverter::MIN_BATTERY_MAX_CHARGE_CURRENT"
                ),
                cg.RawExpression(
                    "esphome::deye_inverter::MAX_BATTERY_MAX_CHARGE_CURRENT"
                ),
                cg.RawExpression(
                    "esphome::deye_inverter::STEP_BATTERY_MAX_CHARGE_CURRENT"
                ),
                cg.RawExpression(
                    "esphome::deye_inverter::SCALE_BATTERY_MAX_CHARGE_CURRENT"
                ),
                device_obj,
            )

        # Max Discharge Current (Register 109, 0-185A, step 0.1, scale 10)
        if CONF_MAX_DISCHARGE_CURRENT in battery_config:
            await register_number_entity(
                battery_config,
                CONF_MAX_DISCHARGE_CURRENT,
                var,
                cg.RawExpression(
                    "esphome::deye_inverter::REG_BATTERY_MAX_DISCHARGE_CURRENT"
                ),
                cg.RawExpression(
                    "esphome::deye_inverter::MIN_BATTERY_MAX_DISCHARGE_CURRENT"
                ),
                cg.RawExpression(
                    "esphome::deye_inverter::MAX_BATTERY_MAX_DISCHARGE_CURRENT"
                ),
                cg.RawExpression(
                    "esphome::deye_inverter::STEP_BATTERY_MAX_DISCHARGE_CURRENT"
                ),
                cg.RawExpression(
                    "esphome::deye_inverter::SCALE_BATTERY_MAX_DISCHARGE_CURRENT"
                ),
                device_obj,
            )

    # Settings Battery Voltage
    if CONF_SETTINGS_BATTERY_VOLTAGE in config:
        voltage_config = config[CONF_SETTINGS_BATTERY_VOLTAGE]

        voltage_registers = [
            (CONF_EQUALIZATION_VOLTAGE, "REG_BATTERY_EQUALIZATION_VOLTAGE"),
            (CONF_ABSORPTION_VOLTAGE, "REG_BATTERY_ABSORPTION_VOLTAGE"),
            (CONF_FLOAT_VOLTAGE, "REG_BATTERY_FLOAT_VOLTAGE"),
            (CONF_EMPTY_VOLTAGE, "REG_BATTERY_EMPTY_VOLTAGE"),
            (CONF_SHUTDOWN_VOLTAGE, "REG_BATTERY_SHUTDOWN_VOLTAGE"),
            (CONF_RESTART_VOLTAGE, "REG_BATTERY_RESTART_VOLTAGE"),
            (CONF_LOW_VOLTAGE_WARNING, "REG_BATTERY_LOW_VOLTAGE_WARNING"),
        ]
        for key, reg_name in voltage_registers:
            if key in voltage_config:
                await register_number_entity(
                    voltage_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression("esphome::deye_inverter::MIN_BATTERY_VOLTAGE"),
                    cg.RawExpression("esphome::deye_inverter::MAX_BATTERY_VOLTAGE"),
                    cg.RawExpression("esphome::deye_inverter::STEP_BATTERY_VOLTAGE"),
                    cg.RawExpression("esphome::deye_inverter::SCALE_BATTERY_VOLTAGE"),
                    device_obj,
                )

    # Settings Battery SOC
    if CONF_SETTINGS_BATTERY_SOC in config:
        soc_config = config[CONF_SETTINGS_BATTERY_SOC]

        soc_registers = [
            (CONF_SHUTDOWN_SOC, "REG_BATTERY_SHUTDOWN_SOC"),
            (CONF_RESTART_SOC, "REG_BATTERY_RESTART_SOC"),
            (CONF_LOW_SOC_WARNING, "REG_BATTERY_LOW_SOC_WARNING"),
        ]
        for key, reg_name in soc_registers:
            if key in soc_config:
                await register_number_entity(
                    soc_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression("esphome::deye_inverter::MIN_BATTERY_SOC"),
                    cg.RawExpression("esphome::deye_inverter::MAX_BATTERY_SOC"),
                    cg.RawExpression("esphome::deye_inverter::STEP_BATTERY_SOC"),
                    cg.RawExpression("esphome::deye_inverter::SCALE_BATTERY_SOC"),
                    device_obj,
                )

    # Settings Battery Additional
    if CONF_SETTINGS_BATTERY_ADDITIONAL in config:
        additional_config = config[CONF_SETTINGS_BATTERY_ADDITIONAL]

        additional_registers = [
            (
                CONF_BATTERY_CAPACITY_AH,
                "REG_BATTERY_CAPACITY",
                "MIN_BATTERY_CAPACITY",
                "MAX_BATTERY_CAPACITY",
                "STEP_BATTERY_CAPACITY",
                "SCALE_BATTERY_CAPACITY",
            ),
            (
                CONF_EQUALIZATION_DAY_CYCLE,
                "REG_BATTERY_EQUALIZATION_DAY_CYCLE",
                "MIN_BATTERY_EQUALIZATION_DAY_CYCLE",
                "MAX_BATTERY_EQUALIZATION_DAY_CYCLE",
                "STEP_BATTERY_EQUALIZATION_DAY_CYCLE",
                "SCALE_BATTERY_EQUALIZATION_DAY_CYCLE",
            ),
            (
                CONF_EQUALIZATION_TIME,
                "REG_BATTERY_EQUALIZATION_TIME",
                "MIN_BATTERY_EQUALIZATION_TIME",
                "MAX_BATTERY_EQUALIZATION_TIME",
                "STEP_BATTERY_EQUALIZATION_TIME",
                "SCALE_BATTERY_EQUALIZATION_TIME",
            ),
            (
                CONF_TEMPCO,
                "REG_BATTERY_TEMPCO",
                "MIN_BATTERY_TEMPCO",
                "MAX_BATTERY_TEMPCO",
                "STEP_BATTERY_TEMPCO",
                "SCALE_BATTERY_TEMPCO",
            ),
            (
                CONF_BATTERY_WAKE_UP,
                "REG_BATTERY_WAKE_UP",
                "MIN_BATTERY_WAKE_UP",
                "MAX_BATTERY_WAKE_UP",
                "STEP_BATTERY_WAKE_UP",
                "SCALE_BATTERY_WAKE_UP",
            ),
            (
                CONF_BATTERY_RESISTANCE,
                "REG_BATTERY_RESISTANCE",
                "MIN_BATTERY_RESISTANCE",
                "MAX_BATTERY_RESISTANCE",
                "STEP_BATTERY_RESISTANCE",
                "SCALE_BATTERY_RESISTANCE",
            ),
            (
                CONF_BATTERY_CHARGING_EFFICIENCY,
                "REG_BATTERY_CHARGING_EFFICIENCY",
                "MIN_BATTERY_CHARGING_EFFICIENCY",
                "MAX_BATTERY_CHARGING_EFFICIENCY",
                "STEP_BATTERY_CHARGING_EFFICIENCY",
                "SCALE_BATTERY_CHARGING_EFFICIENCY",
            ),
        ]
        for (
            key,
            reg_name,
            min_name,
            max_name,
            step_name,
            scale_name,
        ) in additional_registers:
            if key in additional_config:
                await register_number_entity(
                    additional_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )

    # Settings Generator
    if CONF_SETTINGS_GENERATOR in config:
        gen_config = config[CONF_SETTINGS_GENERATOR]

        gen_registers = [
            (
                CONF_GEN_MAX_RUN_TIME,
                "REG_GENERATOR_MAX_RUN_TIME",
                "MIN_GEN_MAX_RUN_TIME",
                "MAX_GEN_MAX_RUN_TIME",
                "STEP_GEN_MAX_RUN_TIME",
                "SCALE_GEN_MAX_RUN_TIME",
            ),
            (
                CONF_GEN_COOLDOWN_TIME,
                "REG_GENERATOR_COOLDOWN_TIME",
                "MIN_GEN_COOLDOWN_TIME",
                "MAX_GEN_COOLDOWN_TIME",
                "STEP_GEN_COOLDOWN_TIME",
                "SCALE_GEN_COOLDOWN_TIME",
            ),
            (
                CONF_GEN_MIN_POWER,
                "REG_GENERATOR_MIN_POWER",
                "MIN_GEN_MIN_POWER",
                "MAX_GEN_MIN_POWER",
                "STEP_GEN_MIN_POWER",
                "SCALE_GEN_MIN_POWER",
            ),
            (
                CONF_GEN_START_VOLTAGE,
                "REG_GENERATOR_START_VOLTAGE",
                "MIN_GEN_START_VOLTAGE",
                "MAX_GEN_START_VOLTAGE",
                "STEP_GEN_START_VOLTAGE",
                "SCALE_GEN_START_VOLTAGE",
            ),
            (
                CONF_GEN_START_SOC,
                "REG_GENERATOR_START_SOC",
                "MIN_GEN_START_SOC",
                "MAX_GEN_START_SOC",
                "STEP_GEN_START_SOC",
                "SCALE_GEN_START_SOC",
            ),
            (
                CONF_GEN_CHARGING_CURRENT,
                "REG_GENERATOR_CHARGE_CURRENT",
                "MIN_GEN_CHARGING_CURRENT",
                "MAX_GEN_CHARGING_CURRENT",
                "STEP_GEN_CHARGING_CURRENT",
                "SCALE_GEN_CHARGING_CURRENT",
            ),
            (
                CONF_GEN_ENABLE,
                "REG_GENERATOR_ENABLE",
                "MIN_GEN_ENABLE",
                "MAX_GEN_ENABLE",
                "STEP_GEN_ENABLE",
                "SCALE_GEN_ENABLE",
            ),
        ]
        for key, reg_name, min_name, max_name, step_name, scale_name in gen_registers:
            if key in gen_config:
                await register_number_entity(
                    gen_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )

    # Settings Generator 2
    if CONF_SETTINGS_GENERATOR_2 in config:
        gen2_config = config[CONF_SETTINGS_GENERATOR_2]

        gen2_registers = [
            (
                CONF_GEN_MAX_TIME,
                "REG_GEN_MAX_TIME",
                "MIN_GEN_MAX_TIME",
                "MAX_GEN_MAX_TIME",
                "STEP_GEN_MAX_TIME",
                "SCALE_GEN_MAX_TIME",
            ),
            (
                CONF_GEN_COOLDOWN,
                "REG_GEN_COOLDOWN",
                "MIN_GEN_COOLDOWN",
                "MAX_GEN_COOLDOWN",
                "STEP_GEN_COOLDOWN",
                "SCALE_GEN_COOLDOWN",
            ),
            (
                CONF_GEN_START_VOLTAGE_225,
                "REG_GEN_START_VOLTAGE_225",
                "MIN_GEN_START_VOLTAGE_225",
                "MAX_GEN_START_VOLTAGE_225",
                "STEP_GEN_START_VOLTAGE_225",
                "SCALE_GEN_START_VOLTAGE_225",
            ),
            (
                CONF_GEN_START_SOC_226,
                "REG_GEN_START_SOC_226",
                "MIN_GEN_START_SOC_226",
                "MAX_GEN_START_SOC_226",
                "STEP_GEN_START_SOC_226",
                "SCALE_GEN_START_SOC_226",
            ),
            (
                CONF_GEN_CHARGE_CURRENT_227,
                "REG_GEN_CHARGE_CURRENT_227",
                "MIN_GEN_CHARGE_CURRENT_227",
                "MAX_GEN_CHARGE_CURRENT_227",
                "STEP_GEN_CHARGE_CURRENT_227",
                "SCALE_GEN_CHARGE_CURRENT_227",
            ),
        ]
        for key, reg_name, min_name, max_name, step_name, scale_name in gen2_registers:
            if key in gen2_config:
                await register_number_entity(
                    gen2_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )

    # Settings Smart Load
    if CONF_SETTINGS_SMART_LOAD in config:
        smart_load_config = config[CONF_SETTINGS_SMART_LOAD]

        smart_load_voltage_registers = [
            (CONF_SMART_LOAD_OFF_VOLTAGE, "REG_SMART_LOAD_OFF_VOLTAGE"),
            (CONF_SMART_LOAD_ON_VOLTAGE, "REG_SMART_LOAD_ON_VOLTAGE"),
        ]
        for key, reg_name in smart_load_voltage_registers:
            if key in smart_load_config:
                await register_number_entity(
                    smart_load_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression("esphome::deye_inverter::MIN_SMART_LOAD_VOLTAGE"),
                    cg.RawExpression("esphome::deye_inverter::MAX_SMART_LOAD_VOLTAGE"),
                    cg.RawExpression("esphome::deye_inverter::STEP_SMART_LOAD_VOLTAGE"),
                    cg.RawExpression(
                        "esphome::deye_inverter::SCALE_SMART_LOAD_VOLTAGE"
                    ),
                    device_obj,
                )

        smart_load_soc_registers = [
            (CONF_SMART_LOAD_OFF_SOC, "REG_SMART_LOAD_OFF_CAPACITY_SOC"),
            (CONF_SMART_LOAD_ON_SOC, "REG_SMART_LOAD_ON_CAPACITY_SOC"),
        ]
        for key, reg_name in smart_load_soc_registers:
            if key in smart_load_config:
                await register_number_entity(
                    smart_load_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression("esphome::deye_inverter::MIN_SMART_LOAD_SOC"),
                    cg.RawExpression("esphome::deye_inverter::MAX_SMART_LOAD_SOC"),
                    cg.RawExpression("esphome::deye_inverter::STEP_SMART_LOAD_SOC"),
                    cg.RawExpression("esphome::deye_inverter::SCALE_SMART_LOAD_SOC"),
                    device_obj,
                )

    # Settings Grid Charge
    if CONF_SETTINGS_GRID_CHARGE in config:
        grid_charge_config = config[CONF_SETTINGS_GRID_CHARGE]

        grid_charge_registers = [
            (
                CONF_MAXIMUM_BATTERY_GRID_CHARGE_CURRENT,
                "REG_MAX_BATTERY_GRID_CHARGE_CURRENT",
                "MIN_MAX_BATTERY_GRID_CHARGE_CURRENT",
                "MAX_MAX_BATTERY_GRID_CHARGE_CURRENT",
                "STEP_MAX_BATTERY_GRID_CHARGE_CURRENT",
                "SCALE_MAX_BATTERY_GRID_CHARGE_CURRENT",
            ),
            (
                CONF_GRID_CHARGE_START_VOLTAGE,
                "REG_GRID_CHARGE_START_V",
                "MIN_GRID_CHARGE_START_VOLTAGE",
                "MAX_GRID_CHARGE_START_VOLTAGE",
                "STEP_GRID_CHARGE_START_VOLTAGE",
                "SCALE_GRID_CHARGE_START_VOLTAGE",
            ),
            (
                CONF_GRID_CHARGE_START_SOC,
                "REG_GRID_CHARGE_START_SOC",
                "MIN_GRID_CHARGE_START_SOC",
                "MAX_GRID_CHARGE_START_SOC",
                "STEP_GRID_CHARGE_START_SOC",
                "SCALE_GRID_CHARGE_START_SOC",
            ),
            (
                CONF_GRID_CHARGE_CURRENT,
                "REG_GRID_CHARGE_CURRENT",
                "MIN_GRID_CHARGE_CURRENT",
                "MAX_GRID_CHARGE_CURRENT",
                "STEP_GRID_CHARGE_CURRENT",
                "SCALE_GRID_CHARGE_CURRENT",
            ),
        ]
        for (
            key,
            reg_name,
            min_name,
            max_name,
            step_name,
            scale_name,
        ) in grid_charge_registers:
            if key in grid_charge_config:
                await register_number_entity(
                    grid_charge_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )

    # Settings Grid Numbers (distributed from settings_special)
    if CONF_SETTINGS_GRID in config:
        grid_numbers_config = config[CONF_SETTINGS_GRID]

        grid_numbers_registers = [
            (
                CONF_ZERO_EXPORT_POWER,
                "REG_ZERO_EXPORT_POWER",
                "MIN_ZERO_EXPORT_POWER",
                "MAX_ZERO_EXPORT_POWER",
                "STEP_ZERO_EXPORT_POWER",
                "SCALE_ZERO_EXPORT_POWER",
            ),
            (
                CONF_MAX_SOLAR_SELL_POWER,
                "REG_MAX_SOLAR_SELL_POWER",
                "MIN_MAX_SOLAR_SELL_POWER",
                "MAX_MAX_SOLAR_SELL_POWER",
                "STEP_MAX_SOLAR_SELL_POWER",
                "SCALE_MAX_SOLAR_SELL_POWER",
            ),
            (
                CONF_GRID_MAX_POWER,
                "REG_MAX_SOLAR_POWER",
                "MIN_GRID_MAX_POWER",
                "MAX_GRID_MAX_POWER",
                "STEP_GRID_MAX_POWER",
                "SCALE_GRID_MAX_POWER",
            ),
            (
                CONF_RESTORE_CONNECTION_TIME,
                "REG_RESTORE_CONNECTION_TIME",
                "MIN_RESTORE_CONNECTION_TIME",
                "MAX_RESTORE_CONNECTION_TIME",
                "STEP_RESTORE_CONNECTION_TIME",
                "SCALE_RESTORE_CONNECTION_TIME",
            ),
        ]
        for (
            key,
            reg_name,
            min_name,
            max_name,
            step_name,
            scale_name,
        ) in grid_numbers_registers:
            if key in grid_numbers_config:
                await register_number_entity(
                    grid_numbers_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )

    # Settings Generator Numbers (distributed from settings_special)
    if CONF_SETTINGS_GENERATOR in config:
        gen_numbers_config = config[CONF_SETTINGS_GENERATOR]

        gen_numbers_registers = [
            (
                CONF_GEN_PORT_COUPLE_FREQ_LIMIT,
                "REG_GEN_PORT_COUPLE_FREQUENCY",
                "MIN_GEN_PORT_COUPLE_FREQ_LIMIT",
                "MAX_GEN_PORT_COUPLE_FREQ_LIMIT",
                "STEP_GEN_PORT_COUPLE_FREQ_LIMIT",
                "SCALE_GEN_PORT_COUPLE_FREQ_LIMIT",
            ),
            (
                CONF_GENERATOR_REQUIRED_POWER_START,
                "REG_GENERATOR_REQUIRED_POWER_START",
                "MIN_GENERATOR_REQUIRED_POWER_START",
                "MAX_GENERATOR_REQUIRED_POWER_START",
                "STEP_GENERATOR_REQUIRED_POWER_START",
                "SCALE_GENERATOR_REQUIRED_POWER_START",
            ),
        ]
        for (
            key,
            reg_name,
            min_name,
            max_name,
            step_name,
            scale_name,
        ) in gen_numbers_registers:
            if key in gen_numbers_config:
                await register_number_entity(
                    gen_numbers_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )

    # Settings Time of Use (start times moved to datetime.py)
    if CONF_SETTINGS_TIME_OF_USE_NUMBERS in config:
        tou_config = config[CONF_SETTINGS_TIME_OF_USE_NUMBERS]

        # Time Point Power values (addresses 154-159)
        tou_power_registers = [
            (CONF_TIME_POINT_1_POWER, "REG_TIME_POINT_1_POWER"),
            (CONF_TIME_POINT_2_POWER, "REG_TIME_POINT_2_POWER"),
            (CONF_TIME_POINT_3_POWER, "REG_TIME_POINT_3_POWER"),
            (CONF_TIME_POINT_4_POWER, "REG_TIME_POINT_4_POWER"),
            (CONF_TIME_POINT_5_POWER, "REG_TIME_POINT_5_POWER"),
            (CONF_TIME_POINT_6_POWER, "REG_TIME_POINT_6_POWER"),
        ]
        for key, reg_name in tou_power_registers:
            if key in tou_config:
                await register_number_entity(
                    tou_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression("esphome::deye_inverter::MIN_TIME_POINT_POWER"),
                    cg.RawExpression("esphome::deye_inverter::MAX_TIME_POINT_POWER"),
                    cg.RawExpression("esphome::deye_inverter::STEP_TIME_POINT_POWER"),
                    cg.RawExpression("esphome::deye_inverter::SCALE_TIME_POINT_POWER"),
                    device_obj,
                )

        # Time Point Min Battery Voltage (addresses 160-165)
        tou_voltage_registers = [
            (CONF_TIME_POINT_1_MIN_BATTERY_VOLTAGE, "REG_TIME_POINT_1_MIN_VOLTAGE"),
            (CONF_TIME_POINT_2_MIN_BATTERY_VOLTAGE, "REG_TIME_POINT_2_MIN_VOLTAGE"),
            (CONF_TIME_POINT_3_MIN_BATTERY_VOLTAGE, "REG_TIME_POINT_3_MIN_VOLTAGE"),
            (CONF_TIME_POINT_4_MIN_BATTERY_VOLTAGE, "REG_TIME_POINT_4_MIN_VOLTAGE"),
            (CONF_TIME_POINT_5_MIN_BATTERY_VOLTAGE, "REG_TIME_POINT_5_MIN_VOLTAGE"),
            (CONF_TIME_POINT_6_MIN_BATTERY_VOLTAGE, "REG_TIME_POINT_6_MIN_VOLTAGE"),
        ]
        for key, reg_name in tou_voltage_registers:
            if key in tou_config:
                await register_number_entity(
                    tou_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(
                        "esphome::deye_inverter::MIN_TIME_POINT_MIN_VOLTAGE"
                    ),
                    cg.RawExpression(
                        "esphome::deye_inverter::MAX_TIME_POINT_MIN_VOLTAGE"
                    ),
                    cg.RawExpression(
                        "esphome::deye_inverter::STEP_TIME_POINT_MIN_VOLTAGE"
                    ),
                    cg.RawExpression(
                        "esphome::deye_inverter::SCALE_TIME_POINT_MIN_VOLTAGE"
                    ),
                    device_obj,
                )

        # Time Point Capacity (addresses 166-171)
        tou_capacity_registers = [
            (CONF_TIME_POINT_1_CAPACITY, "REG_TIME_POINT_1_CAPACITY"),
            (CONF_TIME_POINT_2_CAPACITY, "REG_TIME_POINT_2_CAPACITY"),
            (CONF_TIME_POINT_3_CAPACITY, "REG_TIME_POINT_3_CAPACITY"),
            (CONF_TIME_POINT_4_CAPACITY, "REG_TIME_POINT_4_CAPACITY"),
            (CONF_TIME_POINT_5_CAPACITY, "REG_TIME_POINT_5_CAPACITY"),
            (CONF_TIME_POINT_6_CAPACITY, "REG_TIME_POINT_6_CAPACITY"),
        ]
        for key, reg_name in tou_capacity_registers:
            if key in tou_config:
                await register_number_entity(
                    tou_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression("esphome::deye_inverter::MIN_TIME_POINT_CAPACITY"),
                    cg.RawExpression("esphome::deye_inverter::MAX_TIME_POINT_CAPACITY"),
                    cg.RawExpression(
                        "esphome::deye_inverter::STEP_TIME_POINT_CAPACITY"
                    ),
                    cg.RawExpression(
                        "esphome::deye_inverter::SCALE_TIME_POINT_CAPACITY"
                    ),
                    device_obj,
                )

    # Settings System Numbers (NEW - registers 60-97)
    if CONF_SETTINGS_SYSTEM_NUMBERS in config:
        system_config = config[CONF_SETTINGS_SYSTEM_NUMBERS]

        system_registers = [
            (
                CONF_SYS_SELF_CHECK_TIME,
                "REG_SELF_CHECK_TIME",
                "MIN_SYS_SELF_CHECK_TIME",
                "MAX_SYS_SELF_CHECK_TIME",
                "STEP_SYS_SELF_CHECK_TIME",
                "SCALE_SYS_SELF_CHECK_TIME",
            ),
            (
                CONF_SYS_INSULATION_RESISTANCE,
                "REG_INSULATION_RESISTANCE_LIMIT",
                "MIN_SYS_INSULATION_RESISTANCE",
                "MAX_SYS_INSULATION_RESISTANCE",
                "STEP_SYS_INSULATION_RESISTANCE",
                "SCALE_SYS_INSULATION_RESISTANCE",
            ),
        ]
        for (
            key,
            reg_name,
            min_name,
            max_name,
            step_name,
            scale_name,
        ) in system_registers:
            if key in system_config:
                await register_number_entity(
                    system_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )

    # Settings Grid Protection (NEW - registers 185-200)
    if CONF_SETTINGS_GRID_PROTECTION in config:
        gp_config = config[CONF_SETTINGS_GRID_PROTECTION]

        gp_registers = [
            (
                CONF_GP_OVER_VOLTAGE_PROTECTION,
                "REG_GRID_OVERVOLTAGE_PROTECTION",
                "MIN_GP_OVER_VOLTAGE_PROTECTION",
                "MAX_GP_OVER_VOLTAGE_PROTECTION",
                "STEP_GP_OVER_VOLTAGE_PROTECTION",
                "SCALE_GP_OVER_VOLTAGE_PROTECTION",
            ),
            (
                CONF_GP_UNDER_VOLTAGE_PROTECTION,
                "REG_GRID_UNDERVOLTAGE_PROTECTION",
                "MIN_GP_UNDER_VOLTAGE_PROTECTION",
                "MAX_GP_UNDER_VOLTAGE_PROTECTION",
                "STEP_GP_UNDER_VOLTAGE_PROTECTION",
                "SCALE_GP_UNDER_VOLTAGE_PROTECTION",
            ),
            (
                CONF_GP_OVER_FREQUENCY_PROTECTION,
                "REG_GRID_OVERFREQ_PROTECTION",
                "MIN_GP_OVER_FREQUENCY_PROTECTION",
                "MAX_GP_OVER_FREQUENCY_PROTECTION",
                "STEP_GP_OVER_FREQUENCY_PROTECTION",
                "SCALE_GP_OVER_FREQUENCY_PROTECTION",
            ),
            (
                CONF_GP_UNDER_FREQUENCY_PROTECTION,
                "REG_GRID_UNDERFREQ_PROTECTION",
                "MIN_GP_UNDER_FREQUENCY_PROTECTION",
                "MAX_GP_UNDER_FREQUENCY_PROTECTION",
                "STEP_GP_UNDER_FREQUENCY_PROTECTION",
                "SCALE_GP_UNDER_FREQUENCY_PROTECTION",
            ),
            (
                CONF_GP_VOLTAGE_RECONNECT,
                "REG_GEN_CONNECT_TO_GRID_INPUT",
                "MIN_GP_VOLTAGE_RECONNECT",
                "MAX_GP_VOLTAGE_RECONNECT",
                "STEP_GP_VOLTAGE_RECONNECT",
                "SCALE_GP_VOLTAGE_RECONNECT",
            ),
            (
                CONF_GP_FREQUENCY_RECONNECT,
                "REG_GEN_PEAK_SHAVING_POWER",
                "MIN_GP_FREQUENCY_RECONNECT",
                "MAX_GP_FREQUENCY_RECONNECT",
                "STEP_GP_FREQUENCY_RECONNECT",
                "SCALE_GP_FREQUENCY_RECONNECT",
            ),
            (
                CONF_GP_RECONNECT_TIME,
                "REG_GRID_PEAK_SHAVING_POWER",
                "MIN_GP_RECONNECT_TIME",
                "MAX_GP_RECONNECT_TIME",
                "STEP_GP_RECONNECT_TIME",
                "SCALE_GP_RECONNECT_TIME",
            ),
            (
                CONF_GP_RAMP_RATE,
                "REG_SMART_LOAD_OPEN_DELAY",
                "MIN_GP_RAMP_RATE",
                "MAX_GP_RAMP_RATE",
                "STEP_GP_RAMP_RATE",
                "SCALE_GP_RAMP_RATE",
            ),
            (
                CONF_GP_STARTUP_TIME,
                "REG_OUTPUT_PF_SETTING",
                "MIN_GP_STARTUP_TIME",
                "MAX_GP_STARTUP_TIME",
                "STEP_GP_STARTUP_TIME",
                "SCALE_GP_STARTUP_TIME",
            ),
        ]
        for key, reg_name, min_name, max_name, step_name, scale_name in gp_registers:
            if key in gp_config:
                await register_number_entity(
                    gp_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )

    # Settings California (NEW - registers 340-499)
    if CONF_SETTINGS_CALIFORNIA in config:
        ca_config = config[CONF_SETTINGS_CALIFORNIA]

        # Voltage Points (addresses 341-346)
        ca_voltage_registers = [
            (CONF_CA_VOLTAGE_POINT_1, "REG_RESERVED_341"),
            (CONF_CA_VOLTAGE_POINT_2, "REG_RESERVED_342"),
            (CONF_CA_VOLTAGE_POINT_3, "REG_RESERVED_343"),
            (CONF_CA_VOLTAGE_POINT_4, "REG_GRID_MONITORING_METHOD"),
            (CONF_CA_VOLTAGE_POINT_5, "REG_RESERVED_345"),
            (CONF_CA_VOLTAGE_POINT_6, "REG_RESERVED_346"),
        ]
        for key, reg_name in ca_voltage_registers:
            if key in ca_config:
                await register_number_entity(
                    ca_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression("esphome::deye_inverter::MIN_CA_VOLTAGE_POINT"),
                    cg.RawExpression("esphome::deye_inverter::MAX_CA_VOLTAGE_POINT"),
                    cg.RawExpression("esphome::deye_inverter::STEP_CA_VOLTAGE_POINT"),
                    cg.RawExpression("esphome::deye_inverter::SCALE_CA_VOLTAGE_POINT"),
                    device_obj,
                )

        # Power Points (addresses 347-352)
        ca_power_registers = [
            (CONF_CA_POWER_POINT_1, "REG_EXTERNAL_CT_RATIO"),
            (CONF_CA_POWER_POINT_2, "REG_METER_CT_RATIO"),
            (CONF_CA_POWER_POINT_3, "REG_RESERVED_349"),
            (CONF_CA_POWER_POINT_4, "REG_CHARGE_RAMP_CONTROL_1"),
            (CONF_CA_POWER_POINT_5, "REG_CHARGE_RAMP_CONTROL_2"),
            (CONF_CA_POWER_POINT_6, "REG_RESERVED_352"),
        ]
        for key, reg_name in ca_power_registers:
            if key in ca_config:
                await register_number_entity(
                    ca_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression("esphome::deye_inverter::MIN_CA_POWER_POINT"),
                    cg.RawExpression("esphome::deye_inverter::MAX_CA_POWER_POINT"),
                    cg.RawExpression("esphome::deye_inverter::STEP_CA_POWER_POINT"),
                    cg.RawExpression("esphome::deye_inverter::SCALE_CA_POWER_POINT"),
                    device_obj,
                )

        # Additional California settings
        ca_additional_registers = [
            (
                CONF_CA_RAMP_RATE,
                "REG_RESERVED_353",
                "MIN_CA_RAMP_RATE",
                "MAX_CA_RAMP_RATE",
                "STEP_CA_RAMP_RATE",
                "SCALE_CA_RAMP_RATE",
            ),
            (
                CONF_CA_RECONNECT_TIME,
                "REG_RESERVED_354",
                "MIN_CA_RECONNECT_TIME",
                "MAX_CA_RECONNECT_TIME",
                "STEP_CA_RECONNECT_TIME",
                "SCALE_CA_RECONNECT_TIME",
            ),
        ]
        for (
            key,
            reg_name,
            min_name,
            max_name,
            step_name,
            scale_name,
        ) in ca_additional_registers:
            if key in ca_config:
                await register_number_entity(
                    ca_config,
                    key,
                    var,
                    cg.RawExpression(f"esphome::deye_inverter::{reg_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{min_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{max_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{step_name}"),
                    cg.RawExpression(f"esphome::deye_inverter::{scale_name}"),
                    device_obj,
                )
