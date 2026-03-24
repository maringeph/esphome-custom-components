"""Deye Inverter Sensor Platform.

This module provides the main sensor configuration schema and code generation
for the Deye Inverter component. Based on ds100_meter architecture.
"""

import esphome.codegen as cg
from esphome.components import modbus, sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_DISABLED_BY_DEFAULT,
    CONF_NAME,
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
from esphome.components import text_sensor

AUTO_LOAD = ["modbus", "modbus_controller"]
CODEOWNERS = ["@maringeph"]

# =============================================================================
# IMPORT ALL CONF CONSTANTS FROM __init__.py
# =============================================================================
from . import (
    # Namespace
    deye_inverter_ns,
    DeyeInverter,
    CONF_DEVICE_ID,
    # Main Component
    CONF_MODBUS_ID,
    CONF_ADDRESS,
    CONF_UPDATE_INTERVAL_LIVE,
    CONF_UPDATE_INTERVAL_STATISTICS,
    CONF_UPDATE_INTERVAL_DEVICE_INFO,
    # Device Info
    CONF_DEVICE_INFO,
    CONF_DEVICE_TYPE,
    CONF_MODBUS_ADDRESS,
    CONF_DEVICE_INFO_EXTENDED,
    CONF_SERIAL_NUMBER,
    CONF_FIRMWARE_VERSION,
    CONF_HARDWARE_VERSION,
    CONF_DEVICE_TYPE_CODE,
    CONF_INVERTER_MODEL,
    CONF_INVERTER_POWER_RATING,
    CONF_INVERTER_VOLTAGE_RATING,
    CONF_INVERTER_CURRENT_RATING,
    CONF_GRID_FREQUENCY_RATING,
    # Battery
    CONF_BATTERY,
    CONF_BATTERY_VOLTAGE,
    CONF_BATTERY_CURRENT,
    CONF_BATTERY_POWER,
    CONF_BATTERY_SOC,
    CONF_BATTERY_TEMPERATURE,
    CONF_BATTERY_CAPACITY,
    # PV
    CONF_PV1,
    CONF_PV2,
    CONF_PV3,
    CONF_PV4,
    CONF_PV_VOLTAGE,
    CONF_PV_CURRENT,
    CONF_PV_POWER,
    # Grid
    CONF_GRID,
    CONF_GRID_VOLTAGE_L1,
    CONF_GRID_VOLTAGE_L2,
    CONF_GRID_VOLTAGE_L3,
    CONF_GRID_VOLTAGE_L1_L2,
    CONF_GRID_VOLTAGE_L2_L3,
    CONF_GRID_VOLTAGE_L3_L1,
    CONF_GRID_CURRENT_L1,
    CONF_GRID_CURRENT_L2,
    CONF_GRID_CURRENT_L3,
    CONF_GRID_POWER_L1,
    CONF_GRID_POWER_L2,
    CONF_GRID_POWER_L3,
    CONF_GRID_POWER_TOTAL,
    CONF_GRID_FREQUENCY,
    CONF_GRID_SIDE_A_PHASE_POWER,
    CONF_GRID_SIDE_B_PHASE_POWER,
    CONF_GRID_SIDE_C_PHASE_POWER,
    CONF_GRID_SIDE_TOTAL_POWER,
    CONF_TOTAL_GRID_POWER,
    # Grid CT Sensors
    CONF_INTERNAL_CT_L1_POWER,
    CONF_INTERNAL_CT_L2_POWER,
    CONF_INTERNAL_CT_L3_POWER,
    CONF_INTERNAL_TOTAL_POWER,
    CONF_EXTERNAL_CT_L1_POWER,
    CONF_EXTERNAL_CT_L2_POWER,
    CONF_EXTERNAL_CT_L3_POWER,
    CONF_OUT_OF_GRID_TOTAL_POWER,
    CONF_GRID_METER_APPARENT_POWER,
    CONF_GRID_METER_POWER_FACTOR,
    CONF_GRID_METER_CURRENT_L1,
    CONF_GRID_METER_CURRENT_L2,
    CONF_GRID_METER_CURRENT_L3,
    # Load Grid
    CONF_LOAD_GRID,
    CONF_LOAD_GRID_VOLTAGE_L1,
    CONF_LOAD_GRID_VOLTAGE_L2,
    CONF_LOAD_GRID_VOLTAGE_L3,
    CONF_LOAD_GRID_POWER_L1,
    CONF_LOAD_GRID_POWER_L2,
    CONF_LOAD_GRID_POWER_L3,
    CONF_LOAD_GRID_POWER_TOTAL,
    # Load Grid Port
    CONF_LOAD_GRID_PORT,
    CONF_LOAD_PORT_VOLTAGE_L1,
    CONF_LOAD_PORT_VOLTAGE_L2,
    CONF_LOAD_PORT_VOLTAGE_L3,
    CONF_LOAD_PORT_CURRENT_L1,
    CONF_LOAD_PORT_CURRENT_L2,
    CONF_LOAD_PORT_CURRENT_L3,
    CONF_LOAD_PORT_POWER_L1,
    CONF_LOAD_PORT_POWER_L2,
    CONF_LOAD_PORT_POWER_L3,
    CONF_LOAD_REAL_POWER,
    CONF_LOAD_APPARENT_POWER,
    CONF_LOAD_FREQUENCY,
    # Load UPS
    CONF_LOAD_UPS,
    CONF_LOAD_UPS_VOLTAGE_L1,
    CONF_LOAD_UPS_VOLTAGE_L2,
    CONF_LOAD_UPS_VOLTAGE_L3,
    CONF_LOAD_UPS_POWER_L1,
    CONF_LOAD_UPS_POWER_L2,
    CONF_LOAD_UPS_POWER_L3,
    CONF_LOAD_UPS_POWER_TOTAL,
    CONF_LOAD_UPS_FREQUENCY,
    # Generator
    CONF_GENERATOR,
    CONF_GENERATOR_VOLTAGE_L1,
    CONF_GENERATOR_VOLTAGE_L2,
    CONF_GENERATOR_VOLTAGE_L3,
    CONF_GENERATOR_CURRENT_L1,
    CONF_GENERATOR_CURRENT_L2,
    CONF_GENERATOR_CURRENT_L3,
    CONF_GENERATOR_POWER_L1,
    CONF_GENERATOR_POWER_L2,
    CONF_GENERATOR_POWER_L3,
    CONF_GENERATOR_POWER_TOTAL,
    CONF_GENERATOR_FREQUENCY,
    # Generator Port
    CONF_GENERATOR_PORT,
    CONF_GEN_PORT_VOLTAGE_L1,
    CONF_GEN_PORT_VOLTAGE_L2,
    CONF_GEN_PORT_VOLTAGE_L3,
    CONF_GEN_PORT_CURRENT_L1,
    CONF_GEN_PORT_CURRENT_L2,
    CONF_GEN_PORT_CURRENT_L3,
    CONF_GEN_PORT_POWER_L1,
    CONF_GEN_PORT_POWER_L2,
    CONF_GEN_PORT_POWER_L3,
    CONF_GEN_PORT_POWER_TOTAL,
    CONF_GEN_PORT_FREQUENCY,
    # Temperatures
    CONF_TEMPERATURES,
    CONF_TEMP_HEATSINK,
    CONF_TEMP_DC_TRANSFORMER,
    # Inverter
    CONF_INVERTER,
    CONF_INVERTER_VOLTAGE_L1,
    CONF_INVERTER_VOLTAGE_L2,
    CONF_INVERTER_VOLTAGE_L3,
    CONF_INVERTER_REAL_POWER_L1,
    CONF_INVERTER_REAL_POWER_L2,
    CONF_INVERTER_REAL_POWER_L3,
    CONF_INVERTER_REAL_POWER,
    CONF_INVERTER_APPARENT_POWER,
    CONF_INVERTER_FREQUENCY,
    # DC
    CONF_DC,
    CONF_DC5_CURRENT,
    CONF_DC6_VOLTAGE,
    CONF_DC6_CURRENT,
    CONF_DC7_VOLTAGE,
    CONF_DC7_CURRENT,
    CONF_DC8_VOLTAGE,
    CONF_DC8_CURRENT,
    # Battery Modules
    CONF_BATTERY_MODULE_1,
    CONF_BATTERY_MODULE_2,
    CONF_BATTERY_MODULE_3,
    CONF_BATTERY_MODULE_4,
    CONF_BATTERY_MODULE_5,
    CONF_BATTERY_MODULE_6,
    CONF_BATTERY_MODULE_7,
    CONF_BATTERY_MODULE_8,
    CONF_BATTERY_MODULE_9,
    CONF_BM_VOLTAGE,
    CONF_BM_CURRENT,
    CONF_BM_SOC,
    CONF_BM_TEMPERATURE,
    CONF_BM_STATUS,
    CONF_BM_FAULT_CODE,
    CONF_BM_CYCLE_COUNT,
    CONF_BM_CAPACITY_REMAINING,
    CONF_BM_CAPACITY_TOTAL,
    CONF_BM_POWER,
    CONF_BM_CELL_MAX_VOLTAGE,
    CONF_BM_CELL_MIN_VOLTAGE,
    CONF_BM_CELL_MAX_TEMP,
    CONF_BM_CELL_MIN_TEMP,
    # Statistics
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
    CONF_DAILY_PV1_PRODUCTION,
    CONF_DAILY_PV2_PRODUCTION,
    CONF_DAILY_PV3_PRODUCTION,
    CONF_DAILY_PV4_PRODUCTION,
    CONF_DAILY_GENERATOR_ON_TIME,
    CONF_DAILY_ACTIVE_POWER_GENERATION,
    CONF_ACTIVE_POWER_GENERATION_TODAY,
    CONF_DAILY_GRID_CONNECTION_TIME,
    CONF_TOTAL_ACTIVE_POWER_GENERATION,
    CONF_TOTAL_REACTIVE_POWER_GENERATION,
    CONF_TOTAL_BATTERY_CHARGE_32,
    CONF_TOTAL_BATTERY_DISCHARGE_32,
    CONF_TOTAL_GRID_IMPORT_32,
    CONF_TOTAL_GRID_EXPORT_32,
    CONF_TOTAL_CONSUMPTION_32,
    CONF_ACTIVE_POWER_GEN_TOTAL_LOW,
    CONF_ACTIVE_POWER_GEN_TOTAL_HIGH,
    CONF_REACTIVE_POWER_GEN_TOTAL_LOW,
    CONF_REACTIVE_POWER_GEN_TOTAL_HIGH,
    CONF_TOTAL_PV_PRODUCTION,
    CONF_BATTERY_CHARGE_TOTAL_HIGH,
    CONF_BATTERY_DISCHARGE_TOTAL_HIGH,
    CONF_TOTAL_GRID_BUY_HIGH,
    CONF_TOTAL_GRID_SELL_HIGH,
    CONF_TOTAL_LOAD_HIGH,
    # Status
    CONF_STATUS,
    CONF_WARNING_1_RAW,
    CONF_WARNING_2_RAW,
    CONF_ERROR_1_RAW,
    CONF_ERROR_2_RAW,
    CONF_ERROR_3_RAW,
    CONF_ERROR_4_RAW,
    CONF_COMMUNICATION_BOARD_FAILURE,
    # Status Raw Sensors
    CONF_RUNNING_STATUS,
    CONF_TURN_OFF_ON_STATUS,
    CONF_AC_INV_RELAY,
)

# =============================================================================
# DECLARE DEYE SENSOR CLASS
# =============================================================================

DeyeSensor = deye_inverter_ns.class_("DeyeSensor", sensor.Sensor, cg.Component)

# =============================================================================
# SENSOR SCHEMAS
# =============================================================================

# Entity base schema
ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(DeyeSensor),
    }
)


def deye_sensor_schema(
    unit_of_measurement=None,
    accuracy_decimals=None,
    device_class=None,
    state_class=None,
    icon=None,
):
    """Create a sensor schema that uses DeyeSensor class.

    Only passes non-None values to sensor.sensor_schema() to avoid
    ESPHome validation errors with NoneType.
    """
    kwargs = {}
    if unit_of_measurement is not None:
        kwargs["unit_of_measurement"] = unit_of_measurement
    if accuracy_decimals is not None:
        kwargs["accuracy_decimals"] = accuracy_decimals
    if device_class is not None:
        kwargs["device_class"] = device_class
    if state_class is not None:
        kwargs["state_class"] = state_class
    if icon is not None:
        kwargs["icon"] = icon

    return sensor.sensor_schema(DeyeSensor, **kwargs)


# Device Info Schemas
DEVICE_INFO_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_DEVICE_TYPE): cv.Schema(
            {
                cv.Required(CONF_ID): cv.declare_id(text_sensor.TextSensor),
                cv.Optional(CONF_NAME): cv.string,
                cv.Optional(CONF_DISABLED_BY_DEFAULT, default=True): cv.boolean,
            }
        ),
        cv.Optional(CONF_MODBUS_ADDRESS): cv.Schema(
            {
                cv.Required(CONF_ID): cv.declare_id(DeyeSensor),
                cv.Optional(CONF_NAME): cv.string,
                cv.Optional(CONF_DISABLED_BY_DEFAULT, default=True): cv.boolean,
            }
        ),
    }
)

DEVICE_INFO_EXTENDED_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SERIAL_NUMBER): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_FIRMWARE_VERSION): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_HARDWARE_VERSION): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DEVICE_TYPE_CODE): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_MODEL): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_POWER_RATING): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_VOLTAGE_RATING): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_CURRENT_RATING): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_FREQUENCY_RATING): deye_sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# PV String Schema
PV_STRING_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_PV_VOLTAGE): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_PV_CURRENT): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_PV_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Battery Schema
BATTERY_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_VOLTAGE): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_CURRENT): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_SOC): deye_sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_BATTERY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_TEMPERATURE): deye_sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_CAPACITY): deye_sensor_schema(
            unit_of_measurement="Ah",
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Battery Module Schema
BATTERY_MODULE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BM_VOLTAGE): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CURRENT): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_SOC): deye_sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_BATTERY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_TEMPERATURE): deye_sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_STATUS): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:information",
        ),
        cv.Optional(CONF_BM_FAULT_CODE): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
            icon="mdi:alert",
        ),
        cv.Optional(CONF_BM_CYCLE_COUNT): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
            icon="mdi:battery-sync",
        ),
        cv.Optional(CONF_BM_CAPACITY_REMAINING): deye_sensor_schema(
            unit_of_measurement="Ah",
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CAPACITY_TOTAL): deye_sensor_schema(
            unit_of_measurement="Ah",
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CELL_MAX_VOLTAGE): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CELL_MIN_VOLTAGE): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CELL_MAX_TEMP): deye_sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CELL_MIN_TEMP): deye_sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Grid Schema
GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GRID_VOLTAGE_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L1_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L2_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L3_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_CURRENT_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_CURRENT_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_CURRENT_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_POWER_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_POWER_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_POWER_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_POWER_TOTAL): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_FREQUENCY): deye_sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_SIDE_A_PHASE_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_SIDE_B_PHASE_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_SIDE_C_PHASE_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_SIDE_TOTAL_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_TOTAL_GRID_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INTERNAL_CT_L1_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INTERNAL_CT_L2_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INTERNAL_CT_L3_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INTERNAL_TOTAL_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_EXTERNAL_CT_L1_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_EXTERNAL_CT_L2_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_EXTERNAL_CT_L3_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_OUT_OF_GRID_TOTAL_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_METER_APPARENT_POWER): deye_sensor_schema(
            unit_of_measurement="VA",
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_METER_POWER_FACTOR): deye_sensor_schema(
            accuracy_decimals=2,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_METER_CURRENT_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_METER_CURRENT_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_METER_CURRENT_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Load Grid Schema
LOAD_GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_POWER_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_POWER_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_POWER_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_POWER_TOTAL): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Load Grid Port Schema
LOAD_GRID_PORT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_CURRENT_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_CURRENT_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_CURRENT_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_POWER_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_POWER_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_POWER_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_REAL_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_APPARENT_POWER): deye_sensor_schema(
            unit_of_measurement="VA",
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_FREQUENCY): deye_sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Load UPS Schema
LOAD_UPS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_POWER_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_POWER_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_POWER_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_POWER_TOTAL): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_FREQUENCY): deye_sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Generator Schema
GENERATOR_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GENERATOR_VOLTAGE_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_VOLTAGE_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_VOLTAGE_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_CURRENT_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_CURRENT_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_CURRENT_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_POWER_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_POWER_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_POWER_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_POWER_TOTAL): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_FREQUENCY): deye_sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Generator Port Schema
GENERATOR_PORT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_CURRENT_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_CURRENT_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_CURRENT_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_POWER_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_POWER_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_POWER_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_POWER_TOTAL): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_FREQUENCY): deye_sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Temperatures Schema
TEMPERATURES_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_TEMP_HEATSINK): deye_sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_TEMP_DC_TRANSFORMER): deye_sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Inverter Schema
INVERTER_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_INVERTER_VOLTAGE_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_VOLTAGE_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_VOLTAGE_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_REAL_POWER_L1): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_REAL_POWER_L2): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_REAL_POWER_L3): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_REAL_POWER): deye_sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_APPARENT_POWER): deye_sensor_schema(
            unit_of_measurement="VA",
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_FREQUENCY): deye_sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# DC Schema
DC_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_DC5_CURRENT): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC6_VOLTAGE): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC6_CURRENT): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC7_VOLTAGE): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC7_CURRENT): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC8_VOLTAGE): deye_sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC8_CURRENT): deye_sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# Statistics Schemas
DAILY_STATISTICS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_CHARGE): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_DISCHARGE): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_GRID_IMPORT): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_GRID_EXPORT): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_CONSUMPTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_PV_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_PV1_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_PV2_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_PV3_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_PV4_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_GENERATOR_ON_TIME): deye_sensor_schema(
            unit_of_measurement=UNIT_HOUR,
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DAILY_ACTIVE_POWER_GENERATION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_ACTIVE_POWER_GENERATION_TODAY): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_GRID_CONNECTION_TIME): deye_sensor_schema(
            unit_of_measurement=UNIT_MINUTE,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

TOTAL_STATISTICS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_CHARGE): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_DISCHARGE): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_GRID_IMPORT): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_GRID_EXPORT): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_CONSUMPTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_PV_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_ACTIVE_POWER_GENERATION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_REACTIVE_POWER_GENERATION): deye_sensor_schema(
            unit_of_measurement="kVARh",
            accuracy_decimals=1,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_BATTERY_CHARGE_32): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_BATTERY_DISCHARGE_32): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_GRID_IMPORT_32): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_GRID_EXPORT_32): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_CONSUMPTION_32): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_ACTIVE_POWER_GEN_TOTAL_LOW): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_ACTIVE_POWER_GEN_TOTAL_HIGH): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_REACTIVE_POWER_GEN_TOTAL_LOW): deye_sensor_schema(
            unit_of_measurement="kVARh",
            accuracy_decimals=1,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_REACTIVE_POWER_GEN_TOTAL_HIGH): deye_sensor_schema(
            unit_of_measurement="kVARh",
            accuracy_decimals=1,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_PV_PRODUCTION): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_CHARGE_TOTAL_HIGH): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_DISCHARGE_TOTAL_HIGH): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_GRID_BUY_HIGH): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_GRID_SELL_HIGH): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_LOAD_HIGH): deye_sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
    }
)

STATISTICS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_DAILY): DAILY_STATISTICS_SCHEMA,
        cv.Optional(CONF_TOTAL): TOTAL_STATISTICS_SCHEMA,
    }
)

# Status Schema
STATUS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_WARNING_1_RAW): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_WARNING_2_RAW): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ERROR_1_RAW): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ERROR_2_RAW): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ERROR_3_RAW): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ERROR_4_RAW): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_COMMUNICATION_BOARD_FAILURE): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_RUNNING_STATUS): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_TURN_OFF_ON_STATUS): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_AC_INV_RELAY): deye_sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# =============================================================================
# MAIN COMPONENT CONFIG SCHEMA
# =============================================================================
CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(DeyeInverter),
            cv.Optional(CONF_DEVICE_ID): cv.string,
            cv.Optional(
                CONF_UPDATE_INTERVAL_LIVE, default="1s"
            ): cv.positive_time_period_milliseconds,
            cv.Optional(
                CONF_UPDATE_INTERVAL_STATISTICS, default="5s"
            ): cv.positive_time_period_milliseconds,
            cv.Optional(
                CONF_UPDATE_INTERVAL_DEVICE_INFO, default="60s"
            ): cv.positive_time_period_milliseconds,
            # Device info
            cv.Optional(CONF_DEVICE_INFO): DEVICE_INFO_SCHEMA,
            cv.Optional(CONF_DEVICE_INFO_EXTENDED): DEVICE_INFO_EXTENDED_SCHEMA,
            # Sensor groups
            cv.Optional(CONF_BATTERY): BATTERY_SCHEMA,
            cv.Optional(CONF_PV1): PV_STRING_SCHEMA,
            cv.Optional(CONF_PV2): PV_STRING_SCHEMA,
            cv.Optional(CONF_PV3): PV_STRING_SCHEMA,
            cv.Optional(CONF_PV4): PV_STRING_SCHEMA,
            cv.Optional(CONF_GRID): GRID_SCHEMA,
            cv.Optional(CONF_LOAD_GRID): LOAD_GRID_SCHEMA,
            cv.Optional(CONF_LOAD_GRID_PORT): LOAD_GRID_PORT_SCHEMA,
            cv.Optional(CONF_LOAD_UPS): LOAD_UPS_SCHEMA,
            cv.Optional(CONF_GENERATOR): GENERATOR_SCHEMA,
            cv.Optional(CONF_GENERATOR_PORT): GENERATOR_PORT_SCHEMA,
            cv.Optional(CONF_TEMPERATURES): TEMPERATURES_SCHEMA,
            cv.Optional(CONF_INVERTER): INVERTER_SCHEMA,
            cv.Optional(CONF_DC): DC_SCHEMA,
            cv.Optional(CONF_STATISTICS): STATISTICS_SCHEMA,
            cv.Optional(CONF_STATUS): STATUS_SCHEMA,
            # Battery Modules
            cv.Optional(CONF_BATTERY_MODULE_1): BATTERY_MODULE_SCHEMA,
            cv.Optional(CONF_BATTERY_MODULE_2): BATTERY_MODULE_SCHEMA,
            cv.Optional(CONF_BATTERY_MODULE_3): BATTERY_MODULE_SCHEMA,
            cv.Optional(CONF_BATTERY_MODULE_4): BATTERY_MODULE_SCHEMA,
            cv.Optional(CONF_BATTERY_MODULE_5): BATTERY_MODULE_SCHEMA,
            cv.Optional(CONF_BATTERY_MODULE_6): BATTERY_MODULE_SCHEMA,
            cv.Optional(CONF_BATTERY_MODULE_7): BATTERY_MODULE_SCHEMA,
            cv.Optional(CONF_BATTERY_MODULE_8): BATTERY_MODULE_SCHEMA,
            cv.Optional(CONF_BATTERY_MODULE_9): BATTERY_MODULE_SCHEMA,
        }
    )
    .extend(cv.polling_component_schema("1s"))
    .extend(modbus.modbus_device_schema(0x01))
)


# =============================================================================
# TO CODE - Hauptkomponente erstellen
# =============================================================================
async def to_code(config):
    """Generate code for the Deye Inverter component."""
    # Create the component instance
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await modbus.register_modbus_device(var, config)

    # Handle device_id for Home Assistant grouping
    from . import get_or_create_device

    device_id = config.get(CONF_DEVICE_ID)
    device_obj = await get_or_create_device(device_id)

    # Set update intervals
    cg.add(var.set_update_interval_live(config[CONF_UPDATE_INTERVAL_LIVE]))
    cg.add(var.set_update_interval_statistics(config[CONF_UPDATE_INTERVAL_STATISTICS]))
    cg.add(
        var.set_update_interval_device_info(config[CONF_UPDATE_INTERVAL_DEVICE_INFO])
    )

    # Calculate base update interval for modbus_controller polling
    # Following ds100_meter pattern: GCD of all intervals divided by 5
    from math import gcd

    intervals = [
        config[CONF_UPDATE_INTERVAL_LIVE].total_milliseconds,
        config[CONF_UPDATE_INTERVAL_STATISTICS].total_milliseconds,
        config[CONF_UPDATE_INTERVAL_DEVICE_INFO].total_milliseconds,
    ]
    base_interval = intervals[0]
    for interval in intervals[1:]:
        base_interval = gcd(base_interval, interval)

    # Divide by 5 for smooth polling
    base_interval = max(base_interval // 5, 50)  # Minimum 50ms
    cg.add(var.set_update_interval(base_interval))

    # Register all sensors (pass device_obj for sensor grouping)
    await register_sensors(var, config, device_obj)


# =============================================================================
# SENSOR REGISTRATION FUNCTIONS (formerly in sensor_impl.py)
# =============================================================================


async def register_single_sensor(
    config,
    key,
    parent,
    address,
    scale=1.0,
    offset=0.0,
    signed=False,
    value_type="U_WORD",
    device_obj=None,
):
    """Register a single sensor with the parent component."""
    if key not in config:
        return

    conf = config[key]
    # Create DeyeSensor instead of base sensor
    sens = cg.new_Pvariable(conf[CONF_ID])
    await sensor.register_sensor(sens, conf)
    cg.add(sens.set_parent(parent))
    cg.add(sens.set_address(address))
    cg.add(sens.set_scale(scale))
    cg.add(sens.set_offset(offset))

    # Set bytes based on value type
    if value_type in ["U_DWORD", "U_DWORD_R", "S_DWORD", "S_DWORD_R"]:
        cg.add(sens.set_bytes(4))
        cg.add(
            sens.set_data_type(
                cg.RawExpression(f"deye_inverter::DataType::{value_type}")
            )
        )
    else:
        cg.add(sens.set_bytes(2))
        if signed:
            cg.add(
                sens.set_data_type(cg.RawExpression("deye_inverter::DataType::S_WORD"))
            )
        else:
            cg.add(
                sens.set_data_type(cg.RawExpression("deye_inverter::DataType::U_WORD"))
            )

    # Register with parent's sensor list
    cg.add(parent.register_sensor(sens))

    # Associate with device if provided
    if device_obj is not None:
        cg.add(sens.set_device(device_obj))


async def register_sensors(parent, config, device_obj=None):
    """Register all sensors with the parent component."""

    # =============================================================================
    # PROCESS BATTERY SENSORS
    # =============================================================================
    if CONF_BATTERY in config:
        battery_conf = config[CONF_BATTERY]
        await register_single_sensor(
            battery_conf,
            CONF_BATTERY_VOLTAGE,
            parent,
            587,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            battery_conf,
            CONF_BATTERY_CURRENT,
            parent,
            591,
            scale=0.01,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            battery_conf,
            CONF_BATTERY_POWER,
            parent,
            590,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            battery_conf,
            CONF_BATTERY_SOC,
            parent,
            588,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            battery_conf,
            CONF_BATTERY_TEMPERATURE,
            parent,
            586,
            scale=0.1,
            offset=-100.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            battery_conf,
            CONF_BATTERY_CAPACITY,
            parent,
            592,
            scale=1.0,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS PV STRING SENSORS
    # =============================================================================
    for pv_group, base_addr in [
        (CONF_PV1, 672),
        (CONF_PV2, 673),
        (CONF_PV3, 674),
        (CONF_PV4, 675),
    ]:
        if pv_group in config:
            pv_conf = config[pv_group]
            voltage_addr = 676 + (base_addr - 672) * 2
            current_addr = 677 + (base_addr - 672) * 2
            await register_single_sensor(
                pv_conf,
                CONF_PV_VOLTAGE,
                parent,
                voltage_addr,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                pv_conf,
                CONF_PV_CURRENT,
                parent,
                current_addr,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                pv_conf,
                CONF_PV_POWER,
                parent,
                base_addr,
                scale=1.0,
                device_obj=device_obj,
            )

    # =============================================================================
    # PROCESS GRID SENSORS
    # =============================================================================
    if CONF_GRID in config:
        grid_conf = config[CONF_GRID]
        await register_single_sensor(
            grid_conf,
            CONF_GRID_VOLTAGE_L1,
            parent,
            598,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_VOLTAGE_L2,
            parent,
            599,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_VOLTAGE_L3,
            parent,
            600,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_CURRENT_L1,
            parent,
            610,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_CURRENT_L2,
            parent,
            611,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_CURRENT_L3,
            parent,
            612,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_POWER_L1,
            parent,
            604,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_POWER_L2,
            parent,
            605,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_POWER_L3,
            parent,
            606,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_POWER_TOTAL,
            parent,
            607,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_FREQUENCY,
            parent,
            609,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_SIDE_A_PHASE_POWER,
            parent,
            622,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_SIDE_B_PHASE_POWER,
            parent,
            623,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_SIDE_C_PHASE_POWER,
            parent,
            624,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_TOTAL_GRID_POWER,
            parent,
            625,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_SIDE_TOTAL_POWER,
            parent,
            626,
            scale=1.0,
            device_obj=device_obj,
        )

        # Grid CT Sensors
        await register_single_sensor(
            grid_conf,
            CONF_INTERNAL_CT_L1_POWER,
            parent,
            607,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_INTERNAL_CT_L2_POWER,
            parent,
            608,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_INTERNAL_CT_L3_POWER,
            parent,
            609,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_INTERNAL_TOTAL_POWER,
            parent,
            610,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_EXTERNAL_CT_L1_POWER,
            parent,
            611,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_EXTERNAL_CT_L2_POWER,
            parent,
            612,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_EXTERNAL_CT_L3_POWER,
            parent,
            613,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_OUT_OF_GRID_TOTAL_POWER,
            parent,
            614,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_METER_APPARENT_POWER,
            parent,
            615,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_METER_POWER_FACTOR,
            parent,
            616,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_METER_CURRENT_L1,
            parent,
            617,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_METER_CURRENT_L2,
            parent,
            618,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            grid_conf,
            CONF_GRID_METER_CURRENT_L3,
            parent,
            619,
            scale=0.01,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS LOAD GRID SENSORS
    # =============================================================================
    if CONF_LOAD_GRID in config:
        load_grid_conf = config[CONF_LOAD_GRID]
        await register_single_sensor(
            load_grid_conf,
            CONF_LOAD_GRID_VOLTAGE_L1,
            parent,
            644,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_grid_conf,
            CONF_LOAD_GRID_VOLTAGE_L2,
            parent,
            645,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_grid_conf,
            CONF_LOAD_GRID_VOLTAGE_L3,
            parent,
            646,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_grid_conf,
            CONF_LOAD_GRID_POWER_L1,
            parent,
            650,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_grid_conf,
            CONF_LOAD_GRID_POWER_L2,
            parent,
            651,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_grid_conf,
            CONF_LOAD_GRID_POWER_L3,
            parent,
            652,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_grid_conf,
            CONF_LOAD_GRID_POWER_TOTAL,
            parent,
            653,
            scale=1.0,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS LOAD GRID PORT SENSORS
    # =============================================================================
    if CONF_LOAD_GRID_PORT in config:
        load_port_conf = config[CONF_LOAD_GRID_PORT]
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_VOLTAGE_L1,
            parent,
            644,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_VOLTAGE_L2,
            parent,
            645,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_VOLTAGE_L3,
            parent,
            646,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_CURRENT_L1,
            parent,
            647,
            scale=0.01,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_CURRENT_L2,
            parent,
            648,
            scale=0.01,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_CURRENT_L3,
            parent,
            649,
            scale=0.01,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_POWER_L1,
            parent,
            650,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_POWER_L2,
            parent,
            651,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_POWER_L3,
            parent,
            652,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_REAL_POWER,
            parent,
            653,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_APPARENT_POWER,
            parent,
            654,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_FREQUENCY,
            parent,
            655,
            scale=0.01,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS LOAD UPS SENSORS
    # =============================================================================
    if CONF_LOAD_UPS in config:
        load_ups_conf = config[CONF_LOAD_UPS]
        await register_single_sensor(
            load_ups_conf,
            CONF_LOAD_UPS_VOLTAGE_L1,
            parent,
            627,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_ups_conf,
            CONF_LOAD_UPS_VOLTAGE_L2,
            parent,
            628,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_ups_conf,
            CONF_LOAD_UPS_VOLTAGE_L3,
            parent,
            629,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_ups_conf,
            CONF_LOAD_UPS_POWER_L1,
            parent,
            640,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_ups_conf,
            CONF_LOAD_UPS_POWER_L2,
            parent,
            641,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_ups_conf,
            CONF_LOAD_UPS_POWER_L3,
            parent,
            642,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_ups_conf,
            CONF_LOAD_UPS_POWER_TOTAL,
            parent,
            643,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            load_ups_conf,
            CONF_LOAD_UPS_FREQUENCY,
            parent,
            638,
            scale=0.01,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS GENERATOR SENSORS
    # =============================================================================
    if CONF_GENERATOR in config:
        gen_conf = config[CONF_GENERATOR]
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_VOLTAGE_L1,
            parent,
            661,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_VOLTAGE_L2,
            parent,
            662,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_VOLTAGE_L3,
            parent,
            663,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_CURRENT_L1,
            parent,
            668,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_CURRENT_L2,
            parent,
            669,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_CURRENT_L3,
            parent,
            670,
            scale=0.01,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_POWER_L1,
            parent,
            664,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_POWER_L2,
            parent,
            665,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_POWER_L3,
            parent,
            666,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_POWER_TOTAL,
            parent,
            667,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_conf,
            CONF_GENERATOR_FREQUENCY,
            parent,
            671,
            scale=0.01,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS GENERATOR PORT SENSORS
    # =============================================================================
    if CONF_GENERATOR_PORT in config:
        gen_port_conf = config[CONF_GENERATOR_PORT]
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_VOLTAGE_L1,
            parent,
            661,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_VOLTAGE_L2,
            parent,
            662,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_VOLTAGE_L3,
            parent,
            663,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_CURRENT_L1,
            parent,
            668,
            scale=0.01,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_CURRENT_L2,
            parent,
            669,
            scale=0.01,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_CURRENT_L3,
            parent,
            670,
            scale=0.01,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_POWER_L1,
            parent,
            664,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_POWER_L2,
            parent,
            665,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_POWER_L3,
            parent,
            666,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_POWER_TOTAL,
            parent,
            667,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_FREQUENCY,
            parent,
            671,
            scale=0.01,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS INVERTER SENSORS
    # =============================================================================
    if CONF_INVERTER in config:
        inverter_conf = config[CONF_INVERTER]
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_VOLTAGE_L1,
            parent,
            627,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_VOLTAGE_L2,
            parent,
            628,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_VOLTAGE_L3,
            parent,
            629,
            scale=0.1,
            device_obj=device_obj,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_REAL_POWER_L1,
            parent,
            633,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_REAL_POWER_L2,
            parent,
            634,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_REAL_POWER_L3,
            parent,
            635,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_REAL_POWER,
            parent,
            636,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_APPARENT_POWER,
            parent,
            637,
            scale=1.0,
            signed=True,
            device_obj=device_obj,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_FREQUENCY,
            parent,
            638,
            scale=0.01,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS DC SENSORS
    # =============================================================================
    if CONF_DC in config:
        dc_conf = config[CONF_DC]
        await register_single_sensor(
            dc_conf, CONF_DC5_CURRENT, parent, 212, scale=0.1, device_obj=device_obj
        )
        await register_single_sensor(
            dc_conf, CONF_DC6_VOLTAGE, parent, 213, scale=0.1, device_obj=device_obj
        )
        await register_single_sensor(
            dc_conf, CONF_DC6_CURRENT, parent, 214, scale=0.1, device_obj=device_obj
        )
        await register_single_sensor(
            dc_conf, CONF_DC7_VOLTAGE, parent, 215, scale=0.1, device_obj=device_obj
        )
        await register_single_sensor(
            dc_conf, CONF_DC7_CURRENT, parent, 216, scale=0.1, device_obj=device_obj
        )
        await register_single_sensor(
            dc_conf, CONF_DC8_VOLTAGE, parent, 217, scale=0.1, device_obj=device_obj
        )
        await register_single_sensor(
            dc_conf, CONF_DC8_CURRENT, parent, 218, scale=0.1, device_obj=device_obj
        )

    # =============================================================================
    # PROCESS TEMPERATURE SENSORS
    # =============================================================================
    if CONF_TEMPERATURES in config:
        temp_conf = config[CONF_TEMPERATURES]
        await register_single_sensor(
            temp_conf,
            CONF_TEMP_DC_TRANSFORMER,
            parent,
            540,
            scale=0.1,
            offset=-100.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            temp_conf,
            CONF_TEMP_HEATSINK,
            parent,
            541,
            scale=0.1,
            offset=-100.0,
            device_obj=device_obj,
        )

    # =============================================================================
    # PROCESS BATTERY MODULE SENSORS
    # =============================================================================
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
            await register_single_sensor(
                bm_conf,
                CONF_BM_VOLTAGE,
                parent,
                base_address,
                scale=0.01,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CURRENT,
                parent,
                base_address + 1,
                scale=0.01,
                signed=True,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_SOC,
                parent,
                base_address + 2,
                scale=1.0,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_TEMPERATURE,
                parent,
                base_address + 3,
                scale=0.1,
                offset=-100.0,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_STATUS,
                parent,
                base_address + 4,
                scale=1.0,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_FAULT_CODE,
                parent,
                base_address + 5,
                scale=1.0,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CYCLE_COUNT,
                parent,
                base_address + 6,
                scale=1.0,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CAPACITY_REMAINING,
                parent,
                base_address + 7,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CAPACITY_TOTAL,
                parent,
                base_address + 8,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_POWER,
                parent,
                base_address + 9,
                scale=1.0,
                signed=True,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CELL_MAX_VOLTAGE,
                parent,
                base_address + 10,
                scale=0.001,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CELL_MIN_VOLTAGE,
                parent,
                base_address + 11,
                scale=0.001,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CELL_MAX_TEMP,
                parent,
                base_address + 12,
                scale=0.1,
                offset=-100.0,
                device_obj=device_obj,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CELL_MIN_TEMP,
                parent,
                base_address + 13,
                scale=0.1,
                offset=-100.0,
                device_obj=device_obj,
            )

    # =============================================================================
    # PROCESS STATISTICS SENSORS
    # =============================================================================
    if CONF_STATISTICS in config:
        stats_conf = config[CONF_STATISTICS]

        if CONF_DAILY in stats_conf:
            daily_conf = stats_conf[CONF_DAILY]
            await register_single_sensor(
                daily_conf,
                CONF_PRODUCTION,
                parent,
                501,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_BATTERY_CHARGE,
                parent,
                514,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_BATTERY_DISCHARGE,
                parent,
                515,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_GRID_IMPORT,
                parent,
                520,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_GRID_EXPORT,
                parent,
                521,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_CONSUMPTION,
                parent,
                526,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_PV_PRODUCTION,
                parent,
                529,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_DAILY_PV1_PRODUCTION,
                parent,
                530,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_DAILY_PV2_PRODUCTION,
                parent,
                531,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_DAILY_PV3_PRODUCTION,
                parent,
                532,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_DAILY_PV4_PRODUCTION,
                parent,
                533,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_DAILY_GENERATOR_ON_TIME,
                parent,
                539,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_DAILY_ACTIVE_POWER_GENERATION,
                parent,
                501,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_ACTIVE_POWER_GENERATION_TODAY,
                parent,
                502,
                scale=0.1,
                device_obj=device_obj,
            )
            await register_single_sensor(
                daily_conf,
                CONF_DAILY_GRID_CONNECTION_TIME,
                parent,
                503,
                scale=1.0,
                device_obj=device_obj,
            )

        if CONF_TOTAL in stats_conf:
            total_conf = stats_conf[CONF_TOTAL]
            # 32-bit values
            await register_single_sensor(
                total_conf,
                CONF_PRODUCTION,
                parent,
                504,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_BATTERY_CHARGE,
                parent,
                516,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_BATTERY_DISCHARGE,
                parent,
                518,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_GRID_IMPORT,
                parent,
                522,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_GRID_EXPORT,
                parent,
                524,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_CONSUMPTION,
                parent,
                527,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_PV_PRODUCTION,
                parent,
                534,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_ACTIVE_POWER_GENERATION,
                parent,
                504,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_REACTIVE_POWER_GENERATION,
                parent,
                506,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_BATTERY_CHARGE_32,
                parent,
                516,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_BATTERY_DISCHARGE_32,
                parent,
                518,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_GRID_IMPORT_32,
                parent,
                522,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_GRID_EXPORT_32,
                parent,
                524,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_CONSUMPTION_32,
                parent,
                527,
                scale=0.1,
                value_type="U_DWORD_R",
                device_obj=device_obj,
            )

    # =============================================================================
    # PROCESS STATUS SENSORS
    # =============================================================================
    if CONF_STATUS in config:
        status_conf = config[CONF_STATUS]
        await register_single_sensor(
            status_conf,
            CONF_WARNING_1_RAW,
            parent,
            230,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            status_conf,
            CONF_WARNING_2_RAW,
            parent,
            231,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            status_conf, CONF_ERROR_1_RAW, parent, 232, scale=1.0, device_obj=device_obj
        )
        await register_single_sensor(
            status_conf, CONF_ERROR_2_RAW, parent, 233, scale=1.0, device_obj=device_obj
        )
        await register_single_sensor(
            status_conf, CONF_ERROR_3_RAW, parent, 234, scale=1.0, device_obj=device_obj
        )
        await register_single_sensor(
            status_conf, CONF_ERROR_4_RAW, parent, 235, scale=1.0, device_obj=device_obj
        )
        await register_single_sensor(
            status_conf,
            CONF_COMMUNICATION_BOARD_FAILURE,
            parent,
            545,
            scale=1.0,
            device_obj=device_obj,
        )

        # Status Raw Sensors
        await register_single_sensor(
            status_conf,
            CONF_RUNNING_STATUS,
            parent,
            500,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            status_conf,
            CONF_TURN_OFF_ON_STATUS,
            parent,
            551,
            scale=1.0,
            device_obj=device_obj,
        )
        await register_single_sensor(
            status_conf,
            CONF_AC_INV_RELAY,
            parent,
            552,
            scale=1.0,
            device_obj=device_obj,
        )
