import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ID,
    CONF_VOLTAGE,
    CONF_CURRENT,
    CONF_POWER,
    CONF_FREQUENCY,
    UNIT_VOLT,
    UNIT_AMPERE,
    UNIT_WATT,
    UNIT_HERTZ,
    UNIT_CELSIUS,
    UNIT_PERCENT,
    UNIT_KILOWATT_HOURS,
    UNIT_HOUR,
    UNIT_MINUTE,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_ENERGY,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

from . import (
    CONF_DEYE_INVERTER_ID,
    DeyeInverter,
    CONF_BATTERY,
    CONF_PV1,
    CONF_PV2,
    CONF_PV3,
    CONF_PV4,
    CONF_GRID,
    CONF_LOAD_GRID,
    CONF_LOAD_UPS,
    CONF_GENERATOR,
    CONF_TEMPERATURES,
    CONF_STATISTICS,
    CONF_DAILY,
    CONF_TOTAL,
    CONF_PRODUCTION,
    CONF_BATTERY_CHARGE,
    CONF_BATTERY_DISCHARGE,
    CONF_GRID_IMPORT,
    CONF_GRID_EXPORT,
    CONF_CONSUMPTION,
    CONF_PV_PRODUCTION,
    CONF_LOAD_GRID_PORT,
    CONF_GENERATOR_PORT,
    CONF_INVERTER,
    CONF_DC,
    CONF_BATTERY_MODULE_1,
    CONF_BATTERY_MODULE_2,
    CONF_BATTERY_MODULE_3,
    CONF_BATTERY_MODULE_4,
    CONF_BATTERY_MODULE_5,
    CONF_BATTERY_MODULE_6,
    CONF_BATTERY_MODULE_7,
    CONF_BATTERY_MODULE_8,
    CONF_BATTERY_MODULE_9,
    # NEW 32-bit combined sensors
    CONF_TOTAL_ACTIVE_POWER_GENERATION,
    CONF_TOTAL_REACTIVE_POWER_GENERATION,
    CONF_TOTAL_BATTERY_CHARGE_32,
    CONF_TOTAL_BATTERY_DISCHARGE_32,
    CONF_TOTAL_GRID_IMPORT_32,
    CONF_TOTAL_GRID_EXPORT_32,
    CONF_TOTAL_CONSUMPTION_32,
)

AUTO_LOAD = ["modbus_controller"]

# Namespace für DeyeSensor
DeyeSensor = cg.esphome_ns.namespace("deye_inverter").class_(
    "DeyeSensor", sensor.Sensor, cg.Component
)

CODEOWNERS = ["@maringeph"]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def sensor_schema_with_address(
    address, scale=1.0, offset=0.0, signed=False, value_type="U_WORD", **kwargs
):
    """Create a sensor schema with register address configuration."""
    return sensor.sensor_schema(DeyeSensor, **kwargs).extend(
        {
            cv.Optional("address", default=address): cv.positive_int,
            cv.Optional("scale", default=scale): cv.float_,
            cv.Optional("offset", default=offset): cv.float_,
            cv.Optional("signed", default=signed): cv.boolean,
            cv.Optional("value_type", default=value_type): cv.one_of(
                "U_WORD",
                "S_WORD",
                "U_DWORD",
                "U_DWORD_R",
                "S_DWORD",
                "S_DWORD_R",
                "BITMASK",
            ),
        }
    )


# =============================================================================
# KONFIGURATIONSSCHEMA
# =============================================================================

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(cg.EntityBase),
        cv.GenerateID(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        # Battery Sensors
        cv.Optional(CONF_BATTERY): cv.Schema(
            {
                cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_POWER): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("soc"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_PERCENT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_BATTERY,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("temperature"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_CELSIUS,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_TEMPERATURE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("capacity"): sensor.sensor_schema(
                    unit_of_measurement="Ah",
                    accuracy_decimals=0,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # PV String Sensors
        cv.Optional(CONF_PV1): cv.Schema(
            {
                cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_POWER): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        cv.Optional(CONF_PV2): cv.Schema(
            {
                cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_POWER): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        cv.Optional(CONF_PV3): cv.Schema(
            {
                cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_POWER): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        cv.Optional(CONF_PV4): cv.Schema(
            {
                cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_POWER): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Grid Sensors
        cv.Optional(CONF_GRID): cv.Schema(
            {
                cv.Optional("voltage_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_total"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_FREQUENCY): sensor.sensor_schema(
                    unit_of_measurement=UNIT_HERTZ,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_FREQUENCY,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("grid_side_a_phase_power"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("grid_side_b_phase_power"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("grid_side_c_phase_power"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("grid_side_total_power"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("total_grid_power"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Load Grid Sensors
        cv.Optional(CONF_LOAD_GRID): cv.Schema(
            {
                cv.Optional("voltage_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_total"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Load Grid Port Sensors (NEW)
        cv.Optional(CONF_LOAD_GRID_PORT): cv.Schema(
            {
                cv.Optional("voltage_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("load_real_power"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("load_apparent_power"): sensor.sensor_schema(
                    unit_of_measurement="VA",
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("load_frequency"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_HERTZ,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_FREQUENCY,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Load UPS Sensors
        cv.Optional(CONF_LOAD_UPS): cv.Schema(
            {
                cv.Optional("voltage_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_total"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional(CONF_FREQUENCY): sensor.sensor_schema(
                    unit_of_measurement=UNIT_HERTZ,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_FREQUENCY,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Generator Sensors
        cv.Optional(CONF_GENERATOR): cv.Schema(
            {
                cv.Optional("voltage_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_total"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Generator Port Sensors (NEW)
        cv.Optional(CONF_GENERATOR_PORT): cv.Schema(
            {
                cv.Optional("voltage_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("power_total"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("current_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("gen_port_frequency"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_HERTZ,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_FREQUENCY,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Inverter Sensors (NEW)
        cv.Optional(CONF_INVERTER): cv.Schema(
            {
                cv.Optional("voltage_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("voltage_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("real_power_l1"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("real_power_l2"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("real_power_l3"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("real_power"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_WATT,
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("apparent_power"): sensor.sensor_schema(
                    unit_of_measurement="VA",
                    accuracy_decimals=0,
                    device_class=DEVICE_CLASS_POWER,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("frequency"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_HERTZ,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_FREQUENCY,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # DC Sensors (NEW - additional PV channels)
        cv.Optional(CONF_DC): cv.Schema(
            {
                cv.Optional("dc5_current"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("dc6_voltage"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("dc6_current"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("dc7_voltage"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("dc7_current"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("dc8_voltage"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_VOLT,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_VOLTAGE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("dc8_current"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_AMPERE,
                    accuracy_decimals=2,
                    device_class=DEVICE_CLASS_CURRENT,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Temperature Sensors
        cv.Optional(CONF_TEMPERATURES): cv.Schema(
            {
                cv.Optional("heatsink"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_CELSIUS,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_TEMPERATURE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
                cv.Optional("dc_transformer"): sensor.sensor_schema(
                    unit_of_measurement=UNIT_CELSIUS,
                    accuracy_decimals=1,
                    device_class=DEVICE_CLASS_TEMPERATURE,
                    state_class=STATE_CLASS_MEASUREMENT,
                ),
            }
        ),
        # Battery Module Sensors (NEW - 9 modules)
        **{
            cv.Optional(module_name): cv.Schema(
                {
                    cv.Optional("voltage"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_VOLT,
                        accuracy_decimals=2,
                        device_class=DEVICE_CLASS_VOLTAGE,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("current"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_AMPERE,
                        accuracy_decimals=2,
                        device_class=DEVICE_CLASS_CURRENT,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("soc"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_PERCENT,
                        accuracy_decimals=0,
                        device_class=DEVICE_CLASS_BATTERY,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("temperature"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_CELSIUS,
                        accuracy_decimals=1,
                        device_class=DEVICE_CLASS_TEMPERATURE,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("status"): sensor.sensor_schema(
                        unit_of_measurement="",
                        accuracy_decimals=0,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("fault_code"): sensor.sensor_schema(
                        unit_of_measurement="",
                        accuracy_decimals=0,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("cycle_count"): sensor.sensor_schema(
                        unit_of_measurement="",
                        accuracy_decimals=0,
                        state_class=STATE_CLASS_TOTAL_INCREASING,
                    ),
                    cv.Optional("capacity_remaining"): sensor.sensor_schema(
                        unit_of_measurement="Ah",
                        accuracy_decimals=1,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("capacity_total"): sensor.sensor_schema(
                        unit_of_measurement="Ah",
                        accuracy_decimals=1,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("power"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_WATT,
                        accuracy_decimals=0,
                        device_class=DEVICE_CLASS_POWER,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("cell_max_voltage"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_VOLT,
                        accuracy_decimals=3,
                        device_class=DEVICE_CLASS_VOLTAGE,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("cell_min_voltage"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_VOLT,
                        accuracy_decimals=3,
                        device_class=DEVICE_CLASS_VOLTAGE,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("cell_max_temp"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_CELSIUS,
                        accuracy_decimals=1,
                        device_class=DEVICE_CLASS_TEMPERATURE,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                    cv.Optional("cell_min_temp"): sensor.sensor_schema(
                        unit_of_measurement=UNIT_CELSIUS,
                        accuracy_decimals=1,
                        device_class=DEVICE_CLASS_TEMPERATURE,
                        state_class=STATE_CLASS_MEASUREMENT,
                    ),
                }
            )
            for module_name in [
                CONF_BATTERY_MODULE_1,
                CONF_BATTERY_MODULE_2,
                CONF_BATTERY_MODULE_3,
                CONF_BATTERY_MODULE_4,
                CONF_BATTERY_MODULE_5,
                CONF_BATTERY_MODULE_6,
                CONF_BATTERY_MODULE_7,
                CONF_BATTERY_MODULE_8,
                CONF_BATTERY_MODULE_9,
            ]
        },
        # Statistics Sensors
        cv.Optional(CONF_STATISTICS): cv.Schema(
            {
                cv.Optional(CONF_DAILY): cv.Schema(
                    {
                        cv.Optional(CONF_PRODUCTION): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_BATTERY_CHARGE): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_BATTERY_DISCHARGE): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_GRID_IMPORT): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_GRID_EXPORT): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_CONSUMPTION): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_PV_PRODUCTION): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("pv1_production"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("pv2_production"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("pv3_production"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("pv4_production"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("generator_on_time"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_HOUR,
                            accuracy_decimals=1,
                            state_class=STATE_CLASS_MEASUREMENT,
                        ),
                        # NEW daily statistics
                        cv.Optional(
                            "daily_active_power_generation"
                        ): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(
                            "active_power_generation_today"
                        ): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("daily_grid_connection_time"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_MINUTE,
                            accuracy_decimals=0,
                            state_class=STATE_CLASS_MEASUREMENT,
                        ),
                    }
                ),
                cv.Optional(CONF_TOTAL): cv.Schema(
                    {
                        cv.Optional(CONF_PRODUCTION): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_BATTERY_CHARGE): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_BATTERY_DISCHARGE): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_GRID_IMPORT): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_GRID_EXPORT): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_CONSUMPTION): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(CONF_PV_PRODUCTION): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        # NEW 32-bit combined sensors (replaces separate low/high pairs)
                        cv.Optional(
                            "total_active_power_generation"
                        ): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(
                            "total_reactive_power_generation"
                        ): sensor.sensor_schema(
                            unit_of_measurement="kVARh",
                            accuracy_decimals=1,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_battery_charge"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_battery_discharge"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_grid_import"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_grid_export"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_consumption"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        # Legacy separate low/high sensors (deprecated, kept for backward compatibility)
                        cv.Optional("active_power_gen_total_low"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(
                            "active_power_gen_total_high"
                        ): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(
                            "reactive_power_gen_total_low"
                        ): sensor.sensor_schema(
                            unit_of_measurement="kVARh",
                            accuracy_decimals=1,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(
                            "reactive_power_gen_total_high"
                        ): sensor.sensor_schema(
                            unit_of_measurement="kVARh",
                            accuracy_decimals=1,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_pv_production"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("battery_charge_total_high"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(
                            "battery_discharge_total_high"
                        ): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_grid_buy_high"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_grid_sell_high"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional("total_load_high"): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        # Additional 32-bit combined sensors with descriptive names
                        cv.Optional(
                            "total_active_power_generation"
                        ): sensor.sensor_schema(
                            unit_of_measurement=UNIT_KILOWATT_HOURS,
                            accuracy_decimals=1,
                            device_class=DEVICE_CLASS_ENERGY,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                        cv.Optional(
                            "total_reactive_power_generation"
                        ): sensor.sensor_schema(
                            unit_of_measurement="kVARh",
                            accuracy_decimals=1,
                            state_class=STATE_CLASS_TOTAL_INCREASING,
                        ),
                    }
                ),
            }
        ),
    }
)


# =============================================================================
# HELPER FUNCTIONS FOR to_code
# =============================================================================


async def register_sensor(
    config,
    key,
    parent,
    address,
    scale=1.0,
    offset=0.0,
    signed=False,
    value_type="U_WORD",
):
    """Register a single sensor with the parent component."""
    if key not in config:
        return

    conf = config[key]
    sens = await sensor.new_sensor(conf)
    cg.add(sens.set_parent(parent))
    cg.add(sens.set_address(address))
    cg.add(sens.set_scale(scale))
    cg.add(sens.set_offset(offset))

    # Set bytes based on value type
    if value_type in ["U_DWORD", "U_DWORD_R", "S_DWORD", "S_DWORD_R"]:
        cg.add(sens.set_bytes(4))
        cg.add(
            sens.set_data_type(
                getattr(cg.esphome_ns.namespace("deye_inverter").DataType, value_type)
            )
        )
    else:
        cg.add(sens.set_bytes(2))
        if signed:
            cg.add(
                sens.set_data_type(
                    cg.esphome_ns.namespace("deye_inverter").DataType.S_WORD
                )
            )
        else:
            cg.add(
                sens.set_data_type(
                    cg.esphome_ns.namespace("deye_inverter").DataType.U_WORD
                )
            )

    # Register with parent's sensor list
    cg.add(parent.register_sensor(sens))


# =============================================================================
# CODE GENERATION
# =============================================================================


async def to_code(config):
    parent = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Register Battery Sensors (Register 586-592)
    if CONF_BATTERY in config:
        battery_conf = config[CONF_BATTERY]
        await register_sensor(battery_conf, CONF_VOLTAGE, parent, 587, scale=0.1)
        await register_sensor(
            battery_conf, CONF_CURRENT, parent, 591, scale=0.01, signed=True
        )
        await register_sensor(
            battery_conf, CONF_POWER, parent, 590, scale=1.0, signed=True
        )
        await register_sensor(battery_conf, "soc", parent, 588, scale=1.0)
        await register_sensor(
            battery_conf, "temperature", parent, 586, scale=0.1, offset=-100.0
        )
        await register_sensor(battery_conf, "capacity", parent, 592, scale=1.0)

    # Register PV1 Sensors (Register 672, 676-677)
    if CONF_PV1 in config:
        pv1_conf = config[CONF_PV1]
        await register_sensor(pv1_conf, CONF_VOLTAGE, parent, 676, scale=0.1)
        await register_sensor(pv1_conf, CONF_CURRENT, parent, 677, scale=0.1)
        await register_sensor(pv1_conf, CONF_POWER, parent, 672, scale=1.0)

    # Register PV2 Sensors (Register 673, 678-679)
    if CONF_PV2 in config:
        pv2_conf = config[CONF_PV2]
        await register_sensor(pv2_conf, CONF_VOLTAGE, parent, 678, scale=0.1)
        await register_sensor(pv2_conf, CONF_CURRENT, parent, 679, scale=0.1)
        await register_sensor(pv2_conf, CONF_POWER, parent, 673, scale=1.0)

    # Register PV3 Sensors (Register 674, 680-681)
    if CONF_PV3 in config:
        pv3_conf = config[CONF_PV3]
        await register_sensor(pv3_conf, CONF_VOLTAGE, parent, 680, scale=0.1)
        await register_sensor(pv3_conf, CONF_CURRENT, parent, 681, scale=0.1)
        await register_sensor(pv3_conf, CONF_POWER, parent, 674, scale=1.0)

    # Register PV4 Sensors (Register 675, 682-683)
    if CONF_PV4 in config:
        pv4_conf = config[CONF_PV4]
        await register_sensor(pv4_conf, CONF_VOLTAGE, parent, 682, scale=0.1)
        await register_sensor(pv4_conf, CONF_CURRENT, parent, 683, scale=0.1)
        await register_sensor(pv4_conf, CONF_POWER, parent, 675, scale=1.0)

    # Register Grid Sensors (Register 598-612)
    if CONF_GRID in config:
        grid_conf = config[CONF_GRID]
        await register_sensor(grid_conf, "voltage_l1", parent, 598, scale=0.1)
        await register_sensor(grid_conf, "voltage_l2", parent, 599, scale=0.1)
        await register_sensor(grid_conf, "voltage_l3", parent, 600, scale=0.1)
        await register_sensor(grid_conf, "current_l1", parent, 610, scale=0.01)
        await register_sensor(grid_conf, "current_l2", parent, 611, scale=0.01)
        await register_sensor(grid_conf, "current_l3", parent, 612, scale=0.01)
        await register_sensor(
            grid_conf, "power_l1", parent, 604, scale=1.0, signed=True
        )
        await register_sensor(
            grid_conf, "power_l2", parent, 605, scale=1.0, signed=True
        )
        await register_sensor(
            grid_conf, "power_l3", parent, 606, scale=1.0, signed=True
        )
        await register_sensor(
            grid_conf, "power_total", parent, 607, scale=1.0, signed=True
        )
        await register_sensor(grid_conf, CONF_FREQUENCY, parent, 609, scale=0.01)
        # NEW Grid Side sensors (addresses 622-626)
        await register_sensor(
            grid_conf, "grid_side_a_phase_power", parent, 622, scale=1.0
        )
        await register_sensor(
            grid_conf, "grid_side_b_phase_power", parent, 623, scale=1.0
        )
        await register_sensor(
            grid_conf, "grid_side_c_phase_power", parent, 624, scale=1.0
        )
        await register_sensor(
            grid_conf, "total_grid_power", parent, 625, scale=1.0, signed=True
        )
        await register_sensor(
            grid_conf, "grid_side_total_power", parent, 626, scale=1.0
        )

    # Register Load Grid Sensors (Register 644-653)
    if CONF_LOAD_GRID in config:
        load_grid_conf = config[CONF_LOAD_GRID]
        await register_sensor(load_grid_conf, "voltage_l1", parent, 644, scale=0.1)
        await register_sensor(load_grid_conf, "voltage_l2", parent, 645, scale=0.1)
        await register_sensor(load_grid_conf, "voltage_l3", parent, 646, scale=0.1)
        await register_sensor(load_grid_conf, "power_l1", parent, 650, scale=1.0)
        await register_sensor(load_grid_conf, "power_l2", parent, 651, scale=1.0)
        await register_sensor(load_grid_conf, "power_l3", parent, 652, scale=1.0)
        await register_sensor(load_grid_conf, "power_total", parent, 653, scale=1.0)

    # Register Load Grid Port Sensors (NEW - addresses 644-655)
    if CONF_LOAD_GRID_PORT in config:
        load_port_conf = config[CONF_LOAD_GRID_PORT]
        await register_sensor(load_port_conf, "voltage_l1", parent, 644, scale=0.1)
        await register_sensor(load_port_conf, "voltage_l2", parent, 645, scale=0.1)
        await register_sensor(load_port_conf, "voltage_l3", parent, 646, scale=0.1)
        await register_sensor(
            load_port_conf, "current_l1", parent, 647, scale=0.01, signed=True
        )
        await register_sensor(
            load_port_conf, "current_l2", parent, 648, scale=0.01, signed=True
        )
        await register_sensor(
            load_port_conf, "current_l3", parent, 649, scale=0.01, signed=True
        )
        await register_sensor(
            load_port_conf, "power_l1", parent, 650, scale=1.0, signed=True
        )
        await register_sensor(
            load_port_conf, "power_l2", parent, 651, scale=1.0, signed=True
        )
        await register_sensor(
            load_port_conf, "power_l3", parent, 652, scale=1.0, signed=True
        )
        await register_sensor(
            load_port_conf, "load_real_power", parent, 653, scale=1.0, signed=True
        )
        await register_sensor(
            load_port_conf, "load_apparent_power", parent, 654, scale=1.0, signed=True
        )
        await register_sensor(load_port_conf, "load_frequency", parent, 655, scale=0.01)

    # Register Load UPS Sensors (Register 627-643)
    if CONF_LOAD_UPS in config:
        load_ups_conf = config[CONF_LOAD_UPS]
        await register_sensor(load_ups_conf, "voltage_l1", parent, 627, scale=0.1)
        await register_sensor(load_ups_conf, "voltage_l2", parent, 628, scale=0.1)
        await register_sensor(load_ups_conf, "voltage_l3", parent, 629, scale=0.1)
        await register_sensor(load_ups_conf, "power_l1", parent, 640, scale=1.0)
        await register_sensor(load_ups_conf, "power_l2", parent, 641, scale=1.0)
        await register_sensor(load_ups_conf, "power_l3", parent, 642, scale=1.0)
        await register_sensor(load_ups_conf, "power_total", parent, 643, scale=1.0)
        await register_sensor(load_ups_conf, CONF_FREQUENCY, parent, 638, scale=0.01)

    # Register Generator Sensors (Register 661-667)
    if CONF_GENERATOR in config:
        gen_conf = config[CONF_GENERATOR]
        await register_sensor(gen_conf, "voltage_l1", parent, 661, scale=0.1)
        await register_sensor(gen_conf, "voltage_l2", parent, 662, scale=0.1)
        await register_sensor(gen_conf, "voltage_l3", parent, 663, scale=0.1)
        await register_sensor(gen_conf, "power_l1", parent, 664, scale=1.0)
        await register_sensor(gen_conf, "power_l2", parent, 665, scale=1.0)
        await register_sensor(gen_conf, "power_l3", parent, 666, scale=1.0)
        await register_sensor(gen_conf, "power_total", parent, 667, scale=1.0)

    # Register Generator Port Sensors (NEW - addresses 661-671)
    if CONF_GENERATOR_PORT in config:
        gen_port_conf = config[CONF_GENERATOR_PORT]
        await register_sensor(gen_port_conf, "voltage_l1", parent, 661, scale=0.1)
        await register_sensor(gen_port_conf, "voltage_l2", parent, 662, scale=0.1)
        await register_sensor(gen_port_conf, "voltage_l3", parent, 663, scale=0.1)
        await register_sensor(
            gen_port_conf, "power_l1", parent, 664, scale=1.0, signed=True
        )
        await register_sensor(
            gen_port_conf, "power_l2", parent, 665, scale=1.0, signed=True
        )
        await register_sensor(
            gen_port_conf, "power_l3", parent, 666, scale=1.0, signed=True
        )
        await register_sensor(
            gen_port_conf, "power_total", parent, 667, scale=1.0, signed=True
        )
        await register_sensor(
            gen_port_conf, "current_l1", parent, 668, scale=0.01, signed=True
        )
        await register_sensor(
            gen_port_conf, "current_l2", parent, 669, scale=0.01, signed=True
        )
        await register_sensor(
            gen_port_conf, "current_l3", parent, 670, scale=0.01, signed=True
        )
        await register_sensor(
            gen_port_conf, "gen_port_frequency", parent, 671, scale=0.01
        )

    # Register Inverter Sensors (NEW - addresses 627-638)
    if CONF_INVERTER in config:
        inverter_conf = config[CONF_INVERTER]
        await register_sensor(inverter_conf, "voltage_l1", parent, 627, scale=0.1)
        await register_sensor(inverter_conf, "voltage_l2", parent, 628, scale=0.1)
        await register_sensor(inverter_conf, "voltage_l3", parent, 629, scale=0.1)
        await register_sensor(
            inverter_conf, "real_power_l1", parent, 633, scale=1.0, signed=True
        )
        await register_sensor(
            inverter_conf, "real_power_l2", parent, 634, scale=1.0, signed=True
        )
        await register_sensor(
            inverter_conf, "real_power_l3", parent, 635, scale=1.0, signed=True
        )
        await register_sensor(
            inverter_conf, "real_power", parent, 636, scale=1.0, signed=True
        )
        await register_sensor(
            inverter_conf, "apparent_power", parent, 637, scale=1.0, signed=True
        )
        await register_sensor(inverter_conf, "frequency", parent, 638, scale=0.01)

    # Register DC Sensors (NEW - addresses 212-218)
    if CONF_DC in config:
        dc_conf = config[CONF_DC]
        await register_sensor(dc_conf, "dc5_current", parent, 212, scale=0.1)
        await register_sensor(dc_conf, "dc6_voltage", parent, 213, scale=0.1)
        await register_sensor(dc_conf, "dc6_current", parent, 214, scale=0.1)
        await register_sensor(dc_conf, "dc7_voltage", parent, 215, scale=0.1)
        await register_sensor(dc_conf, "dc7_current", parent, 216, scale=0.1)
        await register_sensor(dc_conf, "dc8_voltage", parent, 217, scale=0.1)
        await register_sensor(dc_conf, "dc8_current", parent, 218, scale=0.1)

    # Register Temperature Sensors (Register 540-541)
    if CONF_TEMPERATURES in config:
        temp_conf = config[CONF_TEMPERATURES]
        await register_sensor(
            temp_conf, "dc_transformer", parent, 540, scale=0.1, offset=-100.0
        )
        await register_sensor(
            temp_conf, "heatsink", parent, 541, scale=0.1, offset=-100.0
        )

    # Register Battery Module Sensors (NEW - 9 modules, 14 registers each, starting at 350)
    battery_modules = [
        (CONF_BATTERY_MODULE_1, 350),
        (CONF_BATTERY_MODULE_2, 364),
        (CONF_BATTERY_MODULE_3, 378),
        (CONF_BATTERY_MODULE_4, 392),
        (CONF_BATTERY_MODULE_5, 406),
        (CONF_BATTERY_MODULE_6, 420),
        (CONF_BATTERY_MODULE_7, 434),
        (CONF_BATTERY_MODULE_8, 448),
        (CONF_BATTERY_MODULE_9, 462),
    ]

    for module_conf_name, base_address in battery_modules:
        if module_conf_name in config:
            bm_conf = config[module_conf_name]
            await register_sensor(bm_conf, "voltage", parent, base_address, scale=0.01)
            await register_sensor(
                bm_conf, "current", parent, base_address + 1, scale=0.01, signed=True
            )
            await register_sensor(bm_conf, "soc", parent, base_address + 2, scale=1.0)
            await register_sensor(
                bm_conf,
                "temperature",
                parent,
                base_address + 3,
                scale=0.1,
                offset=-100.0,
            )
            await register_sensor(
                bm_conf, "status", parent, base_address + 4, scale=1.0
            )
            await register_sensor(
                bm_conf, "fault_code", parent, base_address + 5, scale=1.0
            )
            await register_sensor(
                bm_conf, "cycle_count", parent, base_address + 6, scale=1.0
            )
            await register_sensor(
                bm_conf, "capacity_remaining", parent, base_address + 7, scale=0.1
            )
            await register_sensor(
                bm_conf, "capacity_total", parent, base_address + 8, scale=0.1
            )
            await register_sensor(
                bm_conf, "power", parent, base_address + 9, scale=1.0, signed=True
            )
            await register_sensor(
                bm_conf, "cell_max_voltage", parent, base_address + 10, scale=0.001
            )
            await register_sensor(
                bm_conf, "cell_min_voltage", parent, base_address + 11, scale=0.001
            )
            await register_sensor(
                bm_conf,
                "cell_max_temp",
                parent,
                base_address + 12,
                scale=0.1,
                offset=-100.0,
            )
            await register_sensor(
                bm_conf,
                "cell_min_temp",
                parent,
                base_address + 13,
                scale=0.1,
                offset=-100.0,
            )

    # Register Statistics Sensors
    if CONF_STATISTICS in config:
        stats_conf = config[CONF_STATISTICS]

        if CONF_DAILY in stats_conf:
            daily_conf = stats_conf[CONF_DAILY]
            await register_sensor(daily_conf, CONF_PRODUCTION, parent, 501, scale=0.1)
            await register_sensor(
                daily_conf, CONF_BATTERY_CHARGE, parent, 514, scale=0.1
            )
            await register_sensor(
                daily_conf, CONF_BATTERY_DISCHARGE, parent, 515, scale=0.1
            )
            await register_sensor(daily_conf, CONF_GRID_IMPORT, parent, 520, scale=0.1)
            await register_sensor(daily_conf, CONF_GRID_EXPORT, parent, 521, scale=0.1)
            await register_sensor(daily_conf, CONF_CONSUMPTION, parent, 526, scale=0.1)
            await register_sensor(
                daily_conf, CONF_PV_PRODUCTION, parent, 529, scale=0.1
            )
            await register_sensor(daily_conf, "pv1_production", parent, 530, scale=0.1)
            await register_sensor(daily_conf, "pv2_production", parent, 531, scale=0.1)
            await register_sensor(daily_conf, "pv3_production", parent, 532, scale=0.1)
            await register_sensor(daily_conf, "pv4_production", parent, 533, scale=0.1)
            await register_sensor(
                daily_conf, "generator_on_time", parent, 539, scale=0.1
            )
            # NEW daily statistics
            await register_sensor(
                daily_conf, "daily_active_power_generation", parent, 501, scale=0.1
            )
            await register_sensor(
                daily_conf, "active_power_generation_today", parent, 502, scale=0.1
            )
            await register_sensor(
                daily_conf, "daily_grid_connection_time", parent, 503, scale=1.0
            )

        if CONF_TOTAL in stats_conf:
            total_conf = stats_conf[CONF_TOTAL]
            # Total values are 32-bit (2 registers each) - using U_DWORD_R for reversed byte order
            await register_sensor(
                total_conf,
                CONF_PRODUCTION,
                parent,
                504,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_BATTERY_CHARGE,
                parent,
                516,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_BATTERY_DISCHARGE,
                parent,
                518,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_GRID_IMPORT,
                parent,
                522,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_GRID_EXPORT,
                parent,
                524,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_CONSUMPTION,
                parent,
                527,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_PV_PRODUCTION,
                parent,
                534,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            # NEW 32-bit combined sensors (replaces separate low/high sensors)
            await register_sensor(
                total_conf,
                "total_active_power_generation",
                parent,
                504,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                "total_reactive_power_generation",
                parent,
                506,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                "total_battery_charge",
                parent,
                516,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                "total_battery_discharge",
                parent,
                518,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                "total_grid_import",
                parent,
                522,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                "total_grid_export",
                parent,
                524,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                "total_consumption",
                parent,
                527,
                scale=0.1,
                value_type="U_DWORD_R",
            )
