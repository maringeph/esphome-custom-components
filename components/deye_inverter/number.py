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
                108,
                0,
                185,
                0.1,
                10.0,
                device_obj,
            )

        # Max Discharge Current (Register 109, 0-185A, step 0.1, scale 10)
        if CONF_MAX_DISCHARGE_CURRENT in battery_config:
            await register_number_entity(
                battery_config,
                CONF_MAX_DISCHARGE_CURRENT,
                var,
                109,
                0,
                185,
                0.1,
                10.0,
                device_obj,
            )

    # Settings Battery Voltage
    if CONF_SETTINGS_BATTERY_VOLTAGE in config:
        voltage_config = config[CONF_SETTINGS_BATTERY_VOLTAGE]

        for key, address in [
            (CONF_EQUALIZATION_VOLTAGE, 99),
            (CONF_ABSORPTION_VOLTAGE, 100),
            (CONF_FLOAT_VOLTAGE, 101),
            (CONF_EMPTY_VOLTAGE, 103),
            (CONF_SHUTDOWN_VOLTAGE, 118),
            (CONF_RESTART_VOLTAGE, 119),
            (CONF_LOW_VOLTAGE_WARNING, 120),
        ]:
            if key in voltage_config:
                await register_number_entity(
                    voltage_config,
                    key,
                    var,
                    address,
                    38.0,
                    61.0,
                    0.01,
                    100.0,
                    device_obj,
                )

    # Settings Battery SOC
    if CONF_SETTINGS_BATTERY_SOC in config:
        soc_config = config[CONF_SETTINGS_BATTERY_SOC]

        for key, address in [
            (CONF_SHUTDOWN_SOC, 115),
            (CONF_RESTART_SOC, 116),
            (CONF_LOW_SOC_WARNING, 117),
        ]:
            if key in soc_config:
                await register_number_entity(
                    soc_config,
                    key,
                    var,
                    address,
                    0,
                    100,
                    1,
                    1.0,
                    device_obj,
                )

    # Settings Battery Additional
    if CONF_SETTINGS_BATTERY_ADDITIONAL in config:
        additional_config = config[CONF_SETTINGS_BATTERY_ADDITIONAL]

        for key, address, min_val, max_val, step in [
            (CONF_BATTERY_CAPACITY_AH, 102, 0, 2000, 1),
            (CONF_EQUALIZATION_DAY_CYCLE, 105, 0, 90, 1),
            (CONF_EQUALIZATION_TIME, 106, 0, 20, 0.5),
            (CONF_TEMPCO, 107, 0, 50, 1),
            (CONF_BATTERY_WAKE_UP, 112, 0, 1, 1),
            (CONF_BATTERY_RESISTANCE, 113, 0, 6000, 1),
            (CONF_BATTERY_CHARGING_EFFICIENCY, 114, 0, 100, 0.1),
        ]:
            if key in additional_config:
                scale = 1.0 if step == 1 else (10.0 if step == 0.1 else 100.0)
                await register_number_entity(
                    additional_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    scale,
                    device_obj,
                )

    # Settings Generator
    if CONF_SETTINGS_GENERATOR in config:
        gen_config = config[CONF_SETTINGS_GENERATOR]

        for key, address, min_val, max_val, step in [
            (CONF_GEN_MAX_RUN_TIME, 121, 0, 120, 0.1),
            (CONF_GEN_COOLDOWN_TIME, 122, 0, 60, 1),
            (CONF_GEN_MIN_POWER, 123, 0, 6500, 1),
            (CONF_GEN_START_VOLTAGE, 124, 38.0, 61.0, 0.01),
            (CONF_GEN_START_SOC, 125, 0, 100, 1),
            (CONF_GEN_CHARGING_CURRENT, 126, 0, 185, 1),
            (CONF_GEN_ENABLE, 127, 0, 1, 1),
        ]:
            if key in gen_config:
                scale = 1.0 if step == 1 else (10.0 if step == 0.1 else 100.0)
                await register_number_entity(
                    gen_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    scale,
                    device_obj,
                )

    # Settings Generator 2
    if CONF_SETTINGS_GENERATOR_2 in config:
        gen2_config = config[CONF_SETTINGS_GENERATOR_2]

        for key, address, min_val, max_val, step in [
            (CONF_GEN_MAX_TIME, 223, 0, 24, 0.1),
            (CONF_GEN_COOLDOWN, 224, 0, 24, 0.1),
            (CONF_GEN_START_VOLTAGE_225, 225, 38.0, 63.0, 0.01),
            (CONF_GEN_START_SOC_226, 226, 0, 100, 1),
            (CONF_GEN_CHARGE_CURRENT_227, 227, 0, 185, 1),
        ]:
            if key in gen2_config:
                scale = 1.0 if step == 1 else (10.0 if step == 0.1 else 100.0)
                await register_number_entity(
                    gen2_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    scale,
                    device_obj,
                )

    # Settings Smart Load
    if CONF_SETTINGS_SMART_LOAD in config:
        smart_load_config = config[CONF_SETTINGS_SMART_LOAD]

        for key, address in [
            (CONF_SMART_LOAD_OFF_VOLTAGE, 134),
            (CONF_SMART_LOAD_ON_VOLTAGE, 136),
        ]:
            if key in smart_load_config:
                await register_number_entity(
                    smart_load_config,
                    key,
                    var,
                    address,
                    38.0,
                    61.0,
                    0.01,
                    100.0,
                    device_obj,
                )

        for key, address in [
            (CONF_SMART_LOAD_OFF_SOC, 135),
            (CONF_SMART_LOAD_ON_SOC, 137),
        ]:
            if key in smart_load_config:
                await register_number_entity(
                    smart_load_config,
                    key,
                    var,
                    address,
                    0,
                    100,
                    1,
                    1.0,
                    device_obj,
                )

    # Settings Grid Charge
    if CONF_SETTINGS_GRID_CHARGE in config:
        grid_charge_config = config[CONF_SETTINGS_GRID_CHARGE]

        for key, address, min_val, max_val, step in [
            (CONF_MAXIMUM_BATTERY_GRID_CHARGE_CURRENT, 128, 0, 185, 1),
            (CONF_GRID_CHARGE_START_VOLTAGE, 228, 38.0, 63.0, 0.01),
            (CONF_GRID_CHARGE_START_SOC, 229, 0, 100, 1),
            (CONF_GRID_CHARGE_CURRENT, 230, 0, 185, 1),
        ]:
            if key in grid_charge_config:
                scale = 100.0 if step == 0.01 else 1.0
                await register_number_entity(
                    grid_charge_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    scale,
                    device_obj,
                )

    # Settings Grid Numbers (distributed from settings_special)
    if CONF_SETTINGS_GRID in config:
        grid_numbers_config = config[CONF_SETTINGS_GRID]

        for key, address, min_val, max_val, step in [
            (CONF_ZERO_EXPORT_POWER, 104, 0, 90, 1),
            (CONF_MAX_SOLAR_SELL_POWER, 340, 0, 6500, 1),
            (CONF_GRID_MAX_POWER, 143, 0, 6500, 1),
            (CONF_RESTORE_CONNECTION_TIME, 180, 0, 300, 1),
        ]:
            if key in grid_numbers_config:
                scale = 1.0 if step == 1 else (100.0 if step == 0.01 else 10.0)
                await register_number_entity(
                    grid_numbers_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    scale,
                    device_obj,
                )

    # Settings Generator Numbers (distributed from settings_special)
    if CONF_SETTINGS_GENERATOR in config:
        gen_numbers_config = config[CONF_SETTINGS_GENERATOR]

        for key, address, min_val, max_val, step in [
            (CONF_GEN_PORT_COUPLE_FREQ_LIMIT, 131, 0, 100, 0.01),
            (CONF_GENERATOR_REQUIRED_POWER_START, 139, 0, 6500, 1),
        ]:
            if key in gen_numbers_config:
                scale = 1.0 if step == 1 else (100.0 if step == 0.01 else 10.0)
                await register_number_entity(
                    gen_numbers_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    scale,
                    device_obj,
                )

    # Settings Time of Use (start times moved to datetime.py)
    if CONF_SETTINGS_TIME_OF_USE_NUMBERS in config:
        tou_config = config[CONF_SETTINGS_TIME_OF_USE_NUMBERS]

        # Time Point Power values (addresses 154-159)
        for key, address in [
            (CONF_TIME_POINT_1_POWER, 154),
            (CONF_TIME_POINT_2_POWER, 155),
            (CONF_TIME_POINT_3_POWER, 156),
            (CONF_TIME_POINT_4_POWER, 157),
            (CONF_TIME_POINT_5_POWER, 158),
            (CONF_TIME_POINT_6_POWER, 159),
        ]:
            if key in tou_config:
                await register_number_entity(
                    tou_config,
                    key,
                    var,
                    address,
                    -6500,
                    6500,
                    1,
                    1.0,
                    device_obj,
                )

        # Time Point Min Battery Voltage (addresses 160-165)
        for key, address in [
            (CONF_TIME_POINT_1_MIN_BATTERY_VOLTAGE, 160),
            (CONF_TIME_POINT_2_MIN_BATTERY_VOLTAGE, 161),
            (CONF_TIME_POINT_3_MIN_BATTERY_VOLTAGE, 162),
            (CONF_TIME_POINT_4_MIN_BATTERY_VOLTAGE, 163),
            (CONF_TIME_POINT_5_MIN_BATTERY_VOLTAGE, 164),
            (CONF_TIME_POINT_6_MIN_BATTERY_VOLTAGE, 165),
        ]:
            if key in tou_config:
                await register_number_entity(
                    tou_config,
                    key,
                    var,
                    address,
                    41.0,
                    63.0,
                    0.01,
                    100.0,
                    device_obj,
                )

        # Time Point Capacity (addresses 166-171)
        for key, address in [
            (CONF_TIME_POINT_1_CAPACITY, 166),
            (CONF_TIME_POINT_2_CAPACITY, 167),
            (CONF_TIME_POINT_3_CAPACITY, 168),
            (CONF_TIME_POINT_4_CAPACITY, 169),
            (CONF_TIME_POINT_5_CAPACITY, 170),
            (CONF_TIME_POINT_6_CAPACITY, 171),
        ]:
            if key in tou_config:
                await register_number_entity(
                    tou_config,
                    key,
                    var,
                    address,
                    0,
                    100,
                    5,
                    1.0,
                    device_obj,
                )

    # Settings System Numbers (NEW - registers 60-97)
    if CONF_SETTINGS_SYSTEM_NUMBERS in config:
        system_config = config[CONF_SETTINGS_SYSTEM_NUMBERS]

        for key, address, min_val, max_val, step in [
            # Register 60 is Remote Lock (Switch), not a Number
            (
                CONF_SYS_SELF_CHECK_TIME,
                61,
                0,
                1000,
                1,
            ),  # Self-check time [0,1000] seconds
            # Register 62-64 is System Time (handled by Time entity)
            (
                CONF_SYS_INSULATION_RESISTANCE,
                65,
                100,
                20000,
                1,
            ),  # Insulation resistance [100,20000] (0.1KΩ)
            # TODO: Register 62 (Data Log Interval) needs correct register address
        ]:
            if key in system_config:
                scale = 10.0 if step == 0.5 else 1.0
                await register_number_entity(
                    system_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    scale,
                    device_obj,
                )

    # Settings Grid Protection (NEW - registers 185-200)
    if CONF_SETTINGS_GRID_PROTECTION in config:
        gp_config = config[CONF_SETTINGS_GRID_PROTECTION]

        for key, address, min_val, max_val, step in [
            (CONF_GP_OVER_VOLTAGE_PROTECTION, 185, 200, 300, 0.1),
            (CONF_GP_UNDER_VOLTAGE_PROTECTION, 186, 100, 200, 0.1),
            (CONF_GP_OVER_FREQUENCY_PROTECTION, 187, 50, 65, 0.01),
            (CONF_GP_UNDER_FREQUENCY_PROTECTION, 188, 45, 55, 0.01),
            (CONF_GP_VOLTAGE_RECONNECT, 189, 180, 260, 0.1),
            (CONF_GP_FREQUENCY_RECONNECT, 190, 47, 53, 0.01),
            (CONF_GP_RECONNECT_TIME, 191, 0, 300, 1),
            (CONF_GP_RAMP_RATE, 192, 1, 100, 1),
            (CONF_GP_STARTUP_TIME, 193, 0, 600, 1),
        ]:
            if key in gp_config:
                scale = 100.0 if step == 0.01 else (10.0 if step == 0.1 else 1.0)
                await register_number_entity(
                    gp_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    scale,
                    device_obj,
                )

    # Settings California (NEW - registers 340-499)
    if CONF_SETTINGS_CALIFORNIA in config:
        ca_config = config[CONF_SETTINGS_CALIFORNIA]

        # Voltage Points (addresses 341-346)
        for key, address in [
            (CONF_CA_VOLTAGE_POINT_1, 341),
            (CONF_CA_VOLTAGE_POINT_2, 342),
            (CONF_CA_VOLTAGE_POINT_3, 343),
            (CONF_CA_VOLTAGE_POINT_4, 344),
            (CONF_CA_VOLTAGE_POINT_5, 345),
            (CONF_CA_VOLTAGE_POINT_6, 346),
        ]:
            if key in ca_config:
                await register_number_entity(
                    ca_config,
                    key,
                    var,
                    address,
                    0,
                    300,
                    0.1,
                    10.0,
                    device_obj,
                )

        # Power Points (addresses 347-352)
        for key, address in [
            (CONF_CA_POWER_POINT_1, 347),
            (CONF_CA_POWER_POINT_2, 348),
            (CONF_CA_POWER_POINT_3, 349),
            (CONF_CA_POWER_POINT_4, 350),
            (CONF_CA_POWER_POINT_5, 351),
            (CONF_CA_POWER_POINT_6, 352),
        ]:
            if key in ca_config:
                await register_number_entity(
                    ca_config,
                    key,
                    var,
                    address,
                    0,
                    100,
                    1,
                    1.0,
                    device_obj,
                )

        # Additional California settings
        for key, address, min_val, max_val, step in [
            (CONF_CA_RAMP_RATE, 353, 1, 100, 1),
            (CONF_CA_RECONNECT_TIME, 354, 0, 300, 1),
        ]:
            if key in ca_config:
                await register_number_entity(
                    ca_config,
                    key,
                    var,
                    address,
                    min_val,
                    max_val,
                    step,
                    1.0,
                    device_obj,
                )
