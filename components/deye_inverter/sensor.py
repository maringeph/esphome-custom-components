import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.components.modbus_controller import ModbusController
from esphome.const import (
    CONF_ID,
    CONF_DEVICE_ID,
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

AUTO_LOAD = ["modbus_controller"]
CODEOWNERS = ["@maringeph"]

# =============================================================================
# CONF CONSTANTS
# =============================================================================
CONF_MODBUS_ID = "modbus_id"
CONF_ADDRESS = "address"
CONF_UPDATE_INTERVAL_LIVE = "update_interval_live"
CONF_UPDATE_INTERVAL_STATISTICS = "update_interval_statistics"
CONF_UPDATE_INTERVAL_DEVICE_INFO = "update_interval_device_info"

# Device Info
CONF_DEVICE_INFO = "device_info"
CONF_DEVICE_TYPE = "device_type"
CONF_MODBUS_ADDRESS = "modbus_address"
CONF_DEVICE_INFO_EXTENDED = "device_info_extended"
CONF_SERIAL_NUMBER = "serial_number"
CONF_FIRMWARE_VERSION = "firmware_version"
CONF_HARDWARE_VERSION = "hardware_version"
CONF_DEVICE_TYPE_CODE = "device_type_code"
CONF_INVERTER_MODEL = "inverter_model"
CONF_INVERTER_POWER_RATING = "inverter_power_rating"
CONF_INVERTER_VOLTAGE_RATING = "inverter_voltage_rating"
CONF_INVERTER_CURRENT_RATING = "inverter_current_rating"
CONF_GRID_FREQUENCY_RATING = "grid_frequency_rating"

# Sensor Groups
CONF_BATTERY = "battery"
CONF_BATTERY_VOLTAGE = "voltage"
CONF_BATTERY_CURRENT = "current"
CONF_BATTERY_POWER = "power"
CONF_BATTERY_SOC = "soc"
CONF_BATTERY_TEMPERATURE = "temperature"
CONF_BATTERY_CAPACITY = "capacity"

CONF_PV1 = "pv1"
CONF_PV2 = "pv2"
CONF_PV3 = "pv3"
CONF_PV4 = "pv4"
CONF_PV_VOLTAGE = "voltage"
CONF_PV_CURRENT = "current"
CONF_PV_POWER = "power"

CONF_GRID = "grid"
CONF_GRID_VOLTAGE_L1 = "voltage_l1"
CONF_GRID_VOLTAGE_L2 = "voltage_l2"
CONF_GRID_VOLTAGE_L3 = "voltage_l3"
CONF_GRID_VOLTAGE_L1_L2 = "voltage_l1_l2"
CONF_GRID_VOLTAGE_L2_L3 = "voltage_l2_l3"
CONF_GRID_VOLTAGE_L3_L1 = "voltage_l3_l1"
CONF_GRID_POWER_L1 = "power_l1"
CONF_GRID_POWER_L2 = "power_l2"
CONF_GRID_POWER_L3 = "power_l3"
CONF_GRID_POWER_TOTAL = "power_total"
CONF_GRID_FREQUENCY = "frequency"
CONF_GRID_CURRENT_L1 = "current_l1"
CONF_GRID_CURRENT_L2 = "current_l2"
CONF_GRID_CURRENT_L3 = "current_l3"
CONF_INTERNAL_CT_L1_POWER = "internal_ct_l1_power"
CONF_INTERNAL_CT_L2_POWER = "internal_ct_l2_power"
CONF_INTERNAL_CT_L3_POWER = "internal_ct_l3_power"
CONF_INTERNAL_TOTAL_POWER = "internal_total_power"
CONF_EXTERNAL_CT_L1_POWER = "external_ct_l1_power"
CONF_EXTERNAL_CT_L2_POWER = "external_ct_l2_power"
CONF_EXTERNAL_CT_L3_POWER = "external_ct_l3_power"
CONF_OUT_OF_GRID_TOTAL_POWER = "out_of_grid_total_power"
CONF_GRID_METER_APPARENT_POWER = "grid_meter_apparent_power"
CONF_GRID_METER_POWER_FACTOR = "grid_meter_power_factor"
CONF_GRID_METER_CURRENT_L1 = "grid_meter_current_l1"
CONF_GRID_METER_CURRENT_L2 = "grid_meter_current_l2"
CONF_GRID_METER_CURRENT_L3 = "grid_meter_current_l3"
CONF_GRID_SIDE_A_PHASE_POWER = "grid_side_a_phase_power"
CONF_GRID_SIDE_B_PHASE_POWER = "grid_side_b_phase_power"
CONF_GRID_SIDE_C_PHASE_POWER = "grid_side_c_phase_power"
CONF_GRID_SIDE_TOTAL_POWER = "grid_side_total_power"
CONF_TOTAL_GRID_POWER = "total_grid_power"

CONF_LOAD_GRID = "load_grid"
CONF_LOAD_GRID_POWER_L1 = "power_l1"
CONF_LOAD_GRID_POWER_L2 = "power_l2"
CONF_LOAD_GRID_POWER_L3 = "power_l3"
CONF_LOAD_GRID_POWER_TOTAL = "power_total"
CONF_LOAD_GRID_VOLTAGE_L1 = "voltage_l1"
CONF_LOAD_GRID_VOLTAGE_L2 = "voltage_l2"
CONF_LOAD_GRID_VOLTAGE_L3 = "voltage_l3"

CONF_LOAD_GRID_PORT = "load_grid_port"
CONF_LOAD_PORT_VOLTAGE_L1 = "load_port_voltage_l1"
CONF_LOAD_PORT_VOLTAGE_L2 = "load_port_voltage_l2"
CONF_LOAD_PORT_VOLTAGE_L3 = "load_port_voltage_l3"
CONF_LOAD_PORT_CURRENT_L1 = "load_port_current_l1"
CONF_LOAD_PORT_CURRENT_L2 = "load_port_current_l2"
CONF_LOAD_PORT_CURRENT_L3 = "load_port_current_l3"
CONF_LOAD_PORT_POWER_L1 = "load_port_power_l1"
CONF_LOAD_PORT_POWER_L2 = "load_port_power_l2"
CONF_LOAD_PORT_POWER_L3 = "load_port_power_l3"
CONF_LOAD_REAL_POWER = "load_real_power"
CONF_LOAD_APPARENT_POWER = "load_apparent_power"
CONF_LOAD_FREQUENCY = "load_frequency"

CONF_LOAD_UPS = "load_ups"
CONF_LOAD_UPS_POWER_L1 = "power_l1"
CONF_LOAD_UPS_POWER_L2 = "power_l2"
CONF_LOAD_UPS_POWER_L3 = "power_l3"
CONF_LOAD_UPS_POWER_TOTAL = "power_total"
CONF_LOAD_UPS_VOLTAGE_L1 = "voltage_l1"
CONF_LOAD_UPS_VOLTAGE_L2 = "voltage_l2"
CONF_LOAD_UPS_VOLTAGE_L3 = "voltage_l3"
CONF_LOAD_UPS_FREQUENCY = "frequency"

CONF_GENERATOR = "generator"
CONF_GENERATOR_VOLTAGE_L1 = "voltage_l1"
CONF_GENERATOR_VOLTAGE_L2 = "voltage_l2"
CONF_GENERATOR_VOLTAGE_L3 = "voltage_l3"
CONF_GENERATOR_POWER_L1 = "power_l1"
CONF_GENERATOR_POWER_L2 = "power_l2"
CONF_GENERATOR_POWER_L3 = "power_l3"
CONF_GENERATOR_POWER_TOTAL = "power_total"
CONF_GENERATOR_CURRENT_L1 = "current_l1"
CONF_GENERATOR_CURRENT_L2 = "current_l2"
CONF_GENERATOR_CURRENT_L3 = "current_l3"
CONF_GENERATOR_FREQUENCY = "frequency"

CONF_GENERATOR_PORT = "generator_port"
CONF_GEN_PORT_VOLTAGE_L1 = "gen_port_voltage_l1"
CONF_GEN_PORT_VOLTAGE_L2 = "gen_port_voltage_l2"
CONF_GEN_PORT_VOLTAGE_L3 = "gen_port_voltage_l3"
CONF_GEN_PORT_POWER_L1 = "gen_port_power_l1"
CONF_GEN_PORT_POWER_L2 = "gen_port_power_l2"
CONF_GEN_PORT_POWER_L3 = "gen_port_power_l3"
CONF_GEN_PORT_POWER_TOTAL = "gen_port_power_total"
CONF_GEN_PORT_CURRENT_L1 = "gen_port_current_l1"
CONF_GEN_PORT_CURRENT_L2 = "gen_port_current_l2"
CONF_GEN_PORT_CURRENT_L3 = "gen_port_current_l3"
CONF_GEN_PORT_FREQUENCY = "gen_port_frequency"

CONF_TEMPERATURES = "temperatures"
CONF_TEMP_HEATSINK = "heatsink"
CONF_TEMP_DC_TRANSFORMER = "dc_transformer"

CONF_INVERTER = "inverter"
CONF_INVERTER_VOLTAGE_L1 = "voltage_l1"
CONF_INVERTER_VOLTAGE_L2 = "voltage_l2"
CONF_INVERTER_VOLTAGE_L3 = "voltage_l3"
CONF_INVERTER_REAL_POWER_L1 = "real_power_l1"
CONF_INVERTER_REAL_POWER_L2 = "real_power_l2"
CONF_INVERTER_REAL_POWER_L3 = "real_power_l3"
CONF_INVERTER_REAL_POWER = "real_power"
CONF_INVERTER_APPARENT_POWER = "apparent_power"
CONF_INVERTER_FREQUENCY = "frequency"

CONF_DC = "dc"
CONF_DC5_CURRENT = "dc5_current"
CONF_DC6_VOLTAGE = "dc6_voltage"
CONF_DC6_CURRENT = "dc6_current"
CONF_DC7_VOLTAGE = "dc7_voltage"
CONF_DC7_CURRENT = "dc7_current"
CONF_DC8_VOLTAGE = "dc8_voltage"
CONF_DC8_CURRENT = "dc8_current"

CONF_BATTERY_MODULE_1 = "battery_module_1"
CONF_BATTERY_MODULE_2 = "battery_module_2"
CONF_BATTERY_MODULE_3 = "battery_module_3"
CONF_BATTERY_MODULE_4 = "battery_module_4"
CONF_BATTERY_MODULE_5 = "battery_module_5"
CONF_BATTERY_MODULE_6 = "battery_module_6"
CONF_BATTERY_MODULE_7 = "battery_module_7"
CONF_BATTERY_MODULE_8 = "battery_module_8"
CONF_BATTERY_MODULE_9 = "battery_module_9"

CONF_BM_VOLTAGE = "voltage"
CONF_BM_CURRENT = "current"
CONF_BM_SOC = "soc"
CONF_BM_TEMPERATURE = "temperature"
CONF_BM_STATUS = "status"
CONF_BM_FAULT_CODE = "fault_code"
CONF_BM_CYCLE_COUNT = "cycle_count"
CONF_BM_CAPACITY_REMAINING = "capacity_remaining"
CONF_BM_CAPACITY_TOTAL = "capacity_total"
CONF_BM_POWER = "power"
CONF_BM_CELL_MAX_VOLTAGE = "cell_max_voltage"
CONF_BM_CELL_MIN_VOLTAGE = "cell_min_voltage"
CONF_BM_CELL_MAX_TEMP = "cell_max_temp"
CONF_BM_CELL_MIN_TEMP = "cell_min_temp"

CONF_STATISTICS = "statistics"
CONF_DAILY = "daily"
CONF_TOTAL = "total"
CONF_PRODUCTION = "production"
CONF_BATTERY_CHARGE = "battery_charge"
CONF_BATTERY_DISCHARGE = "battery_discharge"
CONF_GRID_IMPORT = "grid_import"
CONF_GRID_EXPORT = "grid_export"
CONF_CONSUMPTION = "consumption"
CONF_PV_PRODUCTION = "pv_production"
CONF_DAILY_PV1_PRODUCTION = "pv1_production"
CONF_DAILY_PV2_PRODUCTION = "pv2_production"
CONF_DAILY_PV3_PRODUCTION = "pv3_production"
CONF_DAILY_PV4_PRODUCTION = "pv4_production"
CONF_DAILY_GENERATOR_ON_TIME = "generator_on_time"
CONF_DAILY_ACTIVE_POWER_GENERATION = "daily_active_power_generation"
CONF_ACTIVE_POWER_GENERATION_TODAY = "active_power_generation_today"
CONF_DAILY_GRID_CONNECTION_TIME = "daily_grid_connection_time"
CONF_TOTAL_ACTIVE_POWER_GENERATION = "total_active_power_generation"
CONF_TOTAL_REACTIVE_POWER_GENERATION = "total_reactive_power_generation"
CONF_TOTAL_BATTERY_CHARGE_32 = "total_battery_charge"
CONF_TOTAL_BATTERY_DISCHARGE_32 = "total_battery_discharge"
CONF_TOTAL_GRID_IMPORT_32 = "total_grid_import"
CONF_TOTAL_GRID_EXPORT_32 = "total_grid_export"
CONF_TOTAL_CONSUMPTION_32 = "total_consumption"
CONF_ACTIVE_POWER_GEN_TOTAL_LOW = "active_power_gen_total_low"
CONF_ACTIVE_POWER_GEN_TOTAL_HIGH = "active_power_gen_total_high"
CONF_REACTIVE_POWER_GEN_TOTAL_LOW = "reactive_power_gen_total_low"
CONF_REACTIVE_POWER_GEN_TOTAL_HIGH = "reactive_power_gen_total_high"
CONF_TOTAL_PV_PRODUCTION = "total_pv_production"
CONF_BATTERY_CHARGE_TOTAL_HIGH = "battery_charge_total_high"
CONF_BATTERY_DISCHARGE_TOTAL_HIGH = "battery_discharge_total_high"
CONF_TOTAL_GRID_BUY_HIGH = "total_grid_buy_high"
CONF_TOTAL_GRID_SELL_HIGH = "total_grid_sell_high"
CONF_TOTAL_LOAD_HIGH = "total_load_high"

# Status
CONF_STATUS = "status"
CONF_RUNNING_STATUS = "running_status"
CONF_WARNING_1_RAW = "warning_1_raw"
CONF_WARNING_2_RAW = "warning_2_raw"
CONF_ERROR_1_RAW = "error_1_raw"
CONF_ERROR_2_RAW = "error_2_raw"
CONF_ERROR_3_RAW = "error_3_raw"
CONF_ERROR_4_RAW = "error_4_raw"
CONF_COMMUNICATION_BOARD_FAILURE = "communication_board_failure"

# =============================================================================
# NAMESPACE
# =============================================================================
deye_inverter_ns = cg.esphome_ns.namespace("deye_inverter")
DeyeInverter = deye_inverter_ns.class_(
    "DeyeInverter", cg.PollingComponent, cg.Parented.template(ModbusController)
)

# =============================================================================
# ENTITY SCHEMAS
# =============================================================================
ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_ID): cv.declare_id(sensor.Sensor),
    }
)

# =============================================================================
# DEVICE INFO SCHEMAS
# =============================================================================
DEVICE_INFO_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_DEVICE_TYPE): ENTITY_SCHEMA,
        cv.Optional(CONF_MODBUS_ADDRESS): ENTITY_SCHEMA,
    }
)

DEVICE_INFO_EXTENDED_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SERIAL_NUMBER): ENTITY_SCHEMA,
        cv.Optional(CONF_FIRMWARE_VERSION): ENTITY_SCHEMA,
        cv.Optional(CONF_HARDWARE_VERSION): ENTITY_SCHEMA,
        cv.Optional(CONF_DEVICE_TYPE_CODE): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_MODEL): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_POWER_RATING): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_VOLTAGE_RATING): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_CURRENT_RATING): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_FREQUENCY_RATING): ENTITY_SCHEMA,
    }
)

# =============================================================================
# SENSOR GROUP SCHEMAS - Live Data
# =============================================================================
PV_STRING_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_PV_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_PV_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_PV_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

BATTERY_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_SOC): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_BATTERY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BATTERY_CAPACITY): sensor.sensor_schema(
            unit_of_measurement="Ah",
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

BATTERY_MODULE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BM_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_SOC): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_BATTERY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_STATUS): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_FAULT_CODE): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CYCLE_COUNT): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BM_CAPACITY_REMAINING): sensor.sensor_schema(
            unit_of_measurement="Ah",
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CAPACITY_TOTAL): sensor.sensor_schema(
            unit_of_measurement="Ah",
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CELL_MAX_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CELL_MIN_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CELL_MAX_TEMP): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_BM_CELL_MIN_TEMP): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GRID_VOLTAGE_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L1_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L2_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_VOLTAGE_L3_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_CURRENT_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_CURRENT_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_CURRENT_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_POWER_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_POWER_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_POWER_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_POWER_TOTAL): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_FREQUENCY): sensor.sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_SIDE_A_PHASE_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_SIDE_B_PHASE_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_SIDE_C_PHASE_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GRID_SIDE_TOTAL_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_TOTAL_GRID_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

LOAD_GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_POWER_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_POWER_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_POWER_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_GRID_POWER_TOTAL): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

LOAD_GRID_PORT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_CURRENT_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_CURRENT_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_CURRENT_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_POWER_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_POWER_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_PORT_POWER_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_REAL_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_APPARENT_POWER): sensor.sensor_schema(
            unit_of_measurement="VA",
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_FREQUENCY): sensor.sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

LOAD_UPS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_POWER_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_POWER_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_POWER_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_POWER_TOTAL): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_LOAD_UPS_FREQUENCY): sensor.sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

GENERATOR_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GENERATOR_VOLTAGE_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_VOLTAGE_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_VOLTAGE_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_CURRENT_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_CURRENT_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_CURRENT_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_POWER_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_POWER_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_POWER_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_POWER_TOTAL): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GENERATOR_FREQUENCY): sensor.sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

GENERATOR_PORT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_CURRENT_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_CURRENT_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_CURRENT_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_POWER_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_POWER_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_POWER_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_POWER_TOTAL): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_GEN_PORT_FREQUENCY): sensor.sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

TEMPERATURES_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_TEMP_HEATSINK): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_TEMP_DC_TRANSFORMER): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

INVERTER_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_INVERTER_VOLTAGE_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_VOLTAGE_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_VOLTAGE_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_REAL_POWER_L1): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_REAL_POWER_L2): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_REAL_POWER_L3): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_REAL_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_APPARENT_POWER): sensor.sensor_schema(
            unit_of_measurement="VA",
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_INVERTER_FREQUENCY): sensor.sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_FREQUENCY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

DC_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_DC5_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC6_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC6_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC7_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC7_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC8_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DC8_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# =============================================================================
# STATISTICS SCHEMAS
# =============================================================================
DAILY_STATISTICS_SCHEMA = cv.Schema(
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
        cv.Optional(CONF_DAILY_PV1_PRODUCTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_PV2_PRODUCTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_PV3_PRODUCTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_PV4_PRODUCTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_GENERATOR_ON_TIME): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOUR,
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_DAILY_ACTIVE_POWER_GENERATION): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_ACTIVE_POWER_GENERATION_TODAY): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_DAILY_GRID_CONNECTION_TIME): sensor.sensor_schema(
            unit_of_measurement=UNIT_MINUTE,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

TOTAL_STATISTICS_SCHEMA = cv.Schema(
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
        cv.Optional(CONF_TOTAL_ACTIVE_POWER_GENERATION): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_REACTIVE_POWER_GENERATION): sensor.sensor_schema(
            unit_of_measurement="kVARh",
            accuracy_decimals=1,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_BATTERY_CHARGE_32): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_BATTERY_DISCHARGE_32): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_GRID_IMPORT_32): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_GRID_EXPORT_32): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_CONSUMPTION_32): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_ACTIVE_POWER_GEN_TOTAL_LOW): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_ACTIVE_POWER_GEN_TOTAL_HIGH): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_REACTIVE_POWER_GEN_TOTAL_LOW): sensor.sensor_schema(
            unit_of_measurement="kVARh",
            accuracy_decimals=1,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_REACTIVE_POWER_GEN_TOTAL_HIGH): sensor.sensor_schema(
            unit_of_measurement="kVARh",
            accuracy_decimals=1,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_PV_PRODUCTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_CHARGE_TOTAL_HIGH): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_BATTERY_DISCHARGE_TOTAL_HIGH): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_GRID_BUY_HIGH): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_GRID_SELL_HIGH): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_TOTAL_LOAD_HIGH): sensor.sensor_schema(
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

# =============================================================================
# STATUS SCHEMA
# =============================================================================
STATUS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_WARNING_1_RAW): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_WARNING_2_RAW): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ERROR_1_RAW): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ERROR_2_RAW): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ERROR_3_RAW): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ERROR_4_RAW): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_COMMUNICATION_BOARD_FAILURE): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

# =============================================================================
# PLATFORM SCHEMA - Erstellt die Komponente!
# =============================================================================
PLATFORM_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(DeyeInverter),
        cv.Required(CONF_MODBUS_ID): cv.use_id(ModbusController),
        cv.Optional(CONF_DEVICE_ID): cv.use_id(cg.EntityBase),
        cv.Optional(CONF_ADDRESS, default=1): cv.positive_int,
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
).extend(cv.polling_component_schema("1s"))


# =============================================================================
# HELPER FUNCTION
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
        cg.add(sens.set_data_type(getattr(deye_inverter_ns.DataType, value_type)))
    else:
        cg.add(sens.set_bytes(2))
        if signed:
            cg.add(sens.set_data_type(deye_inverter_ns.DataType.S_WORD))
        else:
            cg.add(sens.set_data_type(deye_inverter_ns.DataType.U_WORD))

    # Register with parent's sensor list
    cg.add(parent.register_sensor(sens))


# =============================================================================
# CODE GENERATION
# =============================================================================
async def to_code(config):
    """Generate code for the Deye Inverter component."""
    # Create the component instance
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    # Set the Modbus controller parent
    modbus = await cg.get_variable(config[CONF_MODBUS_ID])
    cg.add(var.set_parent(modbus))

    # Set the Modbus address
    cg.add(var.set_address(config[CONF_ADDRESS]))

    # Set update intervals
    cg.add(var.set_update_interval_live(config[CONF_UPDATE_INTERVAL_LIVE]))
    cg.add(var.set_update_interval_statistics(config[CONF_UPDATE_INTERVAL_STATISTICS]))
    cg.add(
        var.set_update_interval_device_info(config[CONF_UPDATE_INTERVAL_DEVICE_INFO])
    )

    # Set device ID if provided
    if CONF_DEVICE_ID in config:
        device = await cg.get_variable(config[CONF_DEVICE_ID])
        cg.add(var.set_device(device))

    # =============================================================================
    # PROCESS BATTERY SENSORS
    # =============================================================================
    if CONF_BATTERY in config:
        battery_conf = config[CONF_BATTERY]
        await register_sensor(battery_conf, CONF_BATTERY_VOLTAGE, var, 587, scale=0.1)
        await register_sensor(
            battery_conf, CONF_BATTERY_CURRENT, var, 591, scale=0.01, signed=True
        )
        await register_sensor(
            battery_conf, CONF_BATTERY_POWER, var, 590, scale=1.0, signed=True
        )
        await register_sensor(battery_conf, CONF_BATTERY_SOC, var, 588, scale=1.0)
        await register_sensor(
            battery_conf, CONF_BATTERY_TEMPERATURE, var, 586, scale=0.1, offset=-100.0
        )
        await register_sensor(battery_conf, CONF_BATTERY_CAPACITY, var, 592, scale=1.0)

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
            await register_sensor(
                pv_conf, CONF_PV_VOLTAGE, var, voltage_addr, scale=0.1
            )
            await register_sensor(
                pv_conf, CONF_PV_CURRENT, var, current_addr, scale=0.1
            )
            await register_sensor(pv_conf, CONF_PV_POWER, var, base_addr, scale=1.0)

    # =============================================================================
    # PROCESS GRID SENSORS
    # =============================================================================
    if CONF_GRID in config:
        grid_conf = config[CONF_GRID]
        await register_sensor(grid_conf, CONF_GRID_VOLTAGE_L1, var, 598, scale=0.1)
        await register_sensor(grid_conf, CONF_GRID_VOLTAGE_L2, var, 599, scale=0.1)
        await register_sensor(grid_conf, CONF_GRID_VOLTAGE_L3, var, 600, scale=0.1)
        await register_sensor(grid_conf, CONF_GRID_CURRENT_L1, var, 610, scale=0.01)
        await register_sensor(grid_conf, CONF_GRID_CURRENT_L2, var, 611, scale=0.01)
        await register_sensor(grid_conf, CONF_GRID_CURRENT_L3, var, 612, scale=0.01)
        await register_sensor(
            grid_conf, CONF_GRID_POWER_L1, var, 604, scale=1.0, signed=True
        )
        await register_sensor(
            grid_conf, CONF_GRID_POWER_L2, var, 605, scale=1.0, signed=True
        )
        await register_sensor(
            grid_conf, CONF_GRID_POWER_L3, var, 606, scale=1.0, signed=True
        )
        await register_sensor(
            grid_conf, CONF_GRID_POWER_TOTAL, var, 607, scale=1.0, signed=True
        )
        await register_sensor(grid_conf, CONF_GRID_FREQUENCY, var, 609, scale=0.01)
        await register_sensor(
            grid_conf, CONF_GRID_SIDE_A_PHASE_POWER, var, 622, scale=1.0
        )
        await register_sensor(
            grid_conf, CONF_GRID_SIDE_B_PHASE_POWER, var, 623, scale=1.0
        )
        await register_sensor(
            grid_conf, CONF_GRID_SIDE_C_PHASE_POWER, var, 624, scale=1.0
        )
        await register_sensor(
            grid_conf, CONF_TOTAL_GRID_POWER, var, 625, scale=1.0, signed=True
        )
        await register_sensor(
            grid_conf, CONF_GRID_SIDE_TOTAL_POWER, var, 626, scale=1.0
        )

    # =============================================================================
    # PROCESS LOAD GRID SENSORS
    # =============================================================================
    if CONF_LOAD_GRID in config:
        load_grid_conf = config[CONF_LOAD_GRID]
        await register_sensor(
            load_grid_conf, CONF_LOAD_GRID_VOLTAGE_L1, var, 644, scale=0.1
        )
        await register_sensor(
            load_grid_conf, CONF_LOAD_GRID_VOLTAGE_L2, var, 645, scale=0.1
        )
        await register_sensor(
            load_grid_conf, CONF_LOAD_GRID_VOLTAGE_L3, var, 646, scale=0.1
        )
        await register_sensor(
            load_grid_conf, CONF_LOAD_GRID_POWER_L1, var, 650, scale=1.0
        )
        await register_sensor(
            load_grid_conf, CONF_LOAD_GRID_POWER_L2, var, 651, scale=1.0
        )
        await register_sensor(
            load_grid_conf, CONF_LOAD_GRID_POWER_L3, var, 652, scale=1.0
        )
        await register_sensor(
            load_grid_conf, CONF_LOAD_GRID_POWER_TOTAL, var, 653, scale=1.0
        )

    # =============================================================================
    # PROCESS LOAD GRID PORT SENSORS
    # =============================================================================
    if CONF_LOAD_GRID_PORT in config:
        load_port_conf = config[CONF_LOAD_GRID_PORT]
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_VOLTAGE_L1, var, 644, scale=0.1
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_VOLTAGE_L2, var, 645, scale=0.1
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_VOLTAGE_L3, var, 646, scale=0.1
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_CURRENT_L1, var, 647, scale=0.01, signed=True
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_CURRENT_L2, var, 648, scale=0.01, signed=True
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_CURRENT_L3, var, 649, scale=0.01, signed=True
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_POWER_L1, var, 650, scale=1.0, signed=True
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_POWER_L2, var, 651, scale=1.0, signed=True
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_PORT_POWER_L3, var, 652, scale=1.0, signed=True
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_REAL_POWER, var, 653, scale=1.0, signed=True
        )
        await register_sensor(
            load_port_conf, CONF_LOAD_APPARENT_POWER, var, 654, scale=1.0, signed=True
        )
        await register_sensor(load_port_conf, CONF_LOAD_FREQUENCY, var, 655, scale=0.01)

    # =============================================================================
    # PROCESS LOAD UPS SENSORS
    # =============================================================================
    if CONF_LOAD_UPS in config:
        load_ups_conf = config[CONF_LOAD_UPS]
        await register_sensor(
            load_ups_conf, CONF_LOAD_UPS_VOLTAGE_L1, var, 627, scale=0.1
        )
        await register_sensor(
            load_ups_conf, CONF_LOAD_UPS_VOLTAGE_L2, var, 628, scale=0.1
        )
        await register_sensor(
            load_ups_conf, CONF_LOAD_UPS_VOLTAGE_L3, var, 629, scale=0.1
        )
        await register_sensor(
            load_ups_conf, CONF_LOAD_UPS_POWER_L1, var, 640, scale=1.0
        )
        await register_sensor(
            load_ups_conf, CONF_LOAD_UPS_POWER_L2, var, 641, scale=1.0
        )
        await register_sensor(
            load_ups_conf, CONF_LOAD_UPS_POWER_L3, var, 642, scale=1.0
        )
        await register_sensor(
            load_ups_conf, CONF_LOAD_UPS_POWER_TOTAL, var, 643, scale=1.0
        )
        await register_sensor(
            load_ups_conf, CONF_LOAD_UPS_FREQUENCY, var, 638, scale=0.01
        )

    # =============================================================================
    # PROCESS GENERATOR SENSORS
    # =============================================================================
    if CONF_GENERATOR in config:
        gen_conf = config[CONF_GENERATOR]
        await register_sensor(gen_conf, CONF_GENERATOR_VOLTAGE_L1, var, 661, scale=0.1)
        await register_sensor(gen_conf, CONF_GENERATOR_VOLTAGE_L2, var, 662, scale=0.1)
        await register_sensor(gen_conf, CONF_GENERATOR_VOLTAGE_L3, var, 663, scale=0.1)
        await register_sensor(gen_conf, CONF_GENERATOR_CURRENT_L1, var, 668, scale=0.01)
        await register_sensor(gen_conf, CONF_GENERATOR_CURRENT_L2, var, 669, scale=0.01)
        await register_sensor(gen_conf, CONF_GENERATOR_CURRENT_L3, var, 670, scale=0.01)
        await register_sensor(gen_conf, CONF_GENERATOR_POWER_L1, var, 664, scale=1.0)
        await register_sensor(gen_conf, CONF_GENERATOR_POWER_L2, var, 665, scale=1.0)
        await register_sensor(gen_conf, CONF_GENERATOR_POWER_L3, var, 666, scale=1.0)
        await register_sensor(gen_conf, CONF_GENERATOR_POWER_TOTAL, var, 667, scale=1.0)
        await register_sensor(gen_conf, CONF_GENERATOR_FREQUENCY, var, 671, scale=0.01)

    # =============================================================================
    # PROCESS GENERATOR PORT SENSORS
    # =============================================================================
    if CONF_GENERATOR_PORT in config:
        gen_port_conf = config[CONF_GENERATOR_PORT]
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_VOLTAGE_L1, var, 661, scale=0.1
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_VOLTAGE_L2, var, 662, scale=0.1
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_VOLTAGE_L3, var, 663, scale=0.1
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_CURRENT_L1, var, 668, scale=0.01, signed=True
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_CURRENT_L2, var, 669, scale=0.01, signed=True
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_CURRENT_L3, var, 670, scale=0.01, signed=True
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_POWER_L1, var, 664, scale=1.0, signed=True
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_POWER_L2, var, 665, scale=1.0, signed=True
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_POWER_L3, var, 666, scale=1.0, signed=True
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_POWER_TOTAL, var, 667, scale=1.0, signed=True
        )
        await register_sensor(
            gen_port_conf, CONF_GEN_PORT_FREQUENCY, var, 671, scale=0.01
        )

    # =============================================================================
    # PROCESS INVERTER SENSORS
    # =============================================================================
    if CONF_INVERTER in config:
        inverter_conf = config[CONF_INVERTER]
        await register_sensor(
            inverter_conf, CONF_INVERTER_VOLTAGE_L1, var, 627, scale=0.1
        )
        await register_sensor(
            inverter_conf, CONF_INVERTER_VOLTAGE_L2, var, 628, scale=0.1
        )
        await register_sensor(
            inverter_conf, CONF_INVERTER_VOLTAGE_L3, var, 629, scale=0.1
        )
        await register_sensor(
            inverter_conf, CONF_INVERTER_REAL_POWER_L1, var, 633, scale=1.0, signed=True
        )
        await register_sensor(
            inverter_conf, CONF_INVERTER_REAL_POWER_L2, var, 634, scale=1.0, signed=True
        )
        await register_sensor(
            inverter_conf, CONF_INVERTER_REAL_POWER_L3, var, 635, scale=1.0, signed=True
        )
        await register_sensor(
            inverter_conf, CONF_INVERTER_REAL_POWER, var, 636, scale=1.0, signed=True
        )
        await register_sensor(
            inverter_conf,
            CONF_INVERTER_APPARENT_POWER,
            var,
            637,
            scale=1.0,
            signed=True,
        )
        await register_sensor(
            inverter_conf, CONF_INVERTER_FREQUENCY, var, 638, scale=0.01
        )

    # =============================================================================
    # PROCESS DC SENSORS
    # =============================================================================
    if CONF_DC in config:
        dc_conf = config[CONF_DC]
        await register_sensor(dc_conf, CONF_DC5_CURRENT, var, 212, scale=0.1)
        await register_sensor(dc_conf, CONF_DC6_VOLTAGE, var, 213, scale=0.1)
        await register_sensor(dc_conf, CONF_DC6_CURRENT, var, 214, scale=0.1)
        await register_sensor(dc_conf, CONF_DC7_VOLTAGE, var, 215, scale=0.1)
        await register_sensor(dc_conf, CONF_DC7_CURRENT, var, 216, scale=0.1)
        await register_sensor(dc_conf, CONF_DC8_VOLTAGE, var, 217, scale=0.1)
        await register_sensor(dc_conf, CONF_DC8_CURRENT, var, 218, scale=0.1)

    # =============================================================================
    # PROCESS TEMPERATURE SENSORS
    # =============================================================================
    if CONF_TEMPERATURES in config:
        temp_conf = config[CONF_TEMPERATURES]
        await register_sensor(
            temp_conf, CONF_TEMP_DC_TRANSFORMER, var, 540, scale=0.1, offset=-100.0
        )
        await register_sensor(
            temp_conf, CONF_TEMP_HEATSINK, var, 541, scale=0.1, offset=-100.0
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
            await register_sensor(
                bm_conf, CONF_BM_VOLTAGE, var, base_address, scale=0.01
            )
            await register_sensor(
                bm_conf, CONF_BM_CURRENT, var, base_address + 1, scale=0.01, signed=True
            )
            await register_sensor(
                bm_conf, CONF_BM_SOC, var, base_address + 2, scale=1.0
            )
            await register_sensor(
                bm_conf,
                CONF_BM_TEMPERATURE,
                var,
                base_address + 3,
                scale=0.1,
                offset=-100.0,
            )
            await register_sensor(
                bm_conf, CONF_BM_STATUS, var, base_address + 4, scale=1.0
            )
            await register_sensor(
                bm_conf, CONF_BM_FAULT_CODE, var, base_address + 5, scale=1.0
            )
            await register_sensor(
                bm_conf, CONF_BM_CYCLE_COUNT, var, base_address + 6, scale=1.0
            )
            await register_sensor(
                bm_conf, CONF_BM_CAPACITY_REMAINING, var, base_address + 7, scale=0.1
            )
            await register_sensor(
                bm_conf, CONF_BM_CAPACITY_TOTAL, var, base_address + 8, scale=0.1
            )
            await register_sensor(
                bm_conf, CONF_BM_POWER, var, base_address + 9, scale=1.0, signed=True
            )
            await register_sensor(
                bm_conf, CONF_BM_CELL_MAX_VOLTAGE, var, base_address + 10, scale=0.001
            )
            await register_sensor(
                bm_conf, CONF_BM_CELL_MIN_VOLTAGE, var, base_address + 11, scale=0.001
            )
            await register_sensor(
                bm_conf,
                CONF_BM_CELL_MAX_TEMP,
                var,
                base_address + 12,
                scale=0.1,
                offset=-100.0,
            )
            await register_sensor(
                bm_conf,
                CONF_BM_CELL_MIN_TEMP,
                var,
                base_address + 13,
                scale=0.1,
                offset=-100.0,
            )

    # =============================================================================
    # PROCESS STATISTICS SENSORS
    # =============================================================================
    if CONF_STATISTICS in config:
        stats_conf = config[CONF_STATISTICS]

        if CONF_DAILY in stats_conf:
            daily_conf = stats_conf[CONF_DAILY]
            await register_sensor(daily_conf, CONF_PRODUCTION, var, 501, scale=0.1)
            await register_sensor(daily_conf, CONF_BATTERY_CHARGE, var, 514, scale=0.1)
            await register_sensor(
                daily_conf, CONF_BATTERY_DISCHARGE, var, 515, scale=0.1
            )
            await register_sensor(daily_conf, CONF_GRID_IMPORT, var, 520, scale=0.1)
            await register_sensor(daily_conf, CONF_GRID_EXPORT, var, 521, scale=0.1)
            await register_sensor(daily_conf, CONF_CONSUMPTION, var, 526, scale=0.1)
            await register_sensor(daily_conf, CONF_PV_PRODUCTION, var, 529, scale=0.1)
            await register_sensor(
                daily_conf, CONF_DAILY_PV1_PRODUCTION, var, 530, scale=0.1
            )
            await register_sensor(
                daily_conf, CONF_DAILY_PV2_PRODUCTION, var, 531, scale=0.1
            )
            await register_sensor(
                daily_conf, CONF_DAILY_PV3_PRODUCTION, var, 532, scale=0.1
            )
            await register_sensor(
                daily_conf, CONF_DAILY_PV4_PRODUCTION, var, 533, scale=0.1
            )
            await register_sensor(
                daily_conf, CONF_DAILY_GENERATOR_ON_TIME, var, 539, scale=0.1
            )
            await register_sensor(
                daily_conf, CONF_DAILY_ACTIVE_POWER_GENERATION, var, 501, scale=0.1
            )
            await register_sensor(
                daily_conf, CONF_ACTIVE_POWER_GENERATION_TODAY, var, 502, scale=0.1
            )
            await register_sensor(
                daily_conf, CONF_DAILY_GRID_CONNECTION_TIME, var, 503, scale=1.0
            )

        if CONF_TOTAL in stats_conf:
            total_conf = stats_conf[CONF_TOTAL]
            # 32-bit values
            await register_sensor(
                total_conf, CONF_PRODUCTION, var, 504, scale=0.1, value_type="U_DWORD_R"
            )
            await register_sensor(
                total_conf,
                CONF_BATTERY_CHARGE,
                var,
                516,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_BATTERY_DISCHARGE,
                var,
                518,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_GRID_IMPORT,
                var,
                522,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_GRID_EXPORT,
                var,
                524,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_CONSUMPTION,
                var,
                527,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_PV_PRODUCTION,
                var,
                534,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_TOTAL_ACTIVE_POWER_GENERATION,
                var,
                504,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_TOTAL_REACTIVE_POWER_GENERATION,
                var,
                506,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_TOTAL_BATTERY_CHARGE_32,
                var,
                516,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_TOTAL_BATTERY_DISCHARGE_32,
                var,
                518,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_TOTAL_GRID_IMPORT_32,
                var,
                522,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_TOTAL_GRID_EXPORT_32,
                var,
                524,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_sensor(
                total_conf,
                CONF_TOTAL_CONSUMPTION_32,
                var,
                527,
                scale=0.1,
                value_type="U_DWORD_R",
            )

    # =============================================================================
    # PROCESS STATUS SENSORS
    # =============================================================================
    if CONF_STATUS in config:
        status_conf = config[CONF_STATUS]
        await register_sensor(status_conf, CONF_WARNING_1_RAW, var, 230, scale=1.0)
        await register_sensor(status_conf, CONF_WARNING_2_RAW, var, 231, scale=1.0)
        await register_sensor(status_conf, CONF_ERROR_1_RAW, var, 232, scale=1.0)
        await register_sensor(status_conf, CONF_ERROR_2_RAW, var, 233, scale=1.0)
        await register_sensor(status_conf, CONF_ERROR_3_RAW, var, 234, scale=1.0)
        await register_sensor(status_conf, CONF_ERROR_4_RAW, var, 235, scale=1.0)
        await register_sensor(
            status_conf, CONF_COMMUNICATION_BOARD_FAILURE, var, 545, scale=1.0
        )

    return var
