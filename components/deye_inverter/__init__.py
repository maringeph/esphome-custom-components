"""Deye Inverter component for ESPHome.

This component provides integration with Deye solar inverters via Modbus.
Based on register analysis: 595 registers total (298 existing + 296 new)
- sensor: 365
- number: 89
- switch: 38
- select: 22
- text_sensor: 12
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import (
    sensor,
    text_sensor,
    binary_sensor,
    switch,
    select,
    number,
    datetime,
    time,
)
from esphome.components.modbus_controller import ModbusController, modbus_controller_ns
from esphome.components.modbus_controller.const import CONF_MODBUS_CONTROLLER_ID
from esphome.const import (
    CONF_ID,
    CONF_NAME,
    CONF_DEVICE_ID,
    CONF_DISABLED_BY_DEFAULT,
    CONF_UPDATE_INTERVAL,
)

# =============================================================================
# COMPONENT NAMESPACE
# =============================================================================
AUTO_LOAD = ["modbus_controller"]
CODEOWNERS = ["@maringeph"]
MULTI_CONF = True

# =============================================================================
# CONF CONSTANTS - Main Component
# =============================================================================
CONF_DEYE_INVERTER_ID = "deye_inverter_id"
CONF_MODBUS_ID = "modbus_id"
CONF_ADDRESS = "address"

# Update intervals
CONF_UPDATE_INTERVAL_LIVE = "update_interval_live"
CONF_UPDATE_INTERVAL_STATISTICS = "update_interval_statistics"
CONF_UPDATE_INTERVAL_DEVICE_INFO = "update_interval_device_info"

# =============================================================================
# CONF CONSTANTS - Device Info Group (Extended 0-59)
# =============================================================================
CONF_DEVICE_INFO = "device_info"
CONF_DEVICE_TYPE = "device_type"
CONF_MODBUS_ADDRESS = "modbus_address"

# Device Info Extended (NEW - registers 0-59)
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

# =============================================================================
# CONF CONSTANTS - Sensor Groups (Live Data)
# =============================================================================
# Battery group
CONF_BATTERY = "battery"
CONF_BATTERY_VOLTAGE = "voltage"
CONF_BATTERY_CURRENT = "current"
CONF_BATTERY_POWER = "power"
CONF_BATTERY_SOC = "soc"
CONF_BATTERY_TEMPERATURE = "temperature"
CONF_BATTERY_CAPACITY = "capacity"

# PV string groups
CONF_PV1 = "pv1"
CONF_PV2 = "pv2"
CONF_PV3 = "pv3"
CONF_PV4 = "pv4"

# PV-specific constants (FIXED: for PV_STRING_SCHEMA)
CONF_PV_VOLTAGE = "voltage"
CONF_PV_CURRENT = "current"
CONF_PV_POWER = "power"

# Grid group
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

# Internal/External CT Power
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

# Grid Side Phase Power (NEW)
CONF_GRID_SIDE_A_PHASE_POWER = "grid_side_a_phase_power"
CONF_GRID_SIDE_B_PHASE_POWER = "grid_side_b_phase_power"
CONF_GRID_SIDE_C_PHASE_POWER = "grid_side_c_phase_power"
CONF_GRID_SIDE_TOTAL_POWER = "grid_side_total_power"
CONF_TOTAL_GRID_POWER = "total_grid_power"

# Load Grid Port group (NEW - separate from Load UPS)
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

# Load Grid group
CONF_LOAD_GRID = "load_grid"
CONF_LOAD_GRID_POWER_L1 = "power_l1"
CONF_LOAD_GRID_POWER_L2 = "power_l2"
CONF_LOAD_GRID_POWER_L3 = "power_l3"
CONF_LOAD_GRID_POWER_TOTAL = "power_total"
CONF_LOAD_GRID_VOLTAGE_L1 = "voltage_l1"
CONF_LOAD_GRID_VOLTAGE_L2 = "voltage_l2"
CONF_LOAD_GRID_VOLTAGE_L3 = "voltage_l3"

# Load UPS group
CONF_LOAD_UPS = "load_ups"
CONF_LOAD_UPS_POWER_L1 = "power_l1"
CONF_LOAD_UPS_POWER_L2 = "power_l2"
CONF_LOAD_UPS_POWER_L3 = "power_l3"
CONF_LOAD_UPS_POWER_TOTAL = "power_total"
CONF_LOAD_UPS_VOLTAGE_L1 = "voltage_l1"
CONF_LOAD_UPS_VOLTAGE_L2 = "voltage_l2"
CONF_LOAD_UPS_VOLTAGE_L3 = "voltage_l3"
CONF_LOAD_UPS_FREQUENCY = "frequency"

# Generator group
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

# Generator Port group (NEW - separate from Generator Input)
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

# Temperatures group
CONF_TEMPERATURES = "temperatures"
CONF_TEMP_HEATSINK = "heatsink"
CONF_TEMP_DC_TRANSFORMER = "dc_transformer"

# Inverter group
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

# DC group (additional PV channels)
CONF_DC = "dc"
CONF_DC5_CURRENT = "dc5_current"
CONF_DC6_VOLTAGE = "dc6_voltage"
CONF_DC6_CURRENT = "dc6_current"
CONF_DC7_VOLTAGE = "dc7_voltage"
CONF_DC7_CURRENT = "dc7_current"
CONF_DC8_VOLTAGE = "dc8_voltage"
CONF_DC8_CURRENT = "dc8_current"

# =============================================================================
# CONF CONSTANTS - Battery Modules (NEW - 9 modules with 14 registers each)
# =============================================================================
CONF_BATTERY_MODULES = "battery_modules"

# Battery Module 1 (registers 350-363)
CONF_BATTERY_MODULE_1 = "battery_module_1"
# Battery Module 2 (registers 364-377)
CONF_BATTERY_MODULE_2 = "battery_module_2"
# Battery Module 3 (registers 378-391)
CONF_BATTERY_MODULE_3 = "battery_module_3"
# Battery Module 4 (registers 392-405)
CONF_BATTERY_MODULE_4 = "battery_module_4"
# Battery Module 5 (registers 406-419)
CONF_BATTERY_MODULE_5 = "battery_module_5"
# Battery Module 6 (registers 420-433)
CONF_BATTERY_MODULE_6 = "battery_module_6"
# Battery Module 7 (registers 434-447)
CONF_BATTERY_MODULE_7 = "battery_module_7"
# Battery Module 8 (registers 448-461)
CONF_BATTERY_MODULE_8 = "battery_module_8"
# Battery Module 9 (registers 462-475)
CONF_BATTERY_MODULE_9 = "battery_module_9"

# Battery Module sensor fields
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

# =============================================================================
# CONF CONSTANTS - Statistics Group
# =============================================================================
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

# Missing Statistics Constants (NEW)
CONF_DAILY_ACTIVE_POWER_GENERATION = "daily_active_power_generation"
CONF_ACTIVE_POWER_GENERATION_TODAY = "active_power_generation_today"
CONF_DAILY_GRID_CONNECTION_TIME = "daily_grid_connection_time"
# 32-bit combined sensors (replaces separate low/high pairs)
CONF_TOTAL_ACTIVE_POWER_GENERATION = "total_active_power_generation"
CONF_TOTAL_REACTIVE_POWER_GENERATION = "total_reactive_power_generation"
CONF_TOTAL_BATTERY_CHARGE_32 = "total_battery_charge"
CONF_TOTAL_BATTERY_DISCHARGE_32 = "total_battery_discharge"
CONF_TOTAL_GRID_IMPORT_32 = "total_grid_import"
CONF_TOTAL_GRID_EXPORT_32 = "total_grid_export"
CONF_TOTAL_CONSUMPTION_32 = "total_consumption"
# Legacy separate low/high sensors (deprecated, kept for backward compatibility)
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

# =============================================================================
# CONF CONSTANTS - Status Group
# =============================================================================
CONF_STATUS = "status"
CONF_RUNNING_STATUS = "running_status"
CONF_TURN_OFF_ON_STATUS = "turn_off_on_status"
CONF_AC_INV_RELAY = "ac_inv_relay"
CONF_WARNING_1_RAW = "warning_1_raw"
CONF_WARNING_2_RAW = "warning_2_raw"
CONF_ERROR_1_RAW = "error_1_raw"
CONF_ERROR_2_RAW = "error_2_raw"
CONF_ERROR_3_RAW = "error_3_raw"
CONF_ERROR_4_RAW = "error_4_raw"
CONF_COMMUNICATION_BOARD_FAILURE = "communication_board_failure"

# =============================================================================
# CONF CONSTANTS - Binary Sensor / Switch Groups
# =============================================================================
# Status relays (NEW - for binary_sensor)
CONF_RELAY_STATUS = "relay_status"
CONF_RELAY_INVERTER = "relay_inverter"
CONF_RELAY_LOAD = "relay_load"
CONF_RELAY_GRID = "relay_grid"
CONF_RELAY_GENERATOR = "relay_generator"

# Warnings group
CONF_WARNINGS = "warnings"
CONF_FAN_FAILURE = "fan_failure"
CONF_GRID_PHASE = "grid_phase"
CONF_GRID_PHASE_FAULT = "grid_phase_fault"

# Individual Warning Bits (NEW)
CONF_WARNING_1_BITS = "warning_1_bits"
CONF_WARNING_2_BITS = "warning_2_bits"

# Individual Error Bits (NEW)
CONF_ERROR_1_BITS = "error_1_bits"
CONF_ERROR_2_BITS = "error_2_bits"
CONF_ERROR_3_BITS = "error_3_bits"
CONF_ERROR_4_BITS = "error_4_bits"

# =============================================================================
# CONF CONSTANTS - Settings Groups
# =============================================================================
# Settings Battery group
CONF_SETTINGS_BATTERY = "settings_battery"
CONF_BATTERY_TYPE = "battery_type"
CONF_BATTERY_CONTROL_MODE = "battery_control_mode"
CONF_BATTERY_WAKE_UP = "battery_wake_up"
CONF_BATTERY_RESISTANCE = "battery_resistance"
CONF_BATTERY_CHARGING_EFFICIENCY = "battery_charging_efficiency"
CONF_MAX_CHARGE_CURRENT = "max_charge_current"
CONF_MAX_DISCHARGE_CURRENT = "max_discharge_current"
CONF_BATTERY_LOSS_REPORT_FAULT = "battery_loss_report_fault"

# Settings Battery Voltage group
CONF_SETTINGS_BATTERY_VOLTAGE = "settings_battery_voltage"
CONF_EQUALIZATION_VOLTAGE = "equalization_voltage"
CONF_ABSORPTION_VOLTAGE = "absorption_voltage"
CONF_FLOAT_VOLTAGE = "float_voltage"
CONF_EMPTY_VOLTAGE = "empty_voltage"
CONF_SHUTDOWN_VOLTAGE = "shutdown_voltage"
CONF_RESTART_VOLTAGE = "restart_voltage"
CONF_LOW_VOLTAGE_WARNING = "low_voltage_warning"

# Settings Battery SOC group
CONF_SETTINGS_BATTERY_SOC = "settings_battery_soc"
CONF_SHUTDOWN_SOC = "shutdown_soc"
CONF_RESTART_SOC = "restart_soc"
CONF_LOW_SOC_WARNING = "low_soc_warning"

# Settings Battery Additional
CONF_BATTERY_CAPACITY_AH = "battery_capacity_ah"
CONF_EQUALIZATION_DAY_CYCLE = "equalization_day_cycle"
CONF_EQUALIZATION_TIME = "equalization_time"
CONF_TEMPCO = "tempco"

# Settings Grid group
CONF_SETTINGS_GRID = "settings_grid"
CONF_GRID_CHARGE = "grid_charge"
CONF_SOLAR_SELL = "solar_sell"
CONF_GRID_TYPE = "grid_type"
CONF_GRID_MODE = "grid_mode"
CONF_GRID_NOMINAL_VOLTAGE = "grid_nominal_voltage"
CONF_GRID_NOMINAL_FREQUENCY = "grid_nominal_frequency"
CONF_GRID_PHASE_SEQUENCE = "grid_phase_sequence"
CONF_GRID_CHECK_SOURCE = "grid_check_source"
CONF_MICROINVERTER_EXPORT_TO_GRID = "microinverter_export_to_grid"

# Settings Device group
CONF_SETTINGS_DEVICE = "settings_device"
CONF_EXT_BAUD_RATE = "ext_baud_rate"
CONF_EXT_PARITY = "ext_parity"
CONF_EXT_STOP_BITS = "ext_stop_bits"
CONF_EXT_PROTOCOL = "ext_protocol"
CONF_SOLAR_ARC_FAULT_MODE = "solar_arc_fault_mode"

# Settings Working Mode (NEW)
CONF_SETTINGS_WORKING_MODE = "settings_working_mode"
CONF_WORKING_MODE = "working_mode"
CONF_ENERGY_PRIORITY = "energy_priority"
CONF_LIMIT_CONTROL_MODE = "limit_control_mode"
CONF_FORCED_OFF_GRID_WORK = "forced_off_grid_work"

# Settings Generator group (addresses 121-127)
CONF_SETTINGS_GENERATOR = "settings_generator"
CONF_GEN_MAX_RUN_TIME = "gen_max_run_time"
CONF_GEN_COOLDOWN_TIME = "gen_cooldown_time"
CONF_GEN_MIN_POWER = "gen_min_power"
CONF_GEN_START_VOLTAGE = "gen_start_voltage"
CONF_GEN_START_SOC = "gen_start_soc"
CONF_GEN_CHARGING_CURRENT = "gen_charging_current"
CONF_GEN_ENABLE = "gen_enable"
CONF_EXTERNAL_RELAY = "external_relay"

# Settings Generator 2 group (addresses 223-227)
CONF_SETTINGS_GENERATOR_2 = "settings_generator_2"
CONF_GEN_MAX_TIME = "gen_max_time"
CONF_GEN_COOLDOWN = "gen_cooldown"
CONF_GEN_START_VOLTAGE_225 = "gen_start_voltage_225"
CONF_GEN_START_SOC_226 = "gen_start_soc_226"
CONF_GEN_CHARGE_CURRENT_227 = "gen_charge_current_227"

# Settings Generator Port
CONF_GEN_PORT_CONTROL_MODE = "gen_port_control_mode"
CONF_GEN_PORT_FORCE_ON = "gen_port_force_on"
CONF_GEN_PORT_COUPLE_FREQ_LIMIT = "gen_port_couple_frequency_limit"

# Smart Load
CONF_SETTINGS_SMART_LOAD = "settings_smart_load"
CONF_SMART_LOAD_OFF_VOLTAGE = "smart_load_off_voltage"
CONF_SMART_LOAD_OFF_SOC = "smart_load_off_capacity_soc"
CONF_SMART_LOAD_ON_VOLTAGE = "smart_load_on_voltage"
CONF_SMART_LOAD_ON_SOC = "smart_load_on_capacity_soc"

# Special functions - remaining from Register 178
CONF_GEN_PEAK_SHAVING = "gen_peak_shaving"
CONF_GRID_PEAK_SHAVING = "grid_peak_shaving"
CONF_ON_GRID_ALWAYS_ON = "on_grid_always_on"

# Special functions - Register 179
CONF_EXTERNAL_CT_DIRECTION_CHECK = "external_ct_direction_check"

# Other special function registers
CONF_RESTORE_CONNECTION_TIME = "restore_connection_time"

# Grid charge settings
CONF_SETTINGS_GRID_CHARGE = "settings_grid_charge"
CONF_MAXIMUM_BATTERY_GRID_CHARGE_CURRENT = "maximum_battery_grid_charge_current"
CONF_GENERATOR_CHARGING_ENABLED = "generator_charging_enabled"
CONF_GRID_CHARGE_START_VOLTAGE = "grid_charge_start_voltage"
CONF_GRID_CHARGE_START_SOC = "grid_charge_start_soc"
CONF_GRID_CHARGE_CURRENT = "grid_charge_current"

# Generator required power
CONF_GENERATOR_REQUIRED_POWER_START = "generator_required_power_start"

# Settings Grid Numbers (distributed from settings_special)
CONF_ZERO_EXPORT_POWER = "zero_export_power"
CONF_MAX_SOLAR_SELL_POWER = "max_solar_sell_power"
CONF_GRID_MAX_POWER = "grid_max_power"
CONF_RESTORE_CONNECTION_TIME = "restore_connection_time"

# =============================================================================
# CONF CONSTANTS - Settings System (NEW - registers 60-97)
# =============================================================================
CONF_SETTINGS_SYSTEM = "settings_system"
CONF_SYS_LANGUAGE = "sys_language"
CONF_SYS_BEEPER = "sys_beeper"
CONF_SYS_LCD_BACKLIGHT = "sys_lcd_backlight"
CONF_SYS_LCD_CONTRAST = "sys_lcd_contrast"
CONF_SYS_DATE_TIME = "sys_date_time"
CONF_SYS_TIME_ZONE = "sys_time_zone"
CONF_SYS_DST_ENABLE = "sys_dst_enable"
CONF_SYS_PASSWORD = "sys_password"
CONF_SYS_DATA_LOG_INTERVAL = "sys_data_log_interval"
CONF_SYS_REMOTE_LOCK = "sys_remote_lock"
CONF_SYS_FACTORY_RESET = "sys_factory_reset"
CONF_SYS_SOFTWARE_RESET = "sys_software_reset"

# =============================================================================
# CONF CONSTANTS - Settings Grid Protection (NEW - registers 185-200)
# =============================================================================
CONF_SETTINGS_GRID_PROTECTION = "settings_grid_protection"
CONF_GP_OVER_VOLTAGE_PROTECTION = "gp_over_voltage_protection"
CONF_GP_UNDER_VOLTAGE_PROTECTION = "gp_under_voltage_protection"
CONF_GP_OVER_FREQUENCY_PROTECTION = "gp_over_frequency_protection"
CONF_GP_UNDER_FREQUENCY_PROTECTION = "gp_under_frequency_protection"
CONF_GP_VOLTAGE_RECONNECT = "gp_voltage_reconnect"
CONF_GP_FREQUENCY_RECONNECT = "gp_frequency_reconnect"
CONF_GP_RECONNECT_TIME = "gp_reconnect_time"
CONF_GP_RAMP_RATE = "gp_ramp_rate"
CONF_GP_STARTUP_TIME = "gp_startup_time"

# =============================================================================
# CONF CONSTANTS - Settings Extended (NEW - registers 231-339)
# =============================================================================
CONF_SETTINGS_EXTENDED = "settings_extended"
CONF_EXT_COMMUNICATION_ADDRESS = "ext_communication_address"
CONF_EXT_MODBUS_TCP_ENABLE = "ext_modbus_tcp_enable"
CONF_EXT_MQTT_ENABLE = "ext_mqtt_enable"
CONF_EXT_CLOUD_ENABLE = "ext_cloud_enable"
CONF_EXT_SNMP_ENABLE = "ext_snmp_enable"
CONF_EXT_SYSLOG_ENABLE = "ext_syslog_enable"
CONF_EXT_REMOTE_MONITOR = "ext_remote_monitor"
CONF_EXT_FIRMWARE_UPDATE = "ext_firmware_update"

# =============================================================================
# CONF CONSTANTS - Settings California (NEW - registers 340-499)
# =============================================================================
CONF_SETTINGS_CALIFORNIA = "settings_california"
CONF_CA_RULE21_ENABLE = "ca_rule21_enable"
CONF_CA_RULE21_CATEGORY = "ca_rule21_category"
CONF_CA_VOLT_WATT_ENABLE = "ca_volt_watt_enable"
CONF_CA_VOLT_WATT_CURVE = "ca_volt_watt_curve"
CONF_CA_VOLT_VAR_ENABLE = "ca_volt_var_enable"
CONF_CA_VOLT_VAR_CURVE = "ca_volt_var_curve"
CONF_CA_WATT_VAR_ENABLE = "ca_watt_var_enable"
CONF_CA_WATT_VAR_CURVE = "ca_watt_var_curve"
CONF_CA_FREQ_WATT_ENABLE = "ca_freq_watt_enable"
CONF_CA_FREQ_WATT_CURVE = "ca_freq_watt_curve"
CONF_CA_RAMP_RATE = "ca_ramp_rate"
CONF_CA_RECONNECT_TIME = "ca_reconnect_time"
CONF_CA_NORMAL_OP_CAT = "ca_normal_op_cat"
CONF_CA_ABNORMAL_OP_CAT = "ca_abnormal_op_cat"

# California Voltage Points
CONF_CA_VOLTAGE_POINT_1 = "ca_voltage_point_1"
CONF_CA_VOLTAGE_POINT_2 = "ca_voltage_point_2"
CONF_CA_VOLTAGE_POINT_3 = "ca_voltage_point_3"
CONF_CA_VOLTAGE_POINT_4 = "ca_voltage_point_4"
CONF_CA_VOLTAGE_POINT_5 = "ca_voltage_point_5"
CONF_CA_VOLTAGE_POINT_6 = "ca_voltage_point_6"

# California Power Points
CONF_CA_POWER_POINT_1 = "ca_power_point_1"
CONF_CA_POWER_POINT_2 = "ca_power_point_2"
CONF_CA_POWER_POINT_3 = "ca_power_point_3"
CONF_CA_POWER_POINT_4 = "ca_power_point_4"
CONF_CA_POWER_POINT_5 = "ca_power_point_5"
CONF_CA_POWER_POINT_6 = "ca_power_point_6"

# =============================================================================
# CONF CONSTANTS - Settings Time of Use Group
# =============================================================================
CONF_SETTINGS_TIME_OF_USE = "settings_time_of_use"
CONF_TIME_OF_USE = "time_of_use"

# Time Points (1-6)
CONF_TIME_POINT_1 = "time_point_1"
CONF_TIME_POINT_2 = "time_point_2"
CONF_TIME_POINT_3 = "time_point_3"
CONF_TIME_POINT_4 = "time_point_4"
CONF_TIME_POINT_5 = "time_point_5"
CONF_TIME_POINT_6 = "time_point_6"

# Time Point fields
CONF_START = "start"
CONF_POWER = "power"
CONF_MIN_BATTERY_VOLTAGE = "min_battery_voltage"
CONF_CAPACITY = "capacity"
CONF_CHARGE_ENABLE = "charge_enable"

# Time Point detailed CONF constants (addresses 148-177)
# Time Point Start times (addresses 148-153)
CONF_TIME_POINT_1_START = "time_point_1_start"
CONF_TIME_POINT_2_START = "time_point_2_start"
CONF_TIME_POINT_3_START = "time_point_3_start"
CONF_TIME_POINT_4_START = "time_point_4_start"
CONF_TIME_POINT_5_START = "time_point_5_start"
CONF_TIME_POINT_6_START = "time_point_6_start"

# Time Point Power values (addresses 154-159)
CONF_TIME_POINT_1_POWER = "time_point_1_power"
CONF_TIME_POINT_2_POWER = "time_point_2_power"
CONF_TIME_POINT_3_POWER = "time_point_3_power"
CONF_TIME_POINT_4_POWER = "time_point_4_power"
CONF_TIME_POINT_5_POWER = "time_point_5_power"
CONF_TIME_POINT_6_POWER = "time_point_6_power"

# Time Point Min Battery Voltage (addresses 160-165)
CONF_TIME_POINT_1_MIN_BATTERY_VOLTAGE = "time_point_1_min_battery_voltage"
CONF_TIME_POINT_2_MIN_BATTERY_VOLTAGE = "time_point_2_min_battery_voltage"
CONF_TIME_POINT_3_MIN_BATTERY_VOLTAGE = "time_point_3_min_battery_voltage"
CONF_TIME_POINT_4_MIN_BATTERY_VOLTAGE = "time_point_4_min_battery_voltage"
CONF_TIME_POINT_5_MIN_BATTERY_VOLTAGE = "time_point_5_min_battery_voltage"
CONF_TIME_POINT_6_MIN_BATTERY_VOLTAGE = "time_point_6_min_battery_voltage"

# Time Point Capacity (addresses 166-171)
CONF_TIME_POINT_1_CAPACITY = "time_point_1_capacity"
CONF_TIME_POINT_2_CAPACITY = "time_point_2_capacity"
CONF_TIME_POINT_3_CAPACITY = "time_point_3_capacity"
CONF_TIME_POINT_4_CAPACITY = "time_point_4_capacity"
CONF_TIME_POINT_5_CAPACITY = "time_point_5_capacity"
CONF_TIME_POINT_6_CAPACITY = "time_point_6_capacity"

# Time Point Charge Enable (addresses 172-177, Bit 0)
CONF_TIME_POINT_1_CHARGE_ENABLE = "time_point_1_charge_enable"
CONF_TIME_POINT_2_CHARGE_ENABLE = "time_point_2_charge_enable"
CONF_TIME_POINT_3_CHARGE_ENABLE = "time_point_3_charge_enable"
CONF_TIME_POINT_4_CHARGE_ENABLE = "time_point_4_charge_enable"
CONF_TIME_POINT_5_CHARGE_ENABLE = "time_point_5_charge_enable"
CONF_TIME_POINT_6_CHARGE_ENABLE = "time_point_6_charge_enable"

# Time Point Grid Charge Enable (addresses 172-177, Bit 1)
CONF_TIME_POINT_1_GRID_CHARGE_ENABLE = "time_point_1_grid_charge_enable"
CONF_TIME_POINT_2_GRID_CHARGE_ENABLE = "time_point_2_grid_charge_enable"
CONF_TIME_POINT_3_GRID_CHARGE_ENABLE = "time_point_3_grid_charge_enable"
CONF_TIME_POINT_4_GRID_CHARGE_ENABLE = "time_point_4_grid_charge_enable"
CONF_TIME_POINT_5_GRID_CHARGE_ENABLE = "time_point_5_grid_charge_enable"
CONF_TIME_POINT_6_GRID_CHARGE_ENABLE = "time_point_6_grid_charge_enable"

# Time Point Generator Charge Enable (addresses 172-177, Bit 2)
CONF_TIME_POINT_1_GEN_CHARGE_ENABLE = "time_point_1_gen_charge_enable"
CONF_TIME_POINT_2_GEN_CHARGE_ENABLE = "time_point_2_gen_charge_enable"
CONF_TIME_POINT_3_GEN_CHARGE_ENABLE = "time_point_3_gen_charge_enable"
CONF_TIME_POINT_4_GEN_CHARGE_ENABLE = "time_point_4_gen_charge_enable"
CONF_TIME_POINT_5_GEN_CHARGE_ENABLE = "time_point_5_gen_charge_enable"
CONF_TIME_POINT_6_GEN_CHARGE_ENABLE = "time_point_6_gen_charge_enable"

# Weekday Enables (Register 146, Bits 1-7)
CONF_WEEKDAY_MONDAY = "weekday_monday"
CONF_WEEKDAY_TUESDAY = "weekday_tuesday"
CONF_WEEKDAY_WEDNESDAY = "weekday_wednesday"
CONF_WEEKDAY_THURSDAY = "weekday_thursday"
CONF_WEEKDAY_FRIDAY = "weekday_friday"
CONF_WEEKDAY_SATURDAY = "weekday_saturday"
CONF_WEEKDAY_SUNDAY = "weekday_sunday"

# =============================================================================
# NAMESPACE
# =============================================================================
deye_inverter_ns = cg.esphome_ns.namespace("deye_inverter")
DeyeInverter = deye_inverter_ns.class_(
    "DeyeInverter", cg.PollingComponent, cg.Parented.template(ModbusController)
)

# =============================================================================
# BASE ENTITY SCHEMAS
# =============================================================================
ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_NAME): cv.string,
        cv.Required(CONF_ID): cv.declare_id(sensor.Sensor),
        cv.Optional(CONF_DISABLED_BY_DEFAULT, default=False): cv.boolean,
    }
)

BINARY_ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_NAME): cv.string,
        cv.Required(CONF_ID): cv.declare_id(binary_sensor.BinarySensor),
        cv.Optional(CONF_DISABLED_BY_DEFAULT, default=False): cv.boolean,
    }
)

TEXT_ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_NAME): cv.string,
        cv.Required(CONF_ID): cv.declare_id(text_sensor.TextSensor),
        cv.Optional(CONF_DISABLED_BY_DEFAULT, default=False): cv.boolean,
    }
)

SWITCH_ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_NAME): cv.string,
        cv.Required(CONF_ID): cv.declare_id(switch.Switch),
        cv.Optional(CONF_DISABLED_BY_DEFAULT, default=False): cv.boolean,
    }
)

SELECT_ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_NAME): cv.string,
        cv.Required(CONF_ID): cv.declare_id(select.Select),
        cv.Optional(CONF_DISABLED_BY_DEFAULT, default=False): cv.boolean,
    }
)

NUMBER_ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_NAME): cv.string,
        cv.Required(CONF_ID): cv.declare_id(number.Number),
        cv.Optional(CONF_DISABLED_BY_DEFAULT, default=False): cv.boolean,
    }
)

# =============================================================================
# DEVICE INFO SCHEMA
# =============================================================================
DEVICE_INFO_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_DEVICE_TYPE): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_MODBUS_ADDRESS): ENTITY_SCHEMA,
    }
)

# Device Info Extended Schema (NEW)
DEVICE_INFO_EXTENDED_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SERIAL_NUMBER): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_FIRMWARE_VERSION): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_HARDWARE_VERSION): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_DEVICE_TYPE_CODE): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_MODEL): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_POWER_RATING): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_VOLTAGE_RATING): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_CURRENT_RATING): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_FREQUENCY_RATING): ENTITY_SCHEMA,
    }
)

# =============================================================================
# SENSOR GROUP SCHEMAS - Live Data
# =============================================================================

# PV String Schema (reusable for pv1, pv2, pv3, pv4) - FIXED: Uses PV-specific constants
PV_STRING_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_PV_VOLTAGE): ENTITY_SCHEMA,
        cv.Optional(CONF_PV_CURRENT): ENTITY_SCHEMA,
        cv.Optional(CONF_PV_POWER): ENTITY_SCHEMA,
    }
)

# Battery Schema
BATTERY_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_VOLTAGE): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_CURRENT): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_SOC): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_TEMPERATURE): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_CAPACITY): ENTITY_SCHEMA,
    }
)

# Battery Module Schema (NEW - for 9 battery modules)
BATTERY_MODULE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BM_VOLTAGE): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_CURRENT): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_SOC): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_TEMPERATURE): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_STATUS): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_FAULT_CODE): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_CYCLE_COUNT): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_CAPACITY_REMAINING): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_CAPACITY_TOTAL): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_CELL_MAX_VOLTAGE): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_CELL_MIN_VOLTAGE): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_CELL_MAX_TEMP): ENTITY_SCHEMA,
        cv.Optional(CONF_BM_CELL_MIN_TEMP): ENTITY_SCHEMA,
    }
)

# Grid Schema
GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GRID_VOLTAGE_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_VOLTAGE_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_VOLTAGE_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_VOLTAGE_L1_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_VOLTAGE_L2_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_VOLTAGE_L3_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_POWER_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_POWER_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_POWER_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_POWER_TOTAL): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_FREQUENCY): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_CURRENT_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_CURRENT_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_CURRENT_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_INTERNAL_CT_L1_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_INTERNAL_CT_L2_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_INTERNAL_CT_L3_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_INTERNAL_TOTAL_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_EXTERNAL_CT_L1_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_EXTERNAL_CT_L2_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_EXTERNAL_CT_L3_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_OUT_OF_GRID_TOTAL_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_METER_APPARENT_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_METER_POWER_FACTOR): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_METER_CURRENT_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_METER_CURRENT_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_METER_CURRENT_L3): ENTITY_SCHEMA,
        # NEW Grid Side sensors
        cv.Optional(CONF_GRID_SIDE_A_PHASE_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_SIDE_B_PHASE_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_SIDE_C_PHASE_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_SIDE_TOTAL_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_GRID_POWER): ENTITY_SCHEMA,
    }
)

# Load Grid Schema
LOAD_GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_GRID_POWER_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_GRID_POWER_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_GRID_POWER_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_GRID_POWER_TOTAL): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_GRID_VOLTAGE_L3): ENTITY_SCHEMA,
    }
)

# Load Grid Port Schema (NEW)
LOAD_GRID_PORT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_PORT_VOLTAGE_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_PORT_CURRENT_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_PORT_CURRENT_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_PORT_CURRENT_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_PORT_POWER_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_PORT_POWER_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_PORT_POWER_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_REAL_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_APPARENT_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_FREQUENCY): ENTITY_SCHEMA,
    }
)

# Load UPS Schema
LOAD_UPS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_LOAD_UPS_POWER_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_UPS_POWER_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_UPS_POWER_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_UPS_POWER_TOTAL): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_UPS_VOLTAGE_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_LOAD_UPS_FREQUENCY): ENTITY_SCHEMA,
    }
)

# Generator Schema
GENERATOR_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GENERATOR_VOLTAGE_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_VOLTAGE_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_VOLTAGE_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_POWER_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_POWER_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_POWER_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_POWER_TOTAL): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_CURRENT_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_CURRENT_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_CURRENT_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GENERATOR_FREQUENCY): ENTITY_SCHEMA,
    }
)

# Generator Port Schema (NEW)
GENERATOR_PORT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_VOLTAGE_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_POWER_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_POWER_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_POWER_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_POWER_TOTAL): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_CURRENT_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_CURRENT_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_CURRENT_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PORT_FREQUENCY): ENTITY_SCHEMA,
    }
)

# Temperatures Schema
TEMPERATURES_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_TEMP_HEATSINK): ENTITY_SCHEMA,
        cv.Optional(CONF_TEMP_DC_TRANSFORMER): ENTITY_SCHEMA,
    }
)

# Inverter Schema
INVERTER_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_INVERTER_VOLTAGE_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_VOLTAGE_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_VOLTAGE_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_REAL_POWER_L1): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_REAL_POWER_L2): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_REAL_POWER_L3): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_REAL_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_APPARENT_POWER): ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_FREQUENCY): ENTITY_SCHEMA,
    }
)

# DC Schema (additional channels)
DC_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_DC5_CURRENT): ENTITY_SCHEMA,
        cv.Optional(CONF_DC6_VOLTAGE): ENTITY_SCHEMA,
        cv.Optional(CONF_DC6_CURRENT): ENTITY_SCHEMA,
        cv.Optional(CONF_DC7_VOLTAGE): ENTITY_SCHEMA,
        cv.Optional(CONF_DC7_CURRENT): ENTITY_SCHEMA,
        cv.Optional(CONF_DC8_VOLTAGE): ENTITY_SCHEMA,
        cv.Optional(CONF_DC8_CURRENT): ENTITY_SCHEMA,
    }
)

# =============================================================================
# STATISTICS SCHEMAS
# =============================================================================
DAILY_STATISTICS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_PRODUCTION): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_CHARGE): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_DISCHARGE): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_IMPORT): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_EXPORT): ENTITY_SCHEMA,
        cv.Optional(CONF_CONSUMPTION): ENTITY_SCHEMA,
        cv.Optional(CONF_PV_PRODUCTION): ENTITY_SCHEMA,
        cv.Optional(CONF_DAILY_PV1_PRODUCTION): ENTITY_SCHEMA,
        cv.Optional(CONF_DAILY_PV2_PRODUCTION): ENTITY_SCHEMA,
        cv.Optional(CONF_DAILY_PV3_PRODUCTION): ENTITY_SCHEMA,
        cv.Optional(CONF_DAILY_PV4_PRODUCTION): ENTITY_SCHEMA,
        cv.Optional(CONF_DAILY_GENERATOR_ON_TIME): ENTITY_SCHEMA,
        # NEW daily statistics
        cv.Optional(CONF_DAILY_ACTIVE_POWER_GENERATION): ENTITY_SCHEMA,
        cv.Optional(CONF_ACTIVE_POWER_GENERATION_TODAY): ENTITY_SCHEMA,
        cv.Optional(CONF_DAILY_GRID_CONNECTION_TIME): ENTITY_SCHEMA,
    }
)

TOTAL_STATISTICS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_PRODUCTION): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_CHARGE): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_DISCHARGE): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_IMPORT): ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_EXPORT): ENTITY_SCHEMA,
        cv.Optional(CONF_CONSUMPTION): ENTITY_SCHEMA,
        cv.Optional(CONF_PV_PRODUCTION): ENTITY_SCHEMA,
        # NEW 32-bit combined sensors (replaces separate low/high pairs)
        cv.Optional(CONF_TOTAL_ACTIVE_POWER_GENERATION): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_REACTIVE_POWER_GENERATION): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_BATTERY_CHARGE_32): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_BATTERY_DISCHARGE_32): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_GRID_IMPORT_32): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_GRID_EXPORT_32): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_CONSUMPTION_32): ENTITY_SCHEMA,
        # Legacy separate low/high sensors (deprecated, kept for backward compatibility)
        cv.Optional(CONF_ACTIVE_POWER_GEN_TOTAL_LOW): ENTITY_SCHEMA,
        cv.Optional(CONF_ACTIVE_POWER_GEN_TOTAL_HIGH): ENTITY_SCHEMA,
        cv.Optional(CONF_REACTIVE_POWER_GEN_TOTAL_LOW): ENTITY_SCHEMA,
        cv.Optional(CONF_REACTIVE_POWER_GEN_TOTAL_HIGH): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_PV_PRODUCTION): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_CHARGE_TOTAL_HIGH): ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_DISCHARGE_TOTAL_HIGH): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_GRID_BUY_HIGH): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_GRID_SELL_HIGH): ENTITY_SCHEMA,
        cv.Optional(CONF_TOTAL_LOAD_HIGH): ENTITY_SCHEMA,
    }
)

STATISTICS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_DAILY): DAILY_STATISTICS_SCHEMA,
        cv.Optional(CONF_TOTAL): TOTAL_STATISTICS_SCHEMA,
    }
)

# =============================================================================
# STATUS SCHEMAS
# =============================================================================
STATUS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_RUNNING_STATUS): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_TURN_OFF_ON_STATUS): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_AC_INV_RELAY): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_WARNING_1_RAW): ENTITY_SCHEMA,
        cv.Optional(CONF_WARNING_2_RAW): ENTITY_SCHEMA,
        cv.Optional(CONF_ERROR_1_RAW): ENTITY_SCHEMA,
        cv.Optional(CONF_ERROR_2_RAW): ENTITY_SCHEMA,
        cv.Optional(CONF_ERROR_3_RAW): ENTITY_SCHEMA,
        cv.Optional(CONF_ERROR_4_RAW): ENTITY_SCHEMA,
        cv.Optional(CONF_COMMUNICATION_BOARD_FAILURE): ENTITY_SCHEMA,
    }
)

# =============================================================================
# MAIN SENSOR SCHEMA
# =============================================================================
SENSOR_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(DeyeInverter),
        cv.Optional(CONF_DEVICE_ID): cv.use_id(cg.EntityBase),
        cv.Required(CONF_MODBUS_ID): cv.use_id(ModbusController),
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
        # NEW: Battery Modules
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
# TEXT SENSOR SCHEMA
# =============================================================================
TEXT_SENSOR_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_DEVICE_ID): cv.use_id(cg.EntityBase),
        cv.Optional(CONF_DEVICE_TYPE): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_RUNNING_STATUS): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_SERIAL_NUMBER): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_FIRMWARE_VERSION): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_HARDWARE_VERSION): TEXT_ENTITY_SCHEMA,
        cv.Optional(CONF_INVERTER_MODEL): TEXT_ENTITY_SCHEMA,
    }
)

# =============================================================================
# BINARY SENSOR SCHEMA
# =============================================================================
# Status group schema
RELAY_STATUS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_RELAY_INVERTER): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_RELAY_LOAD): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_RELAY_GRID): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_RELAY_GENERATOR): BINARY_ENTITY_SCHEMA,
    }
)

# Warnings group schema
WARNINGS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_FAN_FAILURE): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_PHASE): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_PHASE_FAULT): BINARY_ENTITY_SCHEMA,
    }
)

# Warning bits schema (NEW)
WARNING_BITS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_WARNING_1_BITS): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_WARNING_2_BITS): BINARY_ENTITY_SCHEMA,
    }
)

# Error bits schema (NEW)
ERROR_BITS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_ERROR_1_BITS): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_ERROR_2_BITS): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_ERROR_3_BITS): BINARY_ENTITY_SCHEMA,
        cv.Optional(CONF_ERROR_4_BITS): BINARY_ENTITY_SCHEMA,
    }
)

BINARY_SENSOR_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_DEVICE_ID): cv.use_id(cg.EntityBase),
        cv.Optional(CONF_RELAY_STATUS): RELAY_STATUS_SCHEMA,
        cv.Optional(CONF_WARNINGS): WARNINGS_SCHEMA,
        cv.Optional(CONF_WARNING_1_BITS): WARNING_BITS_SCHEMA,
        cv.Optional(CONF_WARNING_2_BITS): WARNING_BITS_SCHEMA,
        cv.Optional(CONF_ERROR_1_BITS): ERROR_BITS_SCHEMA,
        cv.Optional(CONF_ERROR_2_BITS): ERROR_BITS_SCHEMA,
        cv.Optional(CONF_ERROR_3_BITS): ERROR_BITS_SCHEMA,
        cv.Optional(CONF_ERROR_4_BITS): ERROR_BITS_SCHEMA,
    }
)

# =============================================================================
# SWITCH SCHEMA
# =============================================================================
# Settings Grid schema
SETTINGS_GRID_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GRID_CHARGE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_SOLAR_SELL): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_PEAK_SHAVING): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_PEAK_SHAVING): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_ON_GRID_ALWAYS_ON): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_MICROINVERTER_EXPORT_TO_GRID): SWITCH_ENTITY_SCHEMA,
    }
)

# Settings System schema (NEW)
SETTINGS_SYSTEM_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SYS_BEEPER): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_SYS_LCD_BACKLIGHT): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_SYS_DST_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_SYS_REMOTE_LOCK): SWITCH_ENTITY_SCHEMA,
    }
)

# Time Point schema (switches)
TIME_POINT_SWITCH_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
    }
)

# Settings Time of Use schema
SETTINGS_TIME_OF_USE_SWITCH_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_TIME_OF_USE): SWITCH_ENTITY_SCHEMA,
        # Solar/General Charge Enable (Bit 0)
        cv.Optional(CONF_TIME_POINT_1_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_2_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_3_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_4_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_5_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_6_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        # Grid Charge Enable (Bit 1)
        cv.Optional(CONF_TIME_POINT_1_GRID_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_2_GRID_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_3_GRID_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_4_GRID_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_5_GRID_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_6_GRID_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        # Generator Charge Enable (Bit 2)
        cv.Optional(CONF_TIME_POINT_1_GEN_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_2_GEN_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_3_GEN_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_4_GEN_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_5_GEN_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_6_GEN_CHARGE_ENABLE): SWITCH_ENTITY_SCHEMA,
        # Weekday Enables (Register 146, Bits 1-7)
        cv.Optional(CONF_WEEKDAY_MONDAY): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_WEEKDAY_TUESDAY): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_WEEKDAY_WEDNESDAY): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_WEEKDAY_THURSDAY): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_WEEKDAY_FRIDAY): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_WEEKDAY_SATURDAY): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_WEEKDAY_SUNDAY): SWITCH_ENTITY_SCHEMA,
    }
)

# Settings Device schema (switches)
SETTINGS_DEVICE_SWITCH_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EXTERNAL_CT_DIRECTION_CHECK): SWITCH_ENTITY_SCHEMA,
        cv.Optional(CONF_SOLAR_ARC_FAULT_MODE): SWITCH_ENTITY_SCHEMA,
    }
)

# Settings Working Mode schema (switches)
SETTINGS_WORKING_MODE_SWITCH_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_FORCED_OFF_GRID_WORK): SWITCH_ENTITY_SCHEMA,
    }
)

# Settings Battery schema (switches)
SETTINGS_BATTERY_SWITCH_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_LOSS_REPORT_FAULT): SWITCH_ENTITY_SCHEMA,
    }
)

# Settings Generator schema (switches)
SETTINGS_GENERATOR_SWITCH_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EXTERNAL_RELAY): SWITCH_ENTITY_SCHEMA,
    }
)

SWITCH_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_DEVICE_ID): cv.use_id(cg.EntityBase),
        cv.Optional(CONF_SETTINGS_GRID): SETTINGS_GRID_SCHEMA,
        cv.Optional(CONF_SETTINGS_DEVICE): SETTINGS_DEVICE_SWITCH_SCHEMA,
        cv.Optional(CONF_SETTINGS_SYSTEM): SETTINGS_SYSTEM_SCHEMA,
        cv.Optional(CONF_SETTINGS_TIME_OF_USE): SETTINGS_TIME_OF_USE_SWITCH_SCHEMA,
        cv.Optional(CONF_SETTINGS_WORKING_MODE): SETTINGS_WORKING_MODE_SWITCH_SCHEMA,
        cv.Optional(CONF_SETTINGS_BATTERY): SETTINGS_BATTERY_SWITCH_SCHEMA,
        cv.Optional(CONF_SETTINGS_GENERATOR): SETTINGS_GENERATOR_SWITCH_SCHEMA,
    }
)

# =============================================================================
# SELECT SCHEMA
# =============================================================================
# Settings Grid schema (select)
SETTINGS_GRID_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GRID_TYPE): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_MODE): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_NOMINAL_VOLTAGE): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_NOMINAL_FREQUENCY): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_PHASE_SEQUENCE): SELECT_ENTITY_SCHEMA,
    }
)

# Settings Device schema (select)
SETTINGS_DEVICE_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EXT_BAUD_RATE): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_EXT_PARITY): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_EXT_STOP_BITS): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_EXT_PROTOCOL): SELECT_ENTITY_SCHEMA,
    }
)

# Settings Battery schema (select part)
SETTINGS_BATTERY_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_TYPE): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_CONTROL_MODE): SELECT_ENTITY_SCHEMA,
    }
)

# Generator Port Control Mode
CONF_SETTINGS_GEN_PORT = "settings_gen_port"

# Settings Working Mode
CONF_SETTINGS_WORKING_MODE = "settings_working_mode"

# Settings System Select - use CONF_SETTINGS_SYSTEM already defined
# Settings California - renamed from _SELECT suffix
CONF_SETTINGS_CALIFORNIA = "settings_california"

SETTINGS_GEN_PORT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_PORT_CONTROL_MODE): SELECT_ENTITY_SCHEMA,
    }
)

# Settings Working Mode (includes energy_priority and limit_control_mode)
SETTINGS_WORKING_MODE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_WORKING_MODE): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_ENERGY_PRIORITY): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_LIMIT_CONTROL_MODE): SELECT_ENTITY_SCHEMA,
    }
)

# Settings System Select - use existing CONF_SETTINGS_SYSTEM
SETTINGS_SYSTEM_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SYS_LANGUAGE): SELECT_ENTITY_SCHEMA,
    }
)

# Settings California Select (NEW)
SETTINGS_CALIFORNIA_SELECT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_CA_RULE21_CATEGORY): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_NORMAL_OP_CAT): SELECT_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_ABNORMAL_OP_CAT): SELECT_ENTITY_SCHEMA,
    }
)

SELECT_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_DEVICE_ID): cv.use_id(cg.EntityBase),
        cv.Optional(CONF_SETTINGS_GRID): SETTINGS_GRID_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_DEVICE): SETTINGS_DEVICE_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_BATTERY): SETTINGS_BATTERY_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_GEN_PORT): SETTINGS_GEN_PORT_SCHEMA,
        cv.Optional(CONF_SETTINGS_WORKING_MODE): SETTINGS_WORKING_MODE_SCHEMA,
        cv.Optional(CONF_SETTINGS_SYSTEM): SETTINGS_SYSTEM_SELECT_SCHEMA,
        cv.Optional(CONF_SETTINGS_CALIFORNIA): SETTINGS_CALIFORNIA_SELECT_SCHEMA,
    }
)

# =============================================================================
# NUMBER SCHEMA
# =============================================================================
# Settings Battery (currents) schema
SETTINGS_BATTERY_CURRENT_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_MAX_CHARGE_CURRENT): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_MAX_DISCHARGE_CURRENT): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings Battery Voltage schema
SETTINGS_BATTERY_VOLTAGE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_EQUALIZATION_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_ABSORPTION_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_FLOAT_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_EMPTY_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_SHUTDOWN_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_RESTART_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_LOW_VOLTAGE_WARNING): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings Battery SOC schema
SETTINGS_BATTERY_SOC_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SHUTDOWN_SOC): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_RESTART_SOC): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_LOW_SOC_WARNING): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings Battery Additional
CONF_SETTINGS_BATTERY_ADDITIONAL = "settings_battery_additional"

SETTINGS_BATTERY_ADDITIONAL_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_BATTERY_CAPACITY_AH): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_EQUALIZATION_DAY_CYCLE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_EQUALIZATION_TIME): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TEMPCO): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_WAKE_UP): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_RESISTANCE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_BATTERY_CHARGING_EFFICIENCY): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings Generator schema (addresses 121-127)
SETTINGS_GENERATOR_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_MAX_RUN_TIME): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_COOLDOWN_TIME): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_MIN_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_START_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_START_SOC): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_CHARGING_CURRENT): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_ENABLE): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings Generator 2 schema (addresses 223-227)
SETTINGS_GENERATOR_2_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GEN_MAX_TIME): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_COOLDOWN): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_START_VOLTAGE_225): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_START_SOC_226): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GEN_CHARGE_CURRENT_227): NUMBER_ENTITY_SCHEMA,
    }
)

# Smart Load schema
SETTINGS_SMART_LOAD_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SMART_LOAD_OFF_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_SMART_LOAD_OFF_SOC): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_SMART_LOAD_ON_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_SMART_LOAD_ON_SOC): NUMBER_ENTITY_SCHEMA,
    }
)

# Grid charge settings schema
SETTINGS_GRID_CHARGE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_MAXIMUM_BATTERY_GRID_CHARGE_CURRENT): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_CHARGE_START_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_CHARGE_START_SOC): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_CHARGE_CURRENT): NUMBER_ENTITY_SCHEMA,
    }
)

# Time Point schema (numbers)
TIME_POINT_NUMBER_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_START): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_MIN_BATTERY_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CAPACITY): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings Time of Use (numbers) - addresses 148-171
CONF_SETTINGS_TIME_OF_USE_NUMBERS = "settings_time_of_use_numbers"

SETTINGS_TIME_OF_USE_NUMBERS_SCHEMA = cv.Schema(
    {
        # Time Point Start times moved to SETTINGS_TIME_OF_USE_DATETIME_SCHEMA
        # Time Point Power values (addresses 154-159)
        cv.Optional(CONF_TIME_POINT_1_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_2_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_3_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_4_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_5_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_6_POWER): NUMBER_ENTITY_SCHEMA,
        # Time Point Min Battery Voltage (addresses 160-165)
        cv.Optional(CONF_TIME_POINT_1_MIN_BATTERY_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_2_MIN_BATTERY_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_3_MIN_BATTERY_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_4_MIN_BATTERY_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_5_MIN_BATTERY_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_6_MIN_BATTERY_VOLTAGE): NUMBER_ENTITY_SCHEMA,
        # Time Point Capacity (addresses 166-171)
        cv.Optional(CONF_TIME_POINT_1_CAPACITY): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_2_CAPACITY): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_3_CAPACITY): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_4_CAPACITY): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_5_CAPACITY): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_6_CAPACITY): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings Grid Numbers (distributed from settings_special)
CONF_SETTINGS_GRID_NUMBERS = "settings_grid"

SETTINGS_GRID_NUMBERS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_ZERO_EXPORT_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_MAX_SOLAR_SELL_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GRID_MAX_POWER): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_RESTORE_CONNECTION_TIME): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings System Numbers (NEW - registers 60-97)
CONF_SETTINGS_SYSTEM_NUMBERS = "settings_system_numbers"

SETTINGS_SYSTEM_NUMBERS_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_SYS_LCD_CONTRAST): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_SYS_TIME_ZONE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_SYS_DATA_LOG_INTERVAL): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings Grid Protection Numbers (NEW - registers 185-200)
CONF_SETTINGS_GRID_PROTECTION = "settings_grid_protection"

SETTINGS_GRID_PROTECTION_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_GP_OVER_VOLTAGE_PROTECTION): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GP_UNDER_VOLTAGE_PROTECTION): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GP_OVER_FREQUENCY_PROTECTION): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GP_UNDER_FREQUENCY_PROTECTION): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GP_VOLTAGE_RECONNECT): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GP_FREQUENCY_RECONNECT): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GP_RECONNECT_TIME): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GP_RAMP_RATE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_GP_STARTUP_TIME): NUMBER_ENTITY_SCHEMA,
    }
)

# Settings California Numbers (NEW - registers 340-499)
CONF_SETTINGS_CALIFORNIA = "settings_california"

SETTINGS_CALIFORNIA_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_CA_VOLTAGE_POINT_1): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_VOLTAGE_POINT_2): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_VOLTAGE_POINT_3): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_VOLTAGE_POINT_4): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_VOLTAGE_POINT_5): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_VOLTAGE_POINT_6): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_POWER_POINT_1): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_POWER_POINT_2): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_POWER_POINT_3): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_POWER_POINT_4): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_POWER_POINT_5): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_POWER_POINT_6): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_RAMP_RATE): NUMBER_ENTITY_SCHEMA,
        cv.Optional(CONF_CA_RECONNECT_TIME): NUMBER_ENTITY_SCHEMA,
    }
)

NUMBER_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_DEVICE_ID): cv.use_id(cg.EntityBase),
        cv.Optional(CONF_SETTINGS_BATTERY): SETTINGS_BATTERY_CURRENT_SCHEMA,
        cv.Optional(CONF_SETTINGS_BATTERY_VOLTAGE): SETTINGS_BATTERY_VOLTAGE_SCHEMA,
        cv.Optional(CONF_SETTINGS_BATTERY_SOC): SETTINGS_BATTERY_SOC_SCHEMA,
        cv.Optional(
            CONF_SETTINGS_BATTERY_ADDITIONAL
        ): SETTINGS_BATTERY_ADDITIONAL_SCHEMA,
        cv.Optional(CONF_SETTINGS_GENERATOR): SETTINGS_GENERATOR_SCHEMA,
        cv.Optional(CONF_SETTINGS_GENERATOR_2): SETTINGS_GENERATOR_2_SCHEMA,
        cv.Optional(CONF_SETTINGS_SMART_LOAD): SETTINGS_SMART_LOAD_SCHEMA,
        cv.Optional(CONF_SETTINGS_GRID_CHARGE): SETTINGS_GRID_CHARGE_SCHEMA,
        cv.Optional(
            CONF_SETTINGS_TIME_OF_USE_NUMBERS
        ): SETTINGS_TIME_OF_USE_NUMBERS_SCHEMA,
        cv.Optional(CONF_SETTINGS_GRID_NUMBERS): SETTINGS_GRID_NUMBERS_SCHEMA,
        # NEW: System settings
        cv.Optional(CONF_SETTINGS_SYSTEM_NUMBERS): SETTINGS_SYSTEM_NUMBERS_SCHEMA,
        cv.Optional(CONF_SETTINGS_GRID_PROTECTION): SETTINGS_GRID_PROTECTION_SCHEMA,
        cv.Optional(CONF_SETTINGS_CALIFORNIA): SETTINGS_CALIFORNIA_SCHEMA,
    }
)

# =============================================================================
# CONFIG SCHEMA REGISTRATION
# =============================================================================
CONFIG_SCHEMA = cv.All(
    SENSOR_SCHEMA,
)


# =============================================================================
# ASYNC SETUP FUNCTIONS
# =============================================================================
async def to_code(config):
    """Generate code for the Deye Inverter component."""
    # Create the component instance
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    # Set the Modbus controller parent
    parent = await cg.get_variable(config[CONF_MODBUS_ID])
    cg.add(var.set_parent(parent))

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
    # PROCESS DEVICE INFO
    # =============================================================================
    if CONF_DEVICE_INFO in config:
        device_info_config = config[CONF_DEVICE_INFO]
        for key, entity_key in [
            (CONF_DEVICE_TYPE, "device_type"),
            (CONF_MODBUS_ADDRESS, "modbus_address"),
        ]:
            if key in device_info_config:
                entity_config = device_info_config[key]
                if key == CONF_DEVICE_TYPE:
                    entity = cg.new_Pvariable(entity_config[CONF_ID])
                    cg.add(entity.set_name(entity_config[CONF_NAME]))
                    cg.add(
                        entity.set_disabled_by_default(
                            entity_config[CONF_DISABLED_BY_DEFAULT]
                        )
                    )
                    cg.add(getattr(var, f"set_{entity_key}")(entity))
                    await text_sensor.register_text_sensor(entity, entity_config)
                else:
                    entity = cg.new_Pvariable(entity_config[CONF_ID])
                    cg.add(entity.set_name(entity_config[CONF_NAME]))
                    cg.add(
                        entity.set_disabled_by_default(
                            entity_config[CONF_DISABLED_BY_DEFAULT]
                        )
                    )
                    cg.add(getattr(var, f"set_{entity_key}")(entity))
                    await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS DEVICE INFO EXTENDED (NEW)
    # =============================================================================
    if CONF_DEVICE_INFO_EXTENDED in config:
        device_info_ext_config = config[CONF_DEVICE_INFO_EXTENDED]
        device_info_ext_sensors = [
            (CONF_SERIAL_NUMBER, "serial_number", text_sensor),
            (CONF_FIRMWARE_VERSION, "firmware_version", text_sensor),
            (CONF_HARDWARE_VERSION, "hardware_version", text_sensor),
            (CONF_DEVICE_TYPE_CODE, "device_type_code", sensor),
            (CONF_INVERTER_MODEL, "inverter_model", text_sensor),
            (CONF_INVERTER_POWER_RATING, "inverter_power_rating", sensor),
            (CONF_INVERTER_VOLTAGE_RATING, "inverter_voltage_rating", sensor),
            (CONF_INVERTER_CURRENT_RATING, "inverter_current_rating", sensor),
            (CONF_GRID_FREQUENCY_RATING, "grid_frequency_rating", sensor),
        ]
        for key, entity_key, entity_module in device_info_ext_sensors:
            if key in device_info_ext_config:
                entity_config = device_info_ext_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                if entity_module == text_sensor:
                    await text_sensor.register_text_sensor(entity, entity_config)
                else:
                    await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS BATTERY SENSORS
    # =============================================================================
    if CONF_BATTERY in config:
        battery_config = config[CONF_BATTERY]
        for key, entity_key in [
            (CONF_BATTERY_VOLTAGE, "battery_voltage"),
            (CONF_BATTERY_CURRENT, "battery_current"),
            (CONF_BATTERY_POWER, "battery_power"),
            (CONF_BATTERY_SOC, "battery_soc"),
            (CONF_BATTERY_TEMPERATURE, "battery_temperature"),
            (CONF_BATTERY_CAPACITY, "battery_capacity"),
        ]:
            if key in battery_config:
                entity_config = battery_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS PV STRING SENSORS - FIXED: Uses PV-specific constants
    # =============================================================================
    for pv_group, pv_name in [
        (CONF_PV1, "pv1"),
        (CONF_PV2, "pv2"),
        (CONF_PV3, "pv3"),
        (CONF_PV4, "pv4"),
    ]:
        if pv_group in config:
            pv_config = config[pv_group]
            for key, entity_key in [
                (CONF_PV_VOLTAGE, "voltage"),
                (CONF_PV_CURRENT, "current"),
                (CONF_PV_POWER, "power"),
            ]:
                if key in pv_config:
                    entity_config = pv_config[key]
                    entity = cg.new_Pvariable(entity_config[CONF_ID])
                    cg.add(entity.set_name(entity_config[CONF_NAME]))
                    cg.add(
                        entity.set_disabled_by_default(
                            entity_config[CONF_DISABLED_BY_DEFAULT]
                        )
                    )
                    cg.add(getattr(var, f"set_{pv_name}_{entity_key}")(entity))
                    await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS GRID SENSORS
    # =============================================================================
    if CONF_GRID in config:
        grid_config = config[CONF_GRID]
        grid_sensors = [
            (CONF_GRID_VOLTAGE_L1, "grid_voltage_l1"),
            (CONF_GRID_VOLTAGE_L2, "grid_voltage_l2"),
            (CONF_GRID_VOLTAGE_L3, "grid_voltage_l3"),
            (CONF_GRID_VOLTAGE_L1_L2, "grid_voltage_l1_l2"),
            (CONF_GRID_VOLTAGE_L2_L3, "grid_voltage_l2_l3"),
            (CONF_GRID_VOLTAGE_L3_L1, "grid_voltage_l3_l1"),
            (CONF_GRID_POWER_L1, "grid_power_l1"),
            (CONF_GRID_POWER_L2, "grid_power_l2"),
            (CONF_GRID_POWER_L3, "grid_power_l3"),
            (CONF_GRID_POWER_TOTAL, "grid_power_total"),
            (CONF_GRID_FREQUENCY, "grid_frequency"),
            (CONF_GRID_CURRENT_L1, "grid_current_l1"),
            (CONF_GRID_CURRENT_L2, "grid_current_l2"),
            (CONF_GRID_CURRENT_L3, "grid_current_l3"),
            (CONF_INTERNAL_CT_L1_POWER, "internal_ct_l1_power"),
            (CONF_INTERNAL_CT_L2_POWER, "internal_ct_l2_power"),
            (CONF_INTERNAL_CT_L3_POWER, "internal_ct_l3_power"),
            (CONF_INTERNAL_TOTAL_POWER, "internal_total_power"),
            (CONF_EXTERNAL_CT_L1_POWER, "external_ct_l1_power"),
            (CONF_EXTERNAL_CT_L2_POWER, "external_ct_l2_power"),
            (CONF_EXTERNAL_CT_L3_POWER, "external_ct_l3_power"),
            (CONF_OUT_OF_GRID_TOTAL_POWER, "out_of_grid_total_power"),
            (CONF_GRID_METER_APPARENT_POWER, "grid_meter_apparent_power"),
            (CONF_GRID_METER_POWER_FACTOR, "grid_meter_power_factor"),
            (CONF_GRID_METER_CURRENT_L1, "grid_meter_current_l1"),
            (CONF_GRID_METER_CURRENT_L2, "grid_meter_current_l2"),
            (CONF_GRID_METER_CURRENT_L3, "grid_meter_current_l3"),
            # NEW Grid Side sensors
            (CONF_GRID_SIDE_A_PHASE_POWER, "grid_side_a_phase_power"),
            (CONF_GRID_SIDE_B_PHASE_POWER, "grid_side_b_phase_power"),
            (CONF_GRID_SIDE_C_PHASE_POWER, "grid_side_c_phase_power"),
            (CONF_GRID_SIDE_TOTAL_POWER, "grid_side_total_power"),
            (CONF_TOTAL_GRID_POWER, "total_grid_power"),
        ]
        for key, entity_key in grid_sensors:
            if key in grid_config:
                entity_config = grid_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS LOAD GRID SENSORS
    # =============================================================================
    if CONF_LOAD_GRID in config:
        load_grid_config = config[CONF_LOAD_GRID]
        for key, entity_key in [
            (CONF_LOAD_GRID_POWER_L1, "load_grid_power_l1"),
            (CONF_LOAD_GRID_POWER_L2, "load_grid_power_l2"),
            (CONF_LOAD_GRID_POWER_L3, "load_grid_power_l3"),
            (CONF_LOAD_GRID_POWER_TOTAL, "load_grid_power_total"),
            (CONF_LOAD_GRID_VOLTAGE_L1, "load_grid_voltage_l1"),
            (CONF_LOAD_GRID_VOLTAGE_L2, "load_grid_voltage_l2"),
            (CONF_LOAD_GRID_VOLTAGE_L3, "load_grid_voltage_l3"),
        ]:
            if key in load_grid_config:
                entity_config = load_grid_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS LOAD GRID PORT SENSORS (NEW)
    # =============================================================================
    if CONF_LOAD_GRID_PORT in config:
        load_grid_port_config = config[CONF_LOAD_GRID_PORT]
        for key, entity_key in [
            (CONF_LOAD_PORT_VOLTAGE_L1, "load_port_voltage_l1"),
            (CONF_LOAD_PORT_VOLTAGE_L2, "load_port_voltage_l2"),
            (CONF_LOAD_PORT_VOLTAGE_L3, "load_port_voltage_l3"),
            (CONF_LOAD_PORT_CURRENT_L1, "load_port_current_l1"),
            (CONF_LOAD_PORT_CURRENT_L2, "load_port_current_l2"),
            (CONF_LOAD_PORT_CURRENT_L3, "load_port_current_l3"),
            (CONF_LOAD_PORT_POWER_L1, "load_port_power_l1"),
            (CONF_LOAD_PORT_POWER_L2, "load_port_power_l2"),
            (CONF_LOAD_PORT_POWER_L3, "load_port_power_l3"),
            (CONF_LOAD_REAL_POWER, "load_real_power"),
            (CONF_LOAD_APPARENT_POWER, "load_apparent_power"),
            (CONF_LOAD_FREQUENCY, "load_frequency"),
        ]:
            if key in load_grid_port_config:
                entity_config = load_grid_port_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS LOAD UPS SENSORS
    # =============================================================================
    if CONF_LOAD_UPS in config:
        load_ups_config = config[CONF_LOAD_UPS]
        for key, entity_key in [
            (CONF_LOAD_UPS_POWER_L1, "load_ups_power_l1"),
            (CONF_LOAD_UPS_POWER_L2, "load_ups_power_l2"),
            (CONF_LOAD_UPS_POWER_L3, "load_ups_power_l3"),
            (CONF_LOAD_UPS_POWER_TOTAL, "load_ups_power_total"),
            (CONF_LOAD_UPS_VOLTAGE_L1, "load_ups_voltage_l1"),
            (CONF_LOAD_UPS_VOLTAGE_L2, "load_ups_voltage_l2"),
            (CONF_LOAD_UPS_VOLTAGE_L3, "load_ups_voltage_l3"),
            (CONF_LOAD_UPS_FREQUENCY, "load_ups_frequency"),
        ]:
            if key in load_ups_config:
                entity_config = load_ups_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS GENERATOR SENSORS
    # =============================================================================
    if CONF_GENERATOR in config:
        gen_config = config[CONF_GENERATOR]
        gen_sensors = [
            (CONF_GENERATOR_VOLTAGE_L1, "gen_voltage_l1"),
            (CONF_GENERATOR_VOLTAGE_L2, "gen_voltage_l2"),
            (CONF_GENERATOR_VOLTAGE_L3, "gen_voltage_l3"),
            (CONF_GENERATOR_POWER_L1, "gen_power_l1"),
            (CONF_GENERATOR_POWER_L2, "gen_power_l2"),
            (CONF_GENERATOR_POWER_L3, "gen_power_l3"),
            (CONF_GENERATOR_POWER_TOTAL, "gen_power_total"),
            (CONF_GENERATOR_CURRENT_L1, "gen_current_l1"),
            (CONF_GENERATOR_CURRENT_L2, "gen_current_l2"),
            (CONF_GENERATOR_CURRENT_L3, "gen_current_l3"),
            (CONF_GENERATOR_FREQUENCY, "gen_frequency"),
        ]
        for key, entity_key in gen_sensors:
            if key in gen_config:
                entity_config = gen_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS GENERATOR PORT SENSORS (NEW)
    # =============================================================================
    if CONF_GENERATOR_PORT in config:
        gen_port_config = config[CONF_GENERATOR_PORT]
        gen_port_sensors = [
            (CONF_GEN_PORT_VOLTAGE_L1, "gen_port_voltage_l1"),
            (CONF_GEN_PORT_VOLTAGE_L2, "gen_port_voltage_l2"),
            (CONF_GEN_PORT_VOLTAGE_L3, "gen_port_voltage_l3"),
            (CONF_GEN_PORT_POWER_L1, "gen_port_power_l1"),
            (CONF_GEN_PORT_POWER_L2, "gen_port_power_l2"),
            (CONF_GEN_PORT_POWER_L3, "gen_port_power_l3"),
            (CONF_GEN_PORT_POWER_TOTAL, "gen_port_power_total"),
            (CONF_GEN_PORT_CURRENT_L1, "gen_port_current_l1"),
            (CONF_GEN_PORT_CURRENT_L2, "gen_port_current_l2"),
            (CONF_GEN_PORT_CURRENT_L3, "gen_port_current_l3"),
            (CONF_GEN_PORT_FREQUENCY, "gen_port_frequency"),
        ]
        for key, entity_key in gen_port_sensors:
            if key in gen_port_config:
                entity_config = gen_port_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS TEMPERATURE SENSORS
    # =============================================================================
    if CONF_TEMPERATURES in config:
        temp_config = config[CONF_TEMPERATURES]
        for key, entity_key in [
            (CONF_TEMP_HEATSINK, "temp_heatsink"),
            (CONF_TEMP_DC_TRANSFORMER, "temp_dc_transformer"),
        ]:
            if key in temp_config:
                entity_config = temp_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS INVERTER SENSORS
    # =============================================================================
    if CONF_INVERTER in config:
        inverter_config = config[CONF_INVERTER]
        inverter_sensors = [
            (CONF_INVERTER_VOLTAGE_L1, "inverter_voltage_l1"),
            (CONF_INVERTER_VOLTAGE_L2, "inverter_voltage_l2"),
            (CONF_INVERTER_VOLTAGE_L3, "inverter_voltage_l3"),
            (CONF_INVERTER_REAL_POWER_L1, "inverter_real_power_l1"),
            (CONF_INVERTER_REAL_POWER_L2, "inverter_real_power_l2"),
            (CONF_INVERTER_REAL_POWER_L3, "inverter_real_power_l3"),
            (CONF_INVERTER_REAL_POWER, "inverter_real_power"),
            (CONF_INVERTER_APPARENT_POWER, "inverter_apparent_power"),
            (CONF_INVERTER_FREQUENCY, "inverter_frequency"),
        ]
        for key, entity_key in inverter_sensors:
            if key in inverter_config:
                entity_config = inverter_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS DC SENSORS
    # =============================================================================
    if CONF_DC in config:
        dc_config = config[CONF_DC]
        dc_sensors = [
            (CONF_DC5_CURRENT, "dc5_current"),
            (CONF_DC6_VOLTAGE, "dc6_voltage"),
            (CONF_DC6_CURRENT, "dc6_current"),
            (CONF_DC7_VOLTAGE, "dc7_voltage"),
            (CONF_DC7_CURRENT, "dc7_current"),
            (CONF_DC8_VOLTAGE, "dc8_voltage"),
            (CONF_DC8_CURRENT, "dc8_current"),
        ]
        for key, entity_key in dc_sensors:
            if key in dc_config:
                entity_config = dc_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS BATTERY MODULE SENSORS (NEW)
    # =============================================================================
    battery_module_groups = [
        (CONF_BATTERY_MODULE_1, "battery_module_1"),
        (CONF_BATTERY_MODULE_2, "battery_module_2"),
        (CONF_BATTERY_MODULE_3, "battery_module_3"),
        (CONF_BATTERY_MODULE_4, "battery_module_4"),
        (CONF_BATTERY_MODULE_5, "battery_module_5"),
        (CONF_BATTERY_MODULE_6, "battery_module_6"),
        (CONF_BATTERY_MODULE_7, "battery_module_7"),
        (CONF_BATTERY_MODULE_8, "battery_module_8"),
        (CONF_BATTERY_MODULE_9, "battery_module_9"),
    ]

    for module_conf, module_name in battery_module_groups:
        if module_conf in config:
            module_config = config[module_conf]
            module_sensors = [
                (CONF_BM_VOLTAGE, f"{module_name}_voltage"),
                (CONF_BM_CURRENT, f"{module_name}_current"),
                (CONF_BM_SOC, f"{module_name}_soc"),
                (CONF_BM_TEMPERATURE, f"{module_name}_temperature"),
                (CONF_BM_STATUS, f"{module_name}_status"),
                (CONF_BM_FAULT_CODE, f"{module_name}_fault_code"),
                (CONF_BM_CYCLE_COUNT, f"{module_name}_cycle_count"),
                (CONF_BM_CAPACITY_REMAINING, f"{module_name}_capacity_remaining"),
                (CONF_BM_CAPACITY_TOTAL, f"{module_name}_capacity_total"),
                (CONF_BM_POWER, f"{module_name}_power"),
                (CONF_BM_CELL_MAX_VOLTAGE, f"{module_name}_cell_max_voltage"),
                (CONF_BM_CELL_MIN_VOLTAGE, f"{module_name}_cell_min_voltage"),
                (CONF_BM_CELL_MAX_TEMP, f"{module_name}_cell_max_temp"),
                (CONF_BM_CELL_MIN_TEMP, f"{module_name}_cell_min_temp"),
            ]
            for key, entity_key in module_sensors:
                if key in module_config:
                    entity_config = module_config[key]
                    entity = cg.new_Pvariable(entity_config[CONF_ID])
                    cg.add(entity.set_name(entity_config[CONF_NAME]))
                    cg.add(
                        entity.set_disabled_by_default(
                            entity_config[CONF_DISABLED_BY_DEFAULT]
                        )
                    )
                    cg.add(getattr(var, f"set_{entity_key}")(entity))
                    await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS STATISTICS SENSORS
    # =============================================================================
    if CONF_STATISTICS in config:
        stats_config = config[CONF_STATISTICS]

        # Daily statistics
        if CONF_DAILY in stats_config:
            daily_config = stats_config[CONF_DAILY]
            daily_sensors = [
                (CONF_PRODUCTION, "daily_production"),
                (CONF_BATTERY_CHARGE, "daily_battery_charge"),
                (CONF_BATTERY_DISCHARGE, "daily_battery_discharge"),
                (CONF_GRID_IMPORT, "daily_grid_import"),
                (CONF_GRID_EXPORT, "daily_grid_export"),
                (CONF_CONSUMPTION, "daily_consumption"),
                (CONF_PV_PRODUCTION, "daily_pv_production"),
                (CONF_DAILY_PV1_PRODUCTION, "daily_pv1_production"),
                (CONF_DAILY_PV2_PRODUCTION, "daily_pv2_production"),
                (CONF_DAILY_PV3_PRODUCTION, "daily_pv3_production"),
                (CONF_DAILY_PV4_PRODUCTION, "daily_pv4_production"),
                (CONF_DAILY_GENERATOR_ON_TIME, "daily_generator_on_time"),
                # NEW daily statistics
                (CONF_DAILY_ACTIVE_POWER_GENERATION, "daily_active_power_generation"),
                (CONF_ACTIVE_POWER_GENERATION_TODAY, "active_power_generation_today"),
                (CONF_DAILY_GRID_CONNECTION_TIME, "daily_grid_connection_time"),
            ]
            for key, entity_key in daily_sensors:
                if key in daily_config:
                    entity_config = daily_config[key]
                    entity = cg.new_Pvariable(entity_config[CONF_ID])
                    cg.add(entity.set_name(entity_config[CONF_NAME]))
                    cg.add(
                        entity.set_disabled_by_default(
                            entity_config[CONF_DISABLED_BY_DEFAULT]
                        )
                    )
                    cg.add(getattr(var, f"set_{entity_key}")(entity))
                    await sensor.register_sensor(entity, entity_config)

        # Total statistics
        if CONF_TOTAL in stats_config:
            total_config = stats_config[CONF_TOTAL]
            total_sensors = [
                (CONF_PRODUCTION, "total_production"),
                (CONF_BATTERY_CHARGE, "total_battery_charge"),
                (CONF_BATTERY_DISCHARGE, "total_battery_discharge"),
                (CONF_GRID_IMPORT, "total_grid_import"),
                (CONF_GRID_EXPORT, "total_grid_export"),
                (CONF_CONSUMPTION, "total_consumption"),
                (CONF_PV_PRODUCTION, "total_pv_production"),
                # NEW total statistics
                (CONF_ACTIVE_POWER_GEN_TOTAL_LOW, "active_power_gen_total_low"),
                (CONF_ACTIVE_POWER_GEN_TOTAL_HIGH, "active_power_gen_total_high"),
                (CONF_REACTIVE_POWER_GEN_TOTAL_LOW, "reactive_power_gen_total_low"),
                (CONF_REACTIVE_POWER_GEN_TOTAL_HIGH, "reactive_power_gen_total_high"),
                (CONF_TOTAL_PV_PRODUCTION, "total_pv_production"),
                (CONF_BATTERY_CHARGE_TOTAL_HIGH, "battery_charge_total_high"),
                (CONF_BATTERY_DISCHARGE_TOTAL_HIGH, "battery_discharge_total_high"),
                (CONF_TOTAL_GRID_BUY_HIGH, "total_grid_buy_high"),
                (CONF_TOTAL_GRID_SELL_HIGH, "total_grid_sell_high"),
                (CONF_TOTAL_LOAD_HIGH, "total_load_high"),
            ]
            for key, entity_key in total_sensors:
                if key in total_config:
                    entity_config = total_config[key]
                    entity = cg.new_Pvariable(entity_config[CONF_ID])
                    cg.add(entity.set_name(entity_config[CONF_NAME]))
                    cg.add(
                        entity.set_disabled_by_default(
                            entity_config[CONF_DISABLED_BY_DEFAULT]
                        )
                    )
                    cg.add(getattr(var, f"set_{entity_key}")(entity))
                    await sensor.register_sensor(entity, entity_config)

    # =============================================================================
    # PROCESS STATUS SENSORS
    # =============================================================================
    if CONF_STATUS in config:
        status_config = config[CONF_STATUS]
        status_sensors = [
            (CONF_RUNNING_STATUS, "running_status", text_sensor, "text_sensor"),
            (CONF_WARNING_1_RAW, "warning_1_raw", sensor, "sensor"),
            (CONF_WARNING_2_RAW, "warning_2_raw", sensor, "sensor"),
            (CONF_ERROR_1_RAW, "error_1_raw", sensor, "sensor"),
            (CONF_ERROR_2_RAW, "error_2_raw", sensor, "sensor"),
            (CONF_ERROR_3_RAW, "error_3_raw", sensor, "sensor"),
            (CONF_ERROR_4_RAW, "error_4_raw", sensor, "sensor"),
            (
                CONF_COMMUNICATION_BOARD_FAILURE,
                "communication_board_failure",
                sensor,
                "sensor",
            ),
        ]
        for key, entity_key, entity_module, entity_type in status_sensors:
            if key in status_config:
                entity_config = status_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                if entity_type == "text_sensor":
                    await text_sensor.register_text_sensor(entity, entity_config)
                else:
                    await sensor.register_sensor(entity, entity_config)

    return var


# =============================================================================
# BINARY SENSOR SETUP FUNCTION (NEW)
# =============================================================================
async def binary_sensor_to_code(config):
    """Generate code for Deye Inverter binary sensors."""
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Process relay status group
    if CONF_RELAY_STATUS in config:
        relay_config = config[CONF_RELAY_STATUS]
        for key, entity_key in [
            (CONF_RELAY_INVERTER, "relay_inverter"),
            (CONF_RELAY_LOAD, "relay_load"),
            (CONF_RELAY_GRID, "relay_grid"),
            (CONF_RELAY_GENERATOR, "relay_generator"),
        ]:
            if key in relay_config:
                entity_config = relay_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await binary_sensor.register_binary_sensor(entity, entity_config)

    # Process warnings group
    if CONF_WARNINGS in config:
        warnings_config = config[CONF_WARNINGS]
        for key, entity_key in [
            (CONF_FAN_FAILURE, "fan_failure"),
            (CONF_GRID_PHASE, "grid_phase"),
            (CONF_GRID_PHASE_FAULT, "grid_phase_fault"),
        ]:
            if key in warnings_config:
                entity_config = warnings_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await binary_sensor.register_binary_sensor(entity, entity_config)


# =============================================================================
# SWITCH SETUP FUNCTION (NEW)
# =============================================================================
async def switch_to_code(config):
    """Generate code for Deye Inverter switches."""
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Process settings grid switches
    if CONF_SETTINGS_GRID in config:
        grid_config = config[CONF_SETTINGS_GRID]
        for key, entity_key in [
            (CONF_GRID_CHARGE, "grid_charge"),
            (CONF_SOLAR_SELL, "solar_sell"),
            (CONF_MICROINVERTER_EXPORT_TO_GRID, "microinverter_export_to_grid"),
        ]:
            if key in grid_config:
                entity_config = grid_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await switch.register_switch(entity, entity_config)

    # Process settings system switches (NEW)
    if CONF_SETTINGS_SYSTEM in config:
        system_config = config[CONF_SETTINGS_SYSTEM]
        for key, entity_key in [
            (CONF_SYS_BEEPER, "sys_beeper"),
            (CONF_SYS_LCD_BACKLIGHT, "sys_lcd_backlight"),
            (CONF_SYS_DST_ENABLE, "sys_dst_enable"),
            (CONF_SYS_REMOTE_LOCK, "sys_remote_lock"),
        ]:
            if key in system_config:
                entity_config = system_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await switch.register_switch(entity, entity_config)

    # Process time of use switches
    if CONF_SETTINGS_TIME_OF_USE in config:
        tou_config = config[CONF_SETTINGS_TIME_OF_USE]
        if CONF_TIME_OF_USE in tou_config:
            entity_config = tou_config[CONF_TIME_OF_USE]
            entity = cg.new_Pvariable(entity_config[CONF_ID])
            cg.add(entity.set_name(entity_config[CONF_NAME]))
            cg.add(
                entity.set_disabled_by_default(entity_config[CONF_DISABLED_BY_DEFAULT])
            )
            cg.add(var.set_time_of_use(entity))
            await switch.register_switch(entity, entity_config)

        # Process time point charge enable switches
        for tp_key, tp_name in [
            (CONF_TIME_POINT_1_CHARGE_ENABLE, "time_point_1"),
            (CONF_TIME_POINT_2_CHARGE_ENABLE, "time_point_2"),
            (CONF_TIME_POINT_3_CHARGE_ENABLE, "time_point_3"),
            (CONF_TIME_POINT_4_CHARGE_ENABLE, "time_point_4"),
            (CONF_TIME_POINT_5_CHARGE_ENABLE, "time_point_5"),
            (CONF_TIME_POINT_6_CHARGE_ENABLE, "time_point_6"),
        ]:
            if tp_key in tou_config:
                entity_config = tou_config[tp_key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{tp_name}_charge_enable")(entity))
                await switch.register_switch(entity, entity_config)

    # Process settings device switches
    if CONF_SETTINGS_DEVICE in config:
        device_config = config[CONF_SETTINGS_DEVICE]
        for key, entity_key in [
            (CONF_EXTERNAL_CT_DIRECTION_CHECK, "external_ct_direction_check"),
            (CONF_SOLAR_ARC_FAULT_MODE, "solar_arc_fault_mode"),
        ]:
            if key in device_config:
                entity_config = device_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await switch.register_switch(entity, entity_config)

    # Process settings working mode switches
    if CONF_SETTINGS_WORKING_MODE in config:
        working_mode_config = config[CONF_SETTINGS_WORKING_MODE]
        for key, entity_key in [
            (CONF_FORCED_OFF_GRID_WORK, "forced_off_grid_work"),
        ]:
            if key in working_mode_config:
                entity_config = working_mode_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await switch.register_switch(entity, entity_config)

    # Process settings battery switches
    if CONF_SETTINGS_BATTERY in config:
        battery_config = config[CONF_SETTINGS_BATTERY]
        for key, entity_key in [
            (CONF_BATTERY_LOSS_REPORT_FAULT, "battery_loss_report_fault"),
        ]:
            if key in battery_config:
                entity_config = battery_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await switch.register_switch(entity, entity_config)

    # Process settings generator switches
    if CONF_SETTINGS_GENERATOR in config:
        generator_config = config[CONF_SETTINGS_GENERATOR]
        for key, entity_key in [
            (CONF_EXTERNAL_RELAY, "external_relay"),
        ]:
            if key in generator_config:
                entity_config = generator_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await switch.register_switch(entity, entity_config)


# =============================================================================
# SELECT SETUP FUNCTION (NEW)
# =============================================================================
async def select_to_code(config):
    """Generate code for Deye Inverter selects."""
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Process settings device selects
    if CONF_SETTINGS_DEVICE in config:
        device_config = config[CONF_SETTINGS_DEVICE]
        for key, entity_key in [
            (CONF_GRID_TYPE, "grid_type"),
            (CONF_GRID_MODE, "grid_mode"),
            (CONF_GRID_NOMINAL_VOLTAGE, "grid_nominal_voltage"),
            (CONF_GRID_NOMINAL_FREQUENCY, "grid_nominal_frequency"),
            (CONF_GRID_PHASE_SEQUENCE, "grid_phase_sequence"),
        ]:
            if key in device_config:
                entity_config = device_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await select.register_select(entity, entity_config)

    # Process settings battery selects
    if CONF_SETTINGS_BATTERY in config:
        battery_config = config[CONF_SETTINGS_BATTERY]
        for key, entity_key in [
            (CONF_BATTERY_TYPE, "battery_type"),
            (CONF_BATTERY_CONTROL_MODE, "battery_control_mode"),
        ]:
            if key in battery_config:
                entity_config = battery_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await select.register_select(entity, entity_config)

    # Process gen port control mode select
    if CONF_SETTINGS_GEN_PORT in config:
        gen_port_config = config[CONF_SETTINGS_GEN_PORT]
        if CONF_GEN_PORT_CONTROL_MODE in gen_port_config:
            entity_config = gen_port_config[CONF_GEN_PORT_CONTROL_MODE]
            entity = cg.new_Pvariable(entity_config[CONF_ID])
            cg.add(entity.set_name(entity_config[CONF_NAME]))
            cg.add(
                entity.set_disabled_by_default(entity_config[CONF_DISABLED_BY_DEFAULT])
            )
            cg.add(var.set_gen_port_control_mode(entity))
            await select.register_select(entity, entity_config)

    # Process working mode selects (energy_priority and limit_control_mode moved here)
    if CONF_SETTINGS_WORKING_MODE in config:
        working_mode_config = config[CONF_SETTINGS_WORKING_MODE]
        for key, entity_key in [
            (CONF_WORKING_MODE, "working_mode"),
            (CONF_ENERGY_PRIORITY, "energy_priority"),
            (CONF_LIMIT_CONTROL_MODE, "limit_control_mode"),
        ]:
            if key in working_mode_config:
                entity_config = working_mode_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await select.register_select(entity, entity_config)

    # Process settings system selects
    if CONF_SETTINGS_SYSTEM in config:
        system_config = config[CONF_SETTINGS_SYSTEM]
        if CONF_SYS_LANGUAGE in system_config:
            entity_config = system_config[CONF_SYS_LANGUAGE]
            entity = cg.new_Pvariable(entity_config[CONF_ID])
            cg.add(entity.set_name(entity_config[CONF_NAME]))
            cg.add(
                entity.set_disabled_by_default(entity_config[CONF_DISABLED_BY_DEFAULT])
            )
            cg.add(var.set_sys_language(entity))
            await select.register_select(entity, entity_config)

    # Process settings device selects (ext_* moved here)
    if CONF_SETTINGS_DEVICE in config:
        ext_config = config[CONF_SETTINGS_DEVICE]
        for key, entity_key in [
            (CONF_EXT_BAUD_RATE, "ext_baud_rate"),
            (CONF_EXT_PARITY, "ext_parity"),
            (CONF_EXT_STOP_BITS, "ext_stop_bits"),
            (CONF_EXT_PROTOCOL, "ext_protocol"),
        ]:
            if key in ext_config:
                entity_config = ext_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await select.register_select(entity, entity_config)

    # Process settings california selects
    if CONF_SETTINGS_CALIFORNIA in config:
        ca_config = config[CONF_SETTINGS_CALIFORNIA]
        for key, entity_key in [
            (CONF_CA_RULE21_CATEGORY, "ca_rule21_category"),
            (CONF_CA_NORMAL_OP_CAT, "ca_normal_op_cat"),
            (CONF_CA_ABNORMAL_OP_CAT, "ca_abnormal_op_cat"),
        ]:
            if key in ca_config:
                entity_config = ca_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await select.register_select(entity, entity_config)


# =============================================================================
# NUMBER SETUP FUNCTION (NEW)
# =============================================================================
async def number_to_code(config):
    """Generate code for Deye Inverter numbers."""
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Process settings battery current numbers
    if CONF_SETTINGS_BATTERY in config:
        battery_config = config[CONF_SETTINGS_BATTERY]
        for key, entity_key in [
            (CONF_MAX_CHARGE_CURRENT, "max_charge_current"),
            (CONF_MAX_DISCHARGE_CURRENT, "max_discharge_current"),
        ]:
            if key in battery_config:
                entity_config = battery_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity, entity_config, min_value=0, max_value=185, step=1
                )

    # Process settings battery voltage numbers
    if CONF_SETTINGS_BATTERY_VOLTAGE in config:
        voltage_config = config[CONF_SETTINGS_BATTERY_VOLTAGE]
        for key, entity_key in [
            (CONF_EQUALIZATION_VOLTAGE, "equalization_voltage"),
            (CONF_ABSORPTION_VOLTAGE, "absorption_voltage"),
            (CONF_FLOAT_VOLTAGE, "float_voltage"),
            (CONF_EMPTY_VOLTAGE, "empty_voltage"),
            (CONF_SHUTDOWN_VOLTAGE, "shutdown_voltage"),
            (CONF_RESTART_VOLTAGE, "restart_voltage"),
            (CONF_LOW_VOLTAGE_WARNING, "low_voltage_warning"),
        ]:
            if key in voltage_config:
                entity_config = voltage_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity, entity_config, min_value=38.0, max_value=61.0, step=0.01
                )

    # Process settings battery SOC numbers
    if CONF_SETTINGS_BATTERY_SOC in config:
        soc_config = config[CONF_SETTINGS_BATTERY_SOC]
        for key, entity_key in [
            (CONF_SHUTDOWN_SOC, "shutdown_soc"),
            (CONF_RESTART_SOC, "restart_soc"),
            (CONF_LOW_SOC_WARNING, "low_soc_warning"),
        ]:
            if key in soc_config:
                entity_config = soc_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity, entity_config, min_value=0, max_value=100, step=1
                )

    # Process settings battery additional numbers
    if CONF_SETTINGS_BATTERY_ADDITIONAL in config:
        additional_config = config[CONF_SETTINGS_BATTERY_ADDITIONAL]
        battery_additional_numbers = [
            (CONF_BATTERY_CAPACITY_AH, "battery_capacity_ah", 0, 2000, 1),
            (CONF_EQUALIZATION_DAY_CYCLE, "equalization_day_cycle", 0, 90, 1),
            (CONF_EQUALIZATION_TIME, "equalization_time", 0, 20, 0.5),
            (CONF_TEMPCO, "tempco", 0, 50, 1),
            (CONF_BATTERY_WAKE_UP, "battery_wake_up", 0, 1, 1),
            (CONF_BATTERY_RESISTANCE, "battery_resistance", 0, 6000, 1),
            (
                CONF_BATTERY_CHARGING_EFFICIENCY,
                "battery_charging_efficiency",
                0,
                100,
                0.1,
            ),
        ]
        for key, entity_key, min_val, max_val, step in battery_additional_numbers:
            if key in additional_config:
                entity_config = additional_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings generator numbers
    if CONF_SETTINGS_GENERATOR in config:
        gen_config = config[CONF_SETTINGS_GENERATOR]
        generator_numbers = [
            (CONF_GEN_MAX_RUN_TIME, "gen_max_run_time", 0, 120, 0.1),
            (CONF_GEN_COOLDOWN_TIME, "gen_cooldown_time", 0, 60, 1),
            (CONF_GEN_MIN_POWER, "gen_min_power", 0, 6500, 1),
            (CONF_GEN_START_VOLTAGE, "gen_start_voltage", 38.0, 61.0, 0.01),
            (CONF_GEN_START_SOC, "gen_start_soc", 0, 100, 1),
            (CONF_GEN_CHARGING_CURRENT, "gen_charging_current", 0, 185, 1),
            (CONF_GEN_ENABLE, "gen_enable", 0, 1, 1),
        ]
        for key, entity_key, min_val, max_val, step in generator_numbers:
            if key in gen_config:
                entity_config = gen_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings generator 2 numbers
    if CONF_SETTINGS_GENERATOR_2 in config:
        gen2_config = config[CONF_SETTINGS_GENERATOR_2]
        generator2_numbers = [
            (CONF_GEN_MAX_TIME, "gen_max_time", 0, 24, 0.1),
            (CONF_GEN_COOLDOWN, "gen_cooldown", 0, 24, 0.1),
            (CONF_GEN_START_VOLTAGE_225, "gen_start_voltage_225", 38.0, 63.0, 0.01),
            (CONF_GEN_START_SOC_226, "gen_start_soc_226", 0, 100, 1),
            (CONF_GEN_CHARGE_CURRENT_227, "gen_charge_current_227", 0, 185, 1),
        ]
        for key, entity_key, min_val, max_val, step in generator2_numbers:
            if key in gen2_config:
                entity_config = gen2_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings smart load numbers
    if CONF_SETTINGS_SMART_LOAD in config:
        smart_load_config = config[CONF_SETTINGS_SMART_LOAD]
        for key, entity_key in [
            (CONF_SMART_LOAD_OFF_VOLTAGE, "smart_load_off_voltage"),
            (CONF_SMART_LOAD_ON_VOLTAGE, "smart_load_on_voltage"),
        ]:
            if key in smart_load_config:
                entity_config = smart_load_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity, entity_config, min_value=38.0, max_value=61.0, step=0.01
                )
        for key, entity_key in [
            (CONF_SMART_LOAD_OFF_SOC, "smart_load_off_soc"),
            (CONF_SMART_LOAD_ON_SOC, "smart_load_on_soc"),
        ]:
            if key in smart_load_config:
                entity_config = smart_load_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity, entity_config, min_value=0, max_value=100, step=1
                )

    # Process settings grid charge numbers
    if CONF_SETTINGS_GRID_CHARGE in config:
        grid_charge_config = config[CONF_SETTINGS_GRID_CHARGE]
        for key, entity_key, min_val, max_val, step in [
            (
                CONF_MAXIMUM_BATTERY_GRID_CHARGE_CURRENT,
                "maximum_battery_grid_charge_current",
                0,
                185,
                1,
            ),
            (
                CONF_GRID_CHARGE_START_VOLTAGE,
                "grid_charge_start_voltage",
                38.0,
                63.0,
                0.01,
            ),
            (CONF_GRID_CHARGE_START_SOC, "grid_charge_start_soc", 0, 100, 1),
            (CONF_GRID_CHARGE_CURRENT, "grid_charge_current", 0, 185, 1),
        ]:
            if key in grid_charge_config:
                entity_config = grid_charge_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings grid numbers (distributed from settings_special)
    if CONF_SETTINGS_GRID_NUMBERS in config:
        grid_numbers_config = config[CONF_SETTINGS_GRID_NUMBERS]
        grid_numbers = [
            (CONF_ZERO_EXPORT_POWER, "zero_export_power", 0, 90, 1),
            (CONF_MAX_SOLAR_SELL_POWER, "max_solar_sell_power", 0, 6500, 1),
            (CONF_GRID_MAX_POWER, "grid_max_power", 0, 6500, 1),
            (CONF_RESTORE_CONNECTION_TIME, "restore_connection_time", 0, 300, 1),
        ]
        for key, entity_key, min_val, max_val, step in grid_numbers:
            if key in grid_numbers_config:
                entity_config = grid_numbers_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings generator numbers (distributed from settings_special)
    if CONF_SETTINGS_GENERATOR in config:
        gen_numbers_config = config[CONF_SETTINGS_GENERATOR]
        gen_numbers = [
            (
                CONF_GEN_PORT_COUPLE_FREQ_LIMIT,
                "gen_port_couple_freq_limit",
                0,
                100,
                0.01,
            ),
            (
                CONF_GENERATOR_REQUIRED_POWER_START,
                "generator_required_power_start",
                0,
                6500,
                1,
            ),
        ]
        for key, entity_key, min_val, max_val, step in gen_numbers:
            if key in gen_numbers_config:
                entity_config = gen_numbers_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings time of use numbers
    if CONF_SETTINGS_TIME_OF_USE_NUMBERS in config:
        tou_config = config[CONF_SETTINGS_TIME_OF_USE_NUMBERS]
        # Time Point Start times (addresses 148-153)
        for key, entity_key, min_val, max_val, step in [
            (CONF_TIME_POINT_1_START, "time_point_1_start", 0, 2359, 1),
            (CONF_TIME_POINT_2_START, "time_point_2_start", 0, 2359, 1),
            (CONF_TIME_POINT_3_START, "time_point_3_start", 0, 2359, 1),
            (CONF_TIME_POINT_4_START, "time_point_4_start", 0, 2359, 1),
            (CONF_TIME_POINT_5_START, "time_point_5_start", 0, 2359, 1),
            (CONF_TIME_POINT_6_START, "time_point_6_start", 0, 2359, 1),
        ]:
            if key in tou_config:
                entity_config = tou_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )
        # Time Point Power values (addresses 154-159)
        for key, entity_key, min_val, max_val, step in [
            (CONF_TIME_POINT_1_POWER, "time_point_1_power", -6500, 6500, 1),
            (CONF_TIME_POINT_2_POWER, "time_point_2_power", -6500, 6500, 1),
            (CONF_TIME_POINT_3_POWER, "time_point_3_power", -6500, 6500, 1),
            (CONF_TIME_POINT_4_POWER, "time_point_4_power", -6500, 6500, 1),
            (CONF_TIME_POINT_5_POWER, "time_point_5_power", -6500, 6500, 1),
            (CONF_TIME_POINT_6_POWER, "time_point_6_power", -6500, 6500, 1),
        ]:
            if key in tou_config:
                entity_config = tou_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )
        # Time Point Min Battery Voltage (addresses 160-165)
        for key, entity_key, min_val, max_val, step in [
            (
                CONF_TIME_POINT_1_MIN_BATTERY_VOLTAGE,
                "time_point_1_min_battery_voltage",
                41.0,
                63.0,
                0.01,
            ),
            (
                CONF_TIME_POINT_2_MIN_BATTERY_VOLTAGE,
                "time_point_2_min_battery_voltage",
                41.0,
                63.0,
                0.01,
            ),
            (
                CONF_TIME_POINT_3_MIN_BATTERY_VOLTAGE,
                "time_point_3_min_battery_voltage",
                41.0,
                63.0,
                0.01,
            ),
            (
                CONF_TIME_POINT_4_MIN_BATTERY_VOLTAGE,
                "time_point_4_min_battery_voltage",
                41.0,
                63.0,
                0.01,
            ),
            (
                CONF_TIME_POINT_5_MIN_BATTERY_VOLTAGE,
                "time_point_5_min_battery_voltage",
                41.0,
                63.0,
                0.01,
            ),
            (
                CONF_TIME_POINT_6_MIN_BATTERY_VOLTAGE,
                "time_point_6_min_battery_voltage",
                41.0,
                63.0,
                0.01,
            ),
        ]:
            if key in tou_config:
                entity_config = tou_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )
        # Time Point Capacity (addresses 166-171)
        for key, entity_key, min_val, max_val, step in [
            (CONF_TIME_POINT_1_CAPACITY, "time_point_1_capacity", 0, 100, 1),
            (CONF_TIME_POINT_2_CAPACITY, "time_point_2_capacity", 0, 100, 1),
            (CONF_TIME_POINT_3_CAPACITY, "time_point_3_capacity", 0, 100, 1),
            (CONF_TIME_POINT_4_CAPACITY, "time_point_4_capacity", 0, 100, 1),
            (CONF_TIME_POINT_5_CAPACITY, "time_point_5_capacity", 0, 100, 1),
            (CONF_TIME_POINT_6_CAPACITY, "time_point_6_capacity", 0, 100, 1),
        ]:
            if key in tou_config:
                entity_config = tou_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings system numbers (NEW)
    if CONF_SETTINGS_SYSTEM_NUMBERS in config:
        system_config = config[CONF_SETTINGS_SYSTEM_NUMBERS]
        for key, entity_key, min_val, max_val, step in [
            (CONF_SYS_LCD_CONTRAST, "sys_lcd_contrast", 0, 100, 1),
            (CONF_SYS_TIME_ZONE, "sys_time_zone", -12, 12, 0.5),
            (CONF_SYS_DATA_LOG_INTERVAL, "sys_data_log_interval", 1, 60, 1),
        ]:
            if key in system_config:
                entity_config = system_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings grid protection numbers (NEW)
    if CONF_SETTINGS_GRID_PROTECTION in config:
        gp_config = config[CONF_SETTINGS_GRID_PROTECTION]
        for key, entity_key, min_val, max_val, step in [
            (
                CONF_GP_OVER_VOLTAGE_PROTECTION,
                "gp_over_voltage_protection",
                200,
                300,
                0.1,
            ),
            (
                CONF_GP_UNDER_VOLTAGE_PROTECTION,
                "gp_under_voltage_protection",
                100,
                200,
                0.1,
            ),
            (
                CONF_GP_OVER_FREQUENCY_PROTECTION,
                "gp_over_frequency_protection",
                50,
                65,
                0.01,
            ),
            (
                CONF_GP_UNDER_FREQUENCY_PROTECTION,
                "gp_under_frequency_protection",
                45,
                55,
                0.01,
            ),
            (CONF_GP_VOLTAGE_RECONNECT, "gp_voltage_reconnect", 180, 260, 0.1),
            (CONF_GP_FREQUENCY_RECONNECT, "gp_frequency_reconnect", 47, 53, 0.01),
            (CONF_GP_RECONNECT_TIME, "gp_reconnect_time", 0, 300, 1),
            (CONF_GP_RAMP_RATE, "gp_ramp_rate", 1, 100, 1),
            (CONF_GP_STARTUP_TIME, "gp_startup_time", 0, 600, 1),
        ]:
            if key in gp_config:
                entity_config = gp_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )

    # Process settings california numbers (NEW)
    if CONF_SETTINGS_CALIFORNIA in config:
        ca_config = config[CONF_SETTINGS_CALIFORNIA]
        for key, entity_key, min_val, max_val, step in [
            (CONF_CA_VOLTAGE_POINT_1, "ca_voltage_point_1", 0, 300, 0.1),
            (CONF_CA_VOLTAGE_POINT_2, "ca_voltage_point_2", 0, 300, 0.1),
            (CONF_CA_VOLTAGE_POINT_3, "ca_voltage_point_3", 0, 300, 0.1),
            (CONF_CA_VOLTAGE_POINT_4, "ca_voltage_point_4", 0, 300, 0.1),
            (CONF_CA_VOLTAGE_POINT_5, "ca_voltage_point_5", 0, 300, 0.1),
            (CONF_CA_VOLTAGE_POINT_6, "ca_voltage_point_6", 0, 300, 0.1),
            (CONF_CA_POWER_POINT_1, "ca_power_point_1", 0, 100, 1),
            (CONF_CA_POWER_POINT_2, "ca_power_point_2", 0, 100, 1),
            (CONF_CA_POWER_POINT_3, "ca_power_point_3", 0, 100, 1),
            (CONF_CA_POWER_POINT_4, "ca_power_point_4", 0, 100, 1),
            (CONF_CA_POWER_POINT_5, "ca_power_point_5", 0, 100, 1),
            (CONF_CA_POWER_POINT_6, "ca_power_point_6", 0, 100, 1),
            (CONF_CA_RAMP_RATE, "ca_ramp_rate", 1, 100, 1),
            (CONF_CA_RECONNECT_TIME, "ca_reconnect_time", 0, 300, 1),
        ]:
            if key in ca_config:
                entity_config = ca_config[key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await number.register_number(
                    entity,
                    entity_config,
                    min_value=min_val,
                    max_value=max_val,
                    step=step,
                )


# =============================================================================
# CONF CONSTANTS - Time Platform (appended)
# =============================================================================
CONF_MAX_TIME_DIFF = "max_time_diff"


# =============================================================================
# TIME SETUP FUNCTION
# =============================================================================
async def time_to_code(config):
    """Generate code for Deye Inverter time synchronization."""
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Process system time entity
    entity = cg.new_Pvariable(config[CONF_ID])
    cg.add(entity.set_parent(var))
    if CONF_MAX_TIME_DIFF in config:
        cg.add(entity.set_max_time_diff(config[CONF_MAX_TIME_DIFF]))
    await time.register_time(entity, config)
