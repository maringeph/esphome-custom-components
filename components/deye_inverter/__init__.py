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
from esphome.components import modbus_controller

MULTI_CONF = True
AUTO_LOAD = ["modbus_controller"]

# =============================================================================
# CONF CONSTANTS - Main Component
# =============================================================================
CONF_DEYE_INVERTER_ID = "deye_inverter_id"
CONF_DEVICE_ID = "device_id"
CONF_MODBUS_ID = "modbus_id"
CONF_ADDRESS = "address"

# Update intervals (0 = never)
CONF_UPDATE_INTERVAL_LIVE = "update_interval_live"
CONF_UPDATE_INTERVAL_STATISTICS = "update_interval_statistics"
CONF_UPDATE_INTERVAL_SETTINGS = "update_interval_settings"
CONF_UPDATE_INTERVAL_DEVICE_INFO = "update_interval_device_info"

# Manual read actions
CONF_ACTION_READ_DEVICE_INFO = "read_device_info"
CONF_ACTION_READ_LIVE_DATA = "read_live_data"
CONF_ACTION_READ_STATISTICS = "read_statistics"
CONF_ACTION_READ_SETTINGS = "read_settings"

# Manual read actions
CONF_ACTION_READ_DEVICE_INFO = "read_device_info"
CONF_ACTION_READ_LIVE_DATA = "read_live_data"
CONF_ACTION_READ_STATISTICS = "read_statistics"
CONF_ACTION_READ_SETTINGS = "read_settings"

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

# PV-specific constants
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
# CONF CONSTANTS - Time Platform
# =============================================================================
CONF_MAX_TIME_DIFF = "max_time_diff"

# =============================================================================
# CONF CONSTANTS - Additional Settings Groups (used by platform files)
# =============================================================================
CONF_SETTINGS_BATTERY_ADDITIONAL = "settings_battery_additional"
CONF_SETTINGS_TIME_OF_USE_NUMBERS = "settings_time_of_use_numbers"
CONF_SETTINGS_SYSTEM_NUMBERS = "settings_system_numbers"
CONF_SETTINGS_GEN_PORT = "settings_gen_port"
CONF_SETTINGS_GRID_NUMBERS = "settings_grid_numbers"

# =============================================================================
# NAMESPACE
# =============================================================================
deye_inverter_ns = cg.esphome_ns.namespace("deye_inverter")
DeyeInverter = deye_inverter_ns.class_(
    "DeyeInverter", modbus_controller.ModbusController
)

# =============================================================================
# DEVICE MANAGEMENT (for Home Assistant grouping)
# =============================================================================
from esphome.helpers import fnv1a_32bit_hash

# Cache for device objects to avoid recreating them
devices_cache = {}

Device = cg.esphome_ns.class_("Device")


async def get_or_create_device(device_id: str | None) -> cg.MockObj | None:
    """Create or retrieve a cached Device object for Home Assistant grouping.

    When device_id is configured, this creates a Device object that groups
    all entities with the same device_id as a subdevice in Home Assistant.

    Args:
        device_id: The device identifier string (e.g., "wechselrichter_01")

    Returns:
        A Device object if device_id is provided, None otherwise
    """
    if device_id is None:
        return None

    # Check cache first
    if device_id in devices_cache:
        return devices_cache[device_id]

    # Create new device with unique ID
    device_hash = fnv1a_32bit_hash(device_id)
    device_id_obj = cv.declare_id(Device)(f"deye_device_{device_hash}")
    device_var = cg.new_Pvariable(device_id_obj)

    # Configure device properties
    cg.add(device_var.set_device_id(device_hash))
    cg.add(device_var.set_name(device_id))

    # Register device with ESPHome
    cg.add(cg.App.register_device(device_var))

    # Cache for reuse
    devices_cache[device_id] = device_var

    return device_var


def set_entity_device(entity_var, device_var):
    """Associate an entity with a device.

    Args:
        entity_var: The entity variable
        device_var: The device variable (from get_or_create_device)
    """
    if device_var is not None:
        cg.add(entity_var.set_device(device_var))


# =============================================================================
# AUTOMATION ACTIONS - Manual Read Operations
# =============================================================================
from esphome import automation

# Declare action classes
DeyeReadDeviceInfoAction = deye_inverter_ns.class_(
    "DeyeReadDeviceInfoAction", automation.Action
)
DeyeReadLiveDataAction = deye_inverter_ns.class_(
    "DeyeReadLiveDataAction", automation.Action
)
DeyeReadStatisticsAction = deye_inverter_ns.class_(
    "DeyeReadStatisticsAction", automation.Action
)
DeyeReadSettingsAction = deye_inverter_ns.class_(
    "DeyeReadSettingsAction", automation.Action
)


# Action: Read Device Info
@automation.register_action(
    "deye_inverter.read_device_info",
    DeyeReadDeviceInfoAction,
    cv.Schema(
        {
            cv.GenerateID(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        }
    ),
)
async def deye_inverter_read_device_info_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    parent = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])
    cg.add(var.set_parent(parent))
    return var


# Action: Read Live Data
@automation.register_action(
    "deye_inverter.read_live_data",
    DeyeReadLiveDataAction,
    cv.Schema(
        {
            cv.GenerateID(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        }
    ),
)
async def deye_inverter_read_live_data_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    parent = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])
    cg.add(var.set_parent(parent))
    return var


# Action: Read Statistics
@automation.register_action(
    "deye_inverter.read_statistics",
    DeyeReadStatisticsAction,
    cv.Schema(
        {
            cv.GenerateID(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        }
    ),
)
async def deye_inverter_read_statistics_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    parent = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])
    cg.add(var.set_parent(parent))
    return var


# Action: Read Settings
@automation.register_action(
    "deye_inverter.read_settings",
    DeyeReadSettingsAction,
    cv.Schema(
        {
            cv.GenerateID(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        }
    ),
)
async def deye_inverter_read_settings_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    parent = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])
    cg.add(var.set_parent(parent))
    return var
