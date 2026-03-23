#include "deye_inverter.h"
#include "esphome/core/log.h"

namespace esphome {
namespace deye_inverter {

static const char *const TAG = "deye_inverter";

// =============================================================================
// STATIC REGISTER RANGE DEFINITIONS (Complete Set - All 595 Registers)
// =============================================================================

// Live Data Ranges (1s Interval) - Covers all live_data and status categories
const RegisterRange DeyeInverter::LIVE_RANGES[] = {
    // DC Extended measurements (212-218) - DC5-DC8 voltage/current
    {212, 7, "DC Extended"},    // 212-218 (7 registers)
    // Status: Running status (500)
    RANGE_RUNNING_STATUS,   // 500-500 (1 register)
    // Status: Comm status (548-585) - includes warnings, errors, fan status
    RANGE_COMM_STATUS,      // 548-585 (38 registers)
    // Temperatures + reserves (540-547)
    RANGE_TEMPERATURES,     // 540-547 (8 registers)
    // Battery live data + reserves (586-597)
    RANGE_BATTERY_LIVE,     // 586-597 (12 registers)
    // Grid port measurements (598-612)
    RANGE_GRID_PORT_LIVE,   // 598-612 (15 registers)
    // Grid meter measurements (613-626)
    RANGE_GRID_METER_LIVE,  // 613-626 (14 registers)
    // Inverter output (627-639)
    RANGE_INVERTER_OUTPUT_LIVE,  // 627-639 (13 registers)
    // UPS load measurements (640-643)
    RANGE_UPS_LOAD_LIVE,    // 640-643 (4 registers)
    // Load port measurements (644-660)
    RANGE_LOAD_PORT_LIVE,   // 644-660 (17 registers)
    // Generator port measurements (661-671)
    RANGE_GENERATOR_PORT_LIVE,  // 661-671 (11 registers)
    // PV inputs (672-683)
    RANGE_PV_LIVE           // 672-683 (12 registers)
};

// Statistics Ranges (5s Interval) - Covers addresses 501-539
const RegisterRange DeyeInverter::STATS_RANGES[] = {
    // Daily statistics (501-514)
    RANGE_DAILY_STATS,      // 501-514 (14 registers)
    // Battery statistics (514-519)
    RANGE_BATTERY_STATS,    // 514-519 (6 registers)
    // Grid statistics (520-529) - includes consumption, PV daily
    RANGE_GRID_STATS,       // 520-529 (10 registers)
    // PV statistics (529-539) - includes total PV production
    RANGE_PV_STATS          // 529-539 (11 registers)
};

// Settings Ranges (60s Interval) - Covers addresses 98-230, 340
const RegisterRange DeyeInverter::SETTINGS_RANGES[] = {
    // Battery settings (98-120)
    RANGE_BATTERY_SETTINGS_1,       // 98-120 (23 registers)
    // Generator settings (121-127)
    RANGE_GENERATOR_SETTINGS_1,     // 121-127 (7 registers)
    // Grid settings (128-147)
    RANGE_GRID_SETTINGS,            // 128-147 (20 registers)
    // Time of use - start times (148-153)
    RANGE_TIME_POINT_START,         // 148-153 (6 registers)
    // Time of use - power settings (154-159)
    RANGE_TIME_POINT_POWER,         // 154-159 (6 registers)
    // Time of use - voltage limits (160-165)
    RANGE_TIME_POINT_VOLTAGE,       // 160-165 (6 registers)
    // Time of use - SOC limits (166-171)
    RANGE_TIME_POINT_CAPACITY,      // 166-171 (6 registers)
    // Time of use - charge enable (172-177)
    RANGE_TIME_POINT_CHARGE,        // 172-177 (6 registers)
    // Special functions (178-184)
    RANGE_SPECIAL_FUNCTIONS,        // 178-184 (7 registers)
    // Battery settings part 2 (201-222)
    RANGE_BATTERY_SETTINGS_2,       // 201-222 (22 registers)
    // Generator extended settings (223-230)
    RANGE_GENERATOR_SETTINGS_2,     // 223-230 (8 registers)
    // Max solar power (340)
    RANGE_SOLAR_SETTINGS            // 340 (1 register)
};

// System Settings Ranges (60-97) - 38 registers
const RegisterRange DeyeInverter::SETTINGS_SYSTEM_RANGES[] = {
    {60, 10, "System Settings 60-69"},    // 60-69: Language, Time/Date, Screen settings
    {70, 10, "System Settings 70-79"},    // 70-79: Work mode, LCD light, beep
    {80, 10, "System Settings 80-89"},    // 80-89: Gateway, country, plant, connection
    {90, 8, "System Settings 90-97"}      // 90-97: COM address, grid sell, master/slave
};

// Grid Protection Settings Ranges (185-200) - 16 registers
const RegisterRange DeyeInverter::SETTINGS_GRID_PROTECTION_RANGES[] = {
    {185, 8, "Grid Protection 185-192"},  // 185-192: Voltage protection limits
    {193, 8, "Grid Protection 193-200"}   // 193-200: Frequency protection limits
};

// Extended Settings Ranges (231-339) - 109 registers
const RegisterRange DeyeInverter::SETTINGS_EXTENDED_RANGES[] = {
    {231, 15, "Extended Settings 231-245"},   // 231-245: Inverter settings
    {246, 15, "Extended Settings 246-260"},   // 246-260: Protection settings
    {261, 15, "Extended Settings 261-275"},   // 261-275: Energy management
    {276, 15, "Extended Settings 276-290"},   // 276-290: Grid connection
    {291, 24, "Extended Settings 291-314"},   // 291-314: Advanced settings
    {315, 25, "Extended Settings 315-339"}    // 315-339: Reserved/extended
};

// California Compliance Settings Ranges (340-499) - 160 registers
const RegisterRange DeyeInverter::SETTINGS_CALIFORNIA_RANGES[] = {
    {340, 20, "California Settings 340-359"},   // 340-359: CA Rule 21 compliance
    {360, 20, "California Settings 360-379"},   // 360-379: Volt-watt curve
    {380, 20, "California Settings 380-399"},   // 380-399: Volt-var curve
    {400, 40, "California Settings 400-439"},   // 400-439: Frequency-watt curve
    {440, 30, "California Settings 440-469"},   // 440-469: Ride-through settings
    {470, 30, "California Settings 470-499"}    // 470-499: Reactive power control
};

// Battery Module Ranges (684-809) - 126 registers across 9 modules
// Each module: 14 registers (temp, voltage, current, SOC, SOH, cell voltages x8, status)
const RegisterRange DeyeInverter::BATTERY_MODULE_RANGES[] = {
    {684, 14, "Battery Module 1"},   // 684-697: Module 1 data
    {698, 14, "Battery Module 2"},   // 698-711: Module 2 data
    {712, 14, "Battery Module 3"},   // 712-725: Module 3 data
    {726, 14, "Battery Module 4"},   // 726-739: Module 4 data
    {740, 14, "Battery Module 5"},   // 740-753: Module 5 data
    {754, 14, "Battery Module 6"},   // 754-767: Module 6 data
    {768, 14, "Battery Module 7"},   // 768-781: Module 7 data
    {782, 14, "Battery Module 8"},   // 782-795: Module 8 data
    {796, 14, "Battery Module 9"}    // 796-809: Module 9 data
};

// Device info ranges (read once at startup, then every 5 minutes)
const RegisterRange DeyeInverter::DEVICE_INFO_RANGES[] = {
    {0, 2, "Device Info"},          // 0-1: Device Type & Modbus Address
    {3, 12, "Serial Number"},       // 3-14: Serial Number (12 registers as ASCII string)
    {20, 7, "Device Details"},      // 20-26: Rated power, protocol, etc.
    {27, 3, "Firmware Versions"},   // 27-29: Firmware main, DSP, ARM
    {40, 20, "Hardware Info"}       // 40-59: Hardware version, model info
};

// =============================================================================
// DATA TYPE HELPERS
// =============================================================================

DataType DeyeInverter::parse_data_type(const std::string& str) {
  if (str == "S_WORD") return DataType::S_WORD;
  if (str == "U_DWORD") return DataType::U_DWORD;
  if (str == "U_DWORD_R") return DataType::U_DWORD_R;
  if (str == "S_DWORD") return DataType::S_DWORD;
  if (str == "S_DWORD_R") return DataType::S_DWORD_R;
  if (str == "BITMASK") return DataType::BITMASK;
  return DataType::U_WORD;  // Default
}

float DeyeInverter::convert_value(uint16_t raw, DataType type, float scale, float offset) {
  float value;
  switch (type) {
    case DataType::S_WORD:
      // Handle signed 16-bit
      value = static_cast<float>(static_cast<int16_t>(raw));
      break;
    case DataType::U_WORD:
    case DataType::BITMASK:
    default:
      value = static_cast<float>(raw);
      break;
  }
  return (value * scale) + offset;
}

float DeyeInverter::convert_value_32(uint32_t raw, DataType type, float scale, float offset) {
  float value;
  switch (type) {
    case DataType::S_DWORD:
    case DataType::S_DWORD_R:
      // Handle signed 32-bit
      value = static_cast<float>(static_cast<int32_t>(raw));
      break;
    case DataType::U_DWORD:
    case DataType::U_DWORD_R:
    case DataType::U_WORD:
    case DataType::BITMASK:
    default:
      value = static_cast<float>(raw);
      break;
  }
  return (value * scale) + offset;
}

std::string DeyeInverter::format_time_point(uint16_t value) {
  // Format: 1000 -> "10:00"
  uint8_t hours = value / 100;
  uint8_t minutes = value % 100;
  char buffer[6];
  snprintf(buffer, sizeof(buffer), "%02d:%02d", hours, minutes);
  return std::string(buffer);
}

std::string DeyeInverter::format_version(uint16_t value) {
  // Format firmware/hardware version: 0x0102 -> "1.02"
  uint8_t major = (value >> 8) & 0xFF;
  uint8_t minor = value & 0xFF;
  char buffer[8];
  snprintf(buffer, sizeof(buffer), "%u.%02u", major, minor);
  return std::string(buffer);
}

std::string DeyeInverter::parse_firmware_version(const std::vector<uint8_t>& data, size_t offset) {
  if (offset + 2 > data.size()) return "0.00";
  uint16_t value = (data[offset] << 8) | data[offset + 1];
  return format_version(value);
}

// =============================================================================
// DEYE SENSOR IMPLEMENTATION
// =============================================================================
#ifdef USE_SENSOR

void DeyeSensor::update_value(uint16_t raw_value) {
  float converted = DeyeInverter::convert_value(raw_value, this->data_type_, this->scale_, this->offset_);
  this->publish_state(converted);
}

void DeyeSensor::update_value_32(uint32_t raw_value) {
  float converted = DeyeInverter::convert_value_32(raw_value, this->data_type_, this->scale_, this->offset_);
  this->publish_state(converted);
}

void DeyeSensor::update_value_signed(int16_t raw_value) {
  float converted = (static_cast<float>(raw_value) * this->scale_) + this->offset_;
  this->publish_state(converted);
}

void DeyeSensor::update_value_32_signed(int32_t raw_value) {
  float converted = (static_cast<float>(raw_value) * this->scale_) + this->offset_;
  this->publish_state(converted);
}
#endif

// =============================================================================
// DEYE BINARY SENSOR IMPLEMENTATION
// =============================================================================
#ifdef USE_BINARY_SENSOR

void DeyeBinarySensor::update_value(uint16_t raw_value) {
  bool state = (raw_value & this->bitmask_) != 0;
  this->publish_state(state);
}
#endif

// =============================================================================
// DEYE TEXT SENSOR IMPLEMENTATION
// =============================================================================
#ifdef USE_TEXT_SENSOR

void DeyeTextSensor::update_value(uint16_t raw_value) {
  if (this->is_status_) {
    // Map status code to string
    switch (raw_value) {
      case 0: this->publish_state("Standby"); break;
      case 1: this->publish_state("Self-Check"); break;
      case 2: this->publish_state("Normal"); break;
      case 3: this->publish_state("Alarm"); break;
      case 4: this->publish_state("Fault"); break;
      default: this->publish_state("Unknown"); break;
    }
  } else if (this->is_device_type_) {
    // Map device type code to string
    switch (raw_value) {
      case 0x0200: this->publish_state("String Inverter"); break;
      case 0x0300: this->publish_state("Single Phase Hybrid"); break;
      case 0x0400: this->publish_state("Micro Inverter"); break;
      case 0x0500: this->publish_state("Three Phase Hybrid"); break;
      default: this->publish_state("Unknown (" + std::to_string(raw_value) + ")"); break;
    }
  } else if (this->is_firmware_version_ || this->is_hardware_version_) {
    // Format version string
    this->publish_state(DeyeInverter::format_version(raw_value));
  } else if (this->is_time_point_) {
    // Format time point (1000 -> "10:00")
    this->publish_state(DeyeInverter::format_time_point(raw_value));
  } else if (!this->mapping_.empty()) {
    // Use custom mapping
    auto it = this->mapping_.find(raw_value);
    if (it != this->mapping_.end()) {
      this->publish_state(it->second);
    } else {
      this->publish_state("Unknown (" + std::to_string(raw_value) + ")");
    }
  } else {
    this->publish_state(std::to_string(raw_value));
  }
}

void DeyeTextSensor::update_string(const std::string& value) {
  this->publish_state(value);
}
#endif

// =============================================================================
// DEYE SWITCH IMPLEMENTATION
// =============================================================================
#ifdef USE_SWITCH

void DeyeSwitch::update_value(uint16_t raw_value) {
  if (this->is_2bit_field_) {
    // For 2-bit fields: extract the field value and check if it's enable (11) or disable (10)
    uint16_t field_value = (raw_value & this->bitmask_) >> this->bit_shift_;
    // 11 (0x03) = enable (ON), 10 (0x02) = disable (OFF), 00/01 = disabled (undefined)
    bool state = (field_value == 0x03);
    this->publish_state(state);
  } else {
    // Standard 1-bit field
    bool state = (raw_value & this->bitmask_) != 0;
    this->publish_state(state);
  }
}

void DeyeSwitch::write_state(bool state) {
  this->publish_state(state);
  
  if (this->parent_ != nullptr) {
    if (this->is_2bit_field_) {
      // For 2-bit fields: write the complete value (enable=11 or disable=10)
      uint16_t value = state ? this->value_enable_ : this->value_disable_;
      auto cmd = modbus_controller::ModbusCommandItem::create_write_single_command(
          this, this->address_, value);
      this->queue_command(cmd);
    } else {
      // Standard 1-bit field
      uint16_t value = state ? 0xFFFF : 0x0000;
      auto cmd = modbus_controller::ModbusCommandItem::create_write_single_command(
          this, this->address_, value);
      this->queue_command(cmd);
    }
  }
}
#endif

// =============================================================================
// DEYE NUMBER IMPLEMENTATION
// =============================================================================
#ifdef USE_NUMBER

void DeyeNumber::update_value(uint16_t raw_value) {
  float value;
  if (this->is_time_point_) {
    // For time points, store as-is (1000 = 10:00)
    value = static_cast<float>(raw_value);
  } else {
    value = static_cast<float>(raw_value) * this->scale_;
  }
  this->publish_state(value);
}

void DeyeNumber::control(float value) {
  this->publish_state(value);
  
  if (this->parent_ != nullptr) {
    uint16_t raw_value;
    if (this->is_time_point_) {
      // For time points, store as-is
      raw_value = static_cast<uint16_t>(value);
    } else {
      raw_value = static_cast<uint16_t>(value / this->scale_);
    }
    auto cmd = modbus_controller::ModbusCommandItem::create_write_single_command(
        this, this->address_, raw_value);
    this->queue_command(cmd);
  }
}
#endif

// =============================================================================
// DEYE SELECT IMPLEMENTATION
// =============================================================================
#ifdef USE_SELECT

void DeyeSelect::update_value(uint16_t raw_value) {
  auto it = this->options_map_.find(raw_value);
  if (it != this->options_map_.end()) {
    this->publish_state(it->second);
  } else {
    this->publish_state("Unknown (" + std::to_string(raw_value) + ")");
  }
}

void DeyeSelect::control(const std::string& value) {
  this->publish_state(value);
  
  if (this->parent_ != nullptr) {
    auto it = this->reverse_map_.find(value);
    if (it != this->reverse_map_.end()) {
      auto cmd = modbus_controller::ModbusCommandItem::create_write_single_command(
          this, this->address_, it->second);
      this->queue_command(cmd);
    }
  }
}
#endif

// =============================================================================
// DEYE DATETIME IMPLEMENTATION - For Time of Use start times
// =============================================================================
#ifdef USE_DATETIME

void DeyeDateTime::update_value(uint16_t raw_value) {
  // Parse HHMM format from register value (e.g., 1000 = 10:00)
  uint8_t hour, minute;
  parse_hhmm(raw_value, hour, minute);
  
  // Create time-only datetime (use epoch date 1970-01-01)
  auto now = ESPTime::from_epoch_utc(0);
  now.year = 1970;
  now.month = 1;
  now.day_of_month = 1;
  now.hour = hour;
  now.minute = minute;
  now.second = 0;
  now.recalc_timestamp_utc(false);
  
  this->set_datetime(now);
}

void DeyeDateTime::control(const datetime::DateTimeCall& call) {
  // Get the new time value
  auto time_opt = call.get_hour();
  if (!time_opt.has_value()) return;
  
  uint8_t hour = time_opt.value();
  uint8_t minute = call.get_minute().value_or(0);
  
  // Format to HHMM register value
  uint16_t hhmm_value = format_hhmm(hour, minute);
  
  // Update internal state
  auto now = ESPTime::from_epoch_utc(0);
  now.year = 1970;
  now.month = 1;
  now.day_of_month = 1;
  now.hour = hour;
  now.minute = minute;
  now.second = 0;
  now.recalc_timestamp_utc(false);
  this->set_datetime(now);
  
  // Write to Modbus register
  if (this->parent_ != nullptr) {
    auto cmd = modbus_controller::ModbusCommandItem::create_write_single_command(
        this, this->address_, hhmm_value);
    this->queue_command(cmd);
  }
}

void DeyeDateTime::parse_hhmm(uint16_t value, uint8_t& hour, uint8_t& minute) {
  // Format: 1000 -> hour=10, minute=0
  hour = value / 100;
  minute = value % 100;
  
  // Validate ranges
  if (hour > 23) hour = 23;
  if (minute > 59) minute = 59;
}

uint16_t DeyeDateTime::format_hhmm(uint8_t hour, uint8_t minute) {
  // Format: hour=10, minute=0 -> 1000
  // Validate ranges
  if (hour > 23) hour = 23;
  if (minute > 59) minute = 59;
  
  return (hour * 100) + minute;
}
#endif

// =============================================================================
// DEYE TIME IMPLEMENTATION - For System Time synchronization to inverter
// Only writes time when: local time was just set OR diff > max_diff seconds
// Triggered automatically when Settings are read (contains registers 62-64)
// =============================================================================
#ifdef USE_TIME

void DeyeTime::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Deye Time...");
}

void DeyeTime::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Time:");
  ESP_LOGCONFIG(TAG, "  Max Allowed Diff: %u ms", this->max_time_diff_);
}

void DeyeTime::sync_time_if_needed() {
  if (this->parent_ == nullptr) {
    ESP_LOGW(TAG, "No parent inverter set for time sync");
    return;
  }
  
  // Get current time from ESPHome's time source
  auto local_time = this->now();
  if (!local_time.is_valid()) {
    ESP_LOGW(TAG, "Current time is not valid, skipping inverter time sync");
    return;
  }
  
  bool should_sync = false;
  
  // Check 1: Time was just set (DST change, manual adjustment)
  if (this->time_just_set_) {
    ESP_LOGI(TAG, "Local time was just set, syncing to inverter");
    should_sync = true;
    this->time_just_set_ = false;
  }
  // Check 2: We have valid inverter time and difference is too large
  // (only if max_time_diff > 0, otherwise auto-sync is disabled)
  else if (this->inverter_time_valid_ && this->max_time_diff_ > 0) {
    // Calculate time difference in seconds
    int64_t diff_seconds = local_time.timestamp - this->inverter_time_.timestamp;
    if (diff_seconds < 0) diff_seconds = -diff_seconds;  // Absolute value
    
    if (diff_seconds * 1000 > this->max_time_diff_) {
      ESP_LOGI(TAG, "Time difference too large: %lld seconds, syncing to inverter", diff_seconds);
      should_sync = true;
    } else {
      ESP_LOGV(TAG, "Time difference within limits: %lld seconds", diff_seconds);
    }
  }
  // Check 3: We don't have inverter time yet (first run)
  else {
    ESP_LOGI(TAG, "No inverter time received yet, will sync when available");
    // Don't sync yet, wait for first inverter time reading
  }
  
  if (should_sync) {
    this->write_time_to_inverter();
  }
}

void DeyeTime::write_time_to_inverter() {
  if (this->parent_ == nullptr) {
    return;
  }
  
  // Get current time from ESPHome's time source
  auto now_time = this->now();
  if (!now_time.is_valid()) {
    ESP_LOGW(TAG, "Current time is not valid, cannot sync to inverter");
    return;
  }
  
  // Convert to inverter format (base year 2000)
  uint8_t year_offset = now_time.year - 2000;
  uint8_t month = now_time.month;
  uint8_t day = now_time.day_of_month;
  uint8_t hour = now_time.hour;
  uint8_t minute = now_time.minute;
  uint8_t second = now_time.second;
  
  // Validate values
  if (month < 1) month = 1;
  if (month > 12) month = 12;
  if (day < 1) day = 1;
  if (day > 31) day = 31;
  if (hour > 23) hour = 0;
  if (minute > 59) minute = 0;
  if (second > 59) second = 0;
  
  // Pack into registers
  // Register 62: YY (high byte), MM (low byte)
  uint16_t reg62 = (static_cast<uint16_t>(year_offset) << 8) | month;
  // Register 63: DD (high byte), HH (low byte)
  uint16_t reg63 = (static_cast<uint16_t>(day) << 8) | hour;
  // Register 64: mm (high byte), ss (low byte)
  uint16_t reg64 = (static_cast<uint16_t>(minute) << 8) | second;
  
  // Write to inverter
  auto cmd62 = modbus_controller::ModbusCommandItem::create_write_single_command(
      this, 62, reg62);
  this->queue_command(cmd62);
  
  auto cmd63 = modbus_controller::ModbusCommandItem::create_write_single_command(
      this, 63, reg63);
  this->queue_command(cmd63);
  
  auto cmd64 = modbus_controller::ModbusCommandItem::create_write_single_command(
      this, 64, reg64);
  this->queue_command(cmd64);
  
  ESP_LOGI(TAG, "System time written to inverter: %04d-%02d-%02d %02d:%02d:%02d",
           now_time.year, now_time.month, now_time.day_of_month,
           now_time.hour, now_time.minute, now_time.second);
  
  // Update cached inverter time to prevent immediate re-sync
  this->inverter_time_ = now_time;
  this->inverter_time_valid_ = true;
}

void DeyeTime::on_system_time_received(uint8_t year, uint8_t month, uint8_t day,
                                       uint8_t hour, uint8_t minute, uint8_t second) {
  // Validate values
  if (month < 1 || month > 12 || day < 1 || day > 31 || hour > 23 || minute > 59 || second > 59) {
    ESP_LOGW(TAG, "Invalid inverter time received: %02d-%02d-%02d %02d:%02d:%02d",
             year, month, day, hour, minute, second);
    this->inverter_time_valid_ = false;
    return;
  }
  
  // Store inverter time
  this->inverter_time_ = ESPTime::from_epoch_utc(0);
  this->inverter_time_.year = 2000 + year;
  this->inverter_time_.month = month;
  this->inverter_time_.day_of_month = day;
  this->inverter_time_.hour = hour;
  this->inverter_time_.minute = minute;
  this->inverter_time_.second = second;
  this->inverter_time_.recalc_timestamp_utc(false);
  this->inverter_time_valid_ = true;
  
  ESP_LOGD(TAG, "Inverter time received: %04d-%02d-%02d %02d:%02d:%02d",
           this->inverter_time_.year, month, day, hour, minute, second);
  
  // Immediately check if sync is needed
  this->sync_time_if_needed();
}
#endif

// =============================================================================
// DEYE INVERTER SETUP
// =============================================================================

void DeyeInverter::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Deye Inverter...");
  
  // Set the Modbus address for this device
  this->set_address(this->address_);
  
  // Request device info at startup
  this->update_device_info();
}

void DeyeInverter::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Inverter:");
  ESP_LOGCONFIG(TAG, "  Name: %s", this->name_.c_str());
  ESP_LOGCONFIG(TAG, "  Address: 0x%02X", this->address_);
  ESP_LOGCONFIG(TAG, "  Live Update Interval: %u ms", this->interval_live_);
  ESP_LOGCONFIG(TAG, "  Stats Update Interval: %u ms", this->interval_statistics_);
  ESP_LOGCONFIG(TAG, "  Settings Update Interval: %u ms", this->interval_settings_);
  ESP_LOGCONFIG(TAG, "  System Settings Update Interval: %u ms", this->interval_system_settings_);
  ESP_LOGCONFIG(TAG, "  Grid Protection Update Interval: %u ms", this->interval_grid_protection_);
  ESP_LOGCONFIG(TAG, "  Extended Settings Update Interval: %u ms", this->interval_extended_settings_);
  ESP_LOGCONFIG(TAG, "  California Settings Update Interval: %u ms", this->interval_california_settings_);
  ESP_LOGCONFIG(TAG, "  Battery Module Update Interval: %u ms", this->interval_battery_modules_);
  ESP_LOGCONFIG(TAG, "  Device Info Update Interval: %u ms", this->interval_device_info_);
#ifdef USE_SENSOR
  ESP_LOGCONFIG(TAG, "  Sensors: %u", this->sensors_.size());
#endif
#ifdef USE_BINARY_SENSOR
  ESP_LOGCONFIG(TAG, "  Binary Sensors: %u", this->binary_sensors_.size());
#endif
#ifdef USE_TEXT_SENSOR
  ESP_LOGCONFIG(TAG, "  Text Sensors: %u", this->text_sensors_.size());
#endif
#ifdef USE_SWITCH
  ESP_LOGCONFIG(TAG, "  Switches: %u", this->switches_.size());
#endif
#ifdef USE_NUMBER
  ESP_LOGCONFIG(TAG, "  Numbers: %u", this->numbers_.size());
#endif
#ifdef USE_SELECT
  ESP_LOGCONFIG(TAG, "  Selects: %u", this->selects_.size());
#endif
#ifdef USE_DATETIME
  ESP_LOGCONFIG(TAG, "  DateTimes: %u", this->datetimes_.size());
#endif
#ifdef USE_TIME
  ESP_LOGCONFIG(TAG, "  Times: %u", this->times_.size());
#endif
}

// =============================================================================
// MAIN LOOP - Complete Update Cycle
// =============================================================================

void DeyeInverter::loop() {
  const uint32_t now = millis();
  
  // Check if we need to update live data (1s interval)
  if (now - this->last_live_update_ >= this->interval_live_) {
    this->last_live_update_ = now;
    this->update_live_data();
  }
  
  // Check if we need to update statistics (5s interval)
  if (now - this->last_stats_update_ >= this->interval_statistics_) {
    this->last_stats_update_ = now;
    this->update_statistics();
  }
  
  // Check if we need to update battery modules (5s interval)
  if (now - this->last_battery_modules_update_ >= this->interval_battery_modules_) {
    this->last_battery_modules_update_ = now;
    this->update_battery_modules();
  }
  
  // Check if we need to update settings (60s interval)
  if (now - this->last_settings_update_ >= this->interval_settings_) {
    this->last_settings_update_ = now;
    this->update_settings();
  }
  
  // Check if we need to update system settings (2 min interval)
  if (now - this->last_system_settings_update_ >= this->interval_system_settings_) {
    this->last_system_settings_update_ = now;
    this->update_system_settings();
  }
  
  // Check if we need to update grid protection settings (2 min interval)
  if (now - this->last_grid_protection_update_ >= this->interval_grid_protection_) {
    this->last_grid_protection_update_ = now;
    this->update_grid_protection();
  }
  
  // Check if we need to update extended settings (2 min interval)
  if (now - this->last_extended_settings_update_ >= this->interval_extended_settings_) {
    this->last_extended_settings_update_ = now;
    this->update_extended_settings();
  }
  
  // Check if we need to update California compliance settings (5 min interval)
  if (now - this->last_california_settings_update_ >= this->interval_california_settings_) {
    this->last_california_settings_update_ = now;
    this->update_california_settings();
  }
  
  // Check if we need to update device info (5 min interval, or once at startup)
  if (!this->device_info_initialized_ || 
      (now - this->last_device_info_update_ >= this->interval_device_info_)) {
    this->last_device_info_update_ = now;
    this->update_device_info();
  }
}

// =============================================================================
// UPDATE METHODS
// =============================================================================

void DeyeInverter::update_live_data() {
  // Cycle through live data ranges one at a time to avoid overloading the bus
  if (this->current_phase_ == UpdatePhase::IDLE || 
      this->current_phase_ == UpdatePhase::LIVE_DATA) {
    this->current_phase_ = UpdatePhase::LIVE_DATA;
    
    if (this->current_range_index_ < LIVE_RANGES_COUNT) {
      this->update_register_range(LIVE_RANGES[this->current_range_index_]);
      this->current_range_index_++;
    } else {
      // Reset for next cycle
      this->current_range_index_ = 0;
      this->current_phase_ = UpdatePhase::IDLE;
    }
  }
}

void DeyeInverter::update_statistics() {
  if (this->current_phase_ == UpdatePhase::IDLE) {
    this->current_phase_ = UpdatePhase::STATISTICS;
    
    // Request all statistics ranges
    for (size_t i = 0; i < STATS_RANGES_COUNT; i++) {
      this->update_register_range(STATS_RANGES[i]);
      // Small delay between requests to avoid flooding
      delay(10);
    }
    
    this->current_phase_ = UpdatePhase::IDLE;
  }
}

void DeyeInverter::update_battery_modules() {
  // Cycle through battery module ranges
  if (this->current_phase_ == UpdatePhase::IDLE || 
      this->current_phase_ == UpdatePhase::BATTERY_MODULES) {
    this->current_phase_ = UpdatePhase::BATTERY_MODULES;
    
    if (this->current_battery_module_range_ < BATTERY_MODULE_RANGES_COUNT) {
      this->update_register_range(BATTERY_MODULE_RANGES[this->current_battery_module_range_]);
      this->current_battery_module_range_++;
    } else {
      // Reset for next cycle
      this->current_battery_module_range_ = 0;
      this->current_phase_ = UpdatePhase::IDLE;
    }
  }
}

void DeyeInverter::update_settings() {
  if (this->current_phase_ == UpdatePhase::IDLE) {
    this->current_phase_ = UpdatePhase::SETTINGS;
    
    ESP_LOGD(TAG, "Reading settings...");
    
    // Read all settings ranges
    for (size_t i = 0; i < SETTINGS_RANGES_COUNT; i++) {
      this->update_register_range(SETTINGS_RANGES[i]);
      delay(10);
    }
    
    this->current_phase_ = UpdatePhase::IDLE;
  }
}

void DeyeInverter::update_system_settings() {
  if (this->current_phase_ == UpdatePhase::IDLE) {
    this->current_phase_ = UpdatePhase::SYSTEM_SETTINGS;
    
    ESP_LOGD(TAG, "Reading system settings...");
    
    for (size_t i = 0; i < SETTINGS_SYSTEM_RANGES_COUNT; i++) {
      this->update_register_range(SETTINGS_SYSTEM_RANGES[i]);
      delay(10);
    }
    
    this->current_phase_ = UpdatePhase::IDLE;
  }
}

void DeyeInverter::update_grid_protection() {
  if (this->current_phase_ == UpdatePhase::IDLE) {
    this->current_phase_ = UpdatePhase::GRID_PROTECTION;
    
    ESP_LOGD(TAG, "Reading grid protection settings...");
    
    for (size_t i = 0; i < SETTINGS_GRID_PROTECTION_RANGES_COUNT; i++) {
      this->update_register_range(SETTINGS_GRID_PROTECTION_RANGES[i]);
      delay(10);
    }
    
    this->current_phase_ = UpdatePhase::IDLE;
  }
}

void DeyeInverter::update_extended_settings() {
  if (this->current_phase_ == UpdatePhase::IDLE) {
    this->current_phase_ = UpdatePhase::EXTENDED_SETTINGS;
    
    ESP_LOGD(TAG, "Reading extended settings...");
    
    for (size_t i = 0; i < SETTINGS_EXTENDED_RANGES_COUNT; i++) {
      this->update_register_range(SETTINGS_EXTENDED_RANGES[i]);
      delay(10);
    }
    
    this->current_phase_ = UpdatePhase::IDLE;
  }
}

void DeyeInverter::update_california_settings() {
  if (this->current_phase_ == UpdatePhase::IDLE) {
    this->current_phase_ = UpdatePhase::CALIFORNIA_SETTINGS;
    
    ESP_LOGD(TAG, "Reading California compliance settings...");
    
    for (size_t i = 0; i < SETTINGS_CALIFORNIA_RANGES_COUNT; i++) {
      this->update_register_range(SETTINGS_CALIFORNIA_RANGES[i]);
      delay(10);
    }
    
    this->current_phase_ = UpdatePhase::IDLE;
  }
}

void DeyeInverter::update_device_info() {
  ESP_LOGD(TAG, "Reading device info...");
  
  // Read all device info ranges
  for (size_t i = 0; i < DEVICE_INFO_RANGES_COUNT; i++) {
    this->update_register_range(DEVICE_INFO_RANGES[i]);
    delay(10);
  }
  
  this->device_info_initialized_ = true;
}

void DeyeInverter::update_register_range(const RegisterRange& range) {
  ESP_LOGV(TAG, "Reading register range '%s' (0x%04X, %u registers)", 
           range.name, range.start, range.count);
  
  auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
      this, modbus_controller::ModbusRegisterType::HOLDING, 
      range.start, range.count);
  cmd.on_data_func = [this](modbus_controller::ModbusRegisterType rt, 
                            uint16_t addr, const std::vector<uint8_t> &data) {
    this->on_modbus_data(data);
  };
  this->queue_command(cmd);
}

// =============================================================================
// MODBUS CALLBACKS
// =============================================================================

void DeyeInverter::on_modbus_data(const std::vector<uint8_t>& data) {
  if (data.size() < 4) {
    ESP_LOGW(TAG, "Received invalid data (too short: %u bytes)", data.size());
    return;
  }
  
  // The first 2 bytes contain the starting register address (big-endian)
  uint16_t start_address = (data[0] << 8) | data[1];
  
  // Remaining bytes are the register data
  std::vector<uint8_t> reg_data(data.begin() + 2, data.end());
  
  ESP_LOGV(TAG, "Received %u bytes for register 0x%04X", reg_data.size(), start_address);
  
  // Check if this is device info data (serial number, firmware, etc.)
  if (start_address >= 3 && start_address <= 14) {
    // Serial number range
#ifdef USE_TEXT_SENSOR
    this->update_serial_number_from_data(start_address, reg_data);
#endif
  } else if (start_address >= 27 && start_address <= 29) {
    // Firmware version range
#ifdef USE_TEXT_SENSOR
    this->update_firmware_info_from_data(start_address, reg_data);
#endif
  } else if (start_address >= 684 && start_address <= 809) {
    // Battery module data
#ifdef USE_SENSOR
    this->update_battery_module_sensors(start_address, reg_data);
#endif
  } else if (start_address <= 62 && start_address + (reg_data.size() / 2) > 62) {
    // System time data (registers 62-64)
#ifdef USE_TIME
    this->update_system_time_from_data(start_address, reg_data);
#endif
  }
  
  // Update all entity types
#ifdef USE_SENSOR
  this->update_sensors_from_data(start_address, reg_data);
#endif
#ifdef USE_BINARY_SENSOR
  this->update_binary_sensors_from_data(start_address, reg_data);
#endif
#ifdef USE_TEXT_SENSOR
  this->update_text_sensors_from_data(start_address, reg_data);
#endif
#ifdef USE_SWITCH
  this->update_switches_from_data(start_address, reg_data);
#endif
#ifdef USE_NUMBER
  this->update_numbers_from_data(start_address, reg_data);
#endif
#ifdef USE_SELECT
  this->update_selects_from_data(start_address, reg_data);
#endif
#ifdef USE_DATETIME
  this->update_datetimes_from_data(start_address, reg_data);
#endif
}

void DeyeInverter::on_modbus_error(uint8_t function_code, uint8_t exception_code) {
  ESP_LOGW(TAG, "Modbus error - Function: 0x%02X, Exception: 0x%02X (%s)", 
           function_code, exception_code,
           exception_code == 0x01 ? "Illegal Function" :
           exception_code == 0x02 ? "Illegal Data Address" :
           exception_code == 0x03 ? "Illegal Data Value" :
           exception_code == 0x04 ? "Server Device Failure" :
           "Unknown");
}

// =============================================================================
// BATTERY MODULE PARSING
// =============================================================================

#ifdef USE_SENSOR
void DeyeInverter::update_battery_module_sensors(uint16_t start_address, const std::vector<uint8_t>& data) {
  // Determine which battery module this data belongs to
  uint8_t module_index = 0;
  if (start_address >= 684 && start_address <= 697) module_index = 0;
  else if (start_address >= 698 && start_address <= 711) module_index = 1;
  else if (start_address >= 712 && start_address <= 725) module_index = 2;
  else if (start_address >= 726 && start_address <= 739) module_index = 3;
  else if (start_address >= 740 && start_address <= 753) module_index = 4;
  else if (start_address >= 754 && start_address <= 767) module_index = 5;
  else if (start_address >= 768 && start_address <= 781) module_index = 6;
  else if (start_address >= 782 && start_address <= 795) module_index = 7;
  else if (start_address >= 796 && start_address <= 809) module_index = 8;
  
  // Update sensors that belong to this module
  for (auto *sensor : this->sensors_) {
    if (sensor->get_is_battery_module() && sensor->get_module_index() == module_index) {
      uint16_t sensor_addr = sensor->get_address();
      
      if (sensor_addr >= start_address && sensor_addr < start_address + (data.size() / 2)) {
        size_t offset = (sensor_addr - start_address) * 2;
        
        if (offset + 2 <= data.size()) {
          uint16_t raw_value = this->parse_uint16(data, offset);
          
          if (sensor->get_is_cell_voltage()) {
            // Cell voltage sensors use specific offset calculation
            uint8_t cell_idx = sensor->get_cell_index();
            if (cell_idx < 8) {
              size_t cell_offset = 4 + (cell_idx * 2);  // First 4 bytes are temp/voltage
              if (cell_offset + 2 <= data.size()) {
                uint16_t cell_value = this->parse_uint16(data, cell_offset);
                sensor->update_value(cell_value);
              }
            }
          } else {
            sensor->update_value(raw_value);
          }
        }
      }
    }
  }
}
#endif

float DeyeInverter::parse_battery_module_value(const std::vector<uint8_t>& data, size_t offset, 
                                                uint8_t module_index, uint8_t cell_index, 
                                                bool is_cell_voltage) {
  if (is_cell_voltage && cell_index < 8) {
    // Cell voltages start at offset 4 (after temp, voltage, current, SOC)
    size_t cell_offset = 4 + (cell_index * 2);
    if (cell_offset + 2 <= data.size()) {
      return static_cast<float>(this->parse_uint16(data, cell_offset));
    }
  } else if (offset + 2 <= data.size()) {
    return static_cast<float>(this->parse_uint16(data, offset));
  }
  return 0.0f;
}

// =============================================================================
// SERIAL NUMBER AND FIRMWARE PARSING
// =============================================================================

#ifdef USE_TEXT_SENSOR
void DeyeInverter::update_serial_number_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  // Serial number is stored at registers 3-14 (12 registers = 24 bytes)
  if (start_address > 14) return;  // Not serial number data
  
  for (auto *sensor : this->text_sensors_) {
    if (sensor->get_is_serial_number()) {
      std::string serial = this->parse_string(data, 0, data.size());
      sensor->update_string(serial);
    }
  }
}
#endif

#ifdef USE_TEXT_SENSOR
void DeyeInverter::update_firmware_info_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  // Firmware info is at registers 27-29
  if (start_address < 27 || start_address > 29) return;
  
  for (auto *sensor : this->text_sensors_) {
    if (sensor->get_is_firmware_version() || sensor->get_is_hardware_version()) {
      uint16_t addr = sensor->get_address();
      if (addr >= start_address && addr < start_address + (data.size() / 2)) {
        size_t offset = (addr - start_address) * 2;
        if (offset + 2 <= data.size()) {
          uint16_t raw_value = this->parse_uint16(data, offset);
          sensor->update_value(raw_value);
        }
      }
    }
  }
}
#endif

// =============================================================================
// SENSOR UPDATE METHODS
// =============================================================================

#ifdef USE_SENSOR
void DeyeInverter::update_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *sensor : this->sensors_) {
    // Skip battery module sensors (handled separately)
    if (sensor->get_is_battery_module()) continue;
    
    uint16_t sensor_addr = sensor->get_address();
    
    // Check if this sensor's register is within the received data range
    if (sensor_addr >= start_address && 
        sensor_addr < start_address + (data.size() / 2)) {
      size_t offset = (sensor_addr - start_address) * 2;
      
      if (offset + sensor->get_bytes() <= data.size()) {
        if (sensor->get_bytes() == 4) {
          // 32-bit value - check data type for byte order
          DataType dtype = sensor->get_data_type();
          bool reversed = (dtype == DataType::U_DWORD_R || dtype == DataType::S_DWORD_R);
          bool is_signed = (dtype == DataType::S_DWORD || dtype == DataType::S_DWORD_R);
          
          if (is_signed) {
            int32_t raw_value = this->parse_int32_value(data, offset, reversed);
            sensor->update_value_32_signed(raw_value);
          } else {
            uint32_t raw_value = this->parse_uint32(data, offset, reversed);
            sensor->update_value_32(raw_value);
          }
        } else {
          // 16-bit value (default)
          DataType dtype = sensor->get_data_type();
          if (dtype == DataType::S_WORD) {
            int16_t raw_value = this->parse_int16_value(data, offset);
            sensor->update_value_signed(raw_value);
          } else {
            uint16_t raw_value = this->parse_uint16(data, offset);
            sensor->update_value(raw_value);
          }
        }
      }
    }
  }
}
#endif

#ifdef USE_BINARY_SENSOR
void DeyeInverter::update_binary_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *sensor : this->binary_sensors_) {
    uint16_t sensor_addr = sensor->get_address();
    
    if (sensor_addr >= start_address && sensor_addr < start_address + (data.size() / 2)) {
      size_t offset = (sensor_addr - start_address) * 2;
      
      if (offset + 2 <= data.size()) {
        uint16_t reg_value = this->parse_uint16(data, offset);
        sensor->update_value(reg_value);
      }
    }
  }
}
#endif

#ifdef USE_TEXT_SENSOR
void DeyeInverter::update_text_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *sensor : this->text_sensors_) {
    // Skip special text sensors that are handled separately
    if (sensor->get_is_serial_number()) continue;
    if (sensor->get_is_firmware_version() || sensor->get_is_hardware_version()) continue;
    
    uint16_t sensor_start = sensor->get_address();
    uint8_t sensor_count = sensor->get_register_count();
    
    if (sensor_start >= start_address && 
        sensor_start + sensor_count <= start_address + (data.size() / 2)) {
      size_t offset = (sensor_start - start_address) * 2;
      size_t length = sensor_count * 2;
      
      if (offset + length <= data.size()) {
        if (sensor->get_is_time_point() || sensor->get_is_status() || sensor->get_is_device_type()) {
          // Single register value-based text sensors
          uint16_t raw_value = this->parse_uint16(data, offset);
          sensor->update_value(raw_value);
        } else {
          // String-based text sensors (like serial number)
          std::string value = this->parse_string(data, offset, length);
          sensor->update_string(value);
        }
      }
    }
  }
}
#endif

#ifdef USE_SWITCH
void DeyeInverter::update_switches_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *sw : this->switches_) {
    uint16_t sw_addr = sw->get_address();

    if (sw_addr >= start_address && sw_addr < start_address + (data.size() / 2)) {
      size_t offset = (sw_addr - start_address) * 2;

      if (offset + 2 <= data.size()) {
        uint16_t reg_value = this->parse_uint16(data, offset);
        sw->update_value(reg_value);
      }
    }
  }
}
#endif

#ifdef USE_NUMBER
void DeyeInverter::update_numbers_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *num : this->numbers_) {
    uint16_t num_addr = num->get_address();

    if (num_addr >= start_address && num_addr < start_address + (data.size() / 2)) {
      size_t offset = (num_addr - start_address) * 2;

      if (offset + 2 <= data.size()) {
        uint16_t reg_value = this->parse_uint16(data, offset);
        num->update_value(reg_value);
      }
    }
  }
}
#endif

#ifdef USE_SELECT
void DeyeInverter::update_selects_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *sel : this->selects_) {
    uint16_t sel_addr = sel->get_address();

    if (sel_addr >= start_address && sel_addr < start_address + (data.size() / 2)) {
      size_t offset = (sel_addr - start_address) * 2;

      if (offset + 2 <= data.size()) {
        uint16_t reg_value = this->parse_uint16(data, offset);
        sel->update_value(reg_value);
      }
    }
  }
}
#endif

#ifdef USE_DATETIME
void DeyeInverter::update_datetimes_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *dt : this->datetimes_) {
    uint16_t dt_addr = dt->get_address();

    if (dt_addr >= start_address && dt_addr < start_address + (data.size() / 2)) {
      size_t offset = (dt_addr - start_address) * 2;

      if (offset + 2 <= data.size()) {
        uint16_t reg_value = this->parse_uint16(data, offset);
        dt->update_value(reg_value);
      }
    }
  }
}
#endif

#ifdef USE_TIME
void DeyeInverter::update_system_time_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  // Check if we have data for register 62 (need at least 6 bytes for full datetime)
  if (start_address > 62 || data.size() < 6) {
    return;
  }
  
  // Calculate offset to register 62 within the data
  size_t offset62 = (62 - start_address) * 2;
  if (offset62 + 6 > data.size()) {
    return;
  }
  
  // Parse 6 bytes: YY, MM, DD, HH, mm, ss
  // Register 62: YY (high byte), MM (low byte)
  uint16_t reg62 = (data[offset62] << 8) | data[offset62 + 1];
  uint8_t year = data[offset62];      // YY from register 62 high byte
  uint8_t month = data[offset62 + 1]; // MM from register 62 low byte
  
  // Register 63: DD (high byte), HH (low byte)
  uint8_t day = data[offset62 + 2];   // DD from register 63 high byte
  uint8_t hour = data[offset62 + 3];  // HH from register 63 low byte
  
  // Register 64: mm (high byte), ss (low byte)
  uint8_t minute = data[offset62 + 4]; // mm from register 64 high byte
  uint8_t second = data[offset62 + 5]; // ss from register 64 low byte
  
  ESP_LOGD(TAG, "Inverter system time: %02d-%02d-%02d %02d:%02d:%02d",
           year, month, day, hour, minute, second);
  
  // Notify all time entities
  for (auto *tm : this->times_) {
    tm->on_system_time_received(year, month, day, hour, minute, second);
  }
}
#endif

// =============================================================================
// DATA PARSING HELPERS
// =============================================================================

float DeyeInverter::parse_value(const std::vector<uint8_t>& data, size_t offset,
                                uint8_t bytes, DataType data_type, float scale, float offset_val) {
  float raw_value = 0.0f;
  
  if (bytes == 4) {
    // 32-bit value
    bool reversed = (data_type == DataType::U_DWORD_R || data_type == DataType::S_DWORD_R);
    bool is_signed = (data_type == DataType::S_DWORD || data_type == DataType::S_DWORD_R);
    
    if (is_signed) {
      int32_t val32 = this->parse_int32_value(data, offset, reversed);
      raw_value = static_cast<float>(val32);
    } else {
      uint32_t val32 = this->parse_uint32(data, offset, reversed);
      raw_value = static_cast<float>(val32);
    }
  } else {
    // 16-bit value (default)
    if (data_type == DataType::S_WORD) {
      int16_t val16 = this->parse_int16_value(data, offset);
      raw_value = static_cast<float>(val16);
    } else {
      uint16_t val16 = this->parse_uint16(data, offset);
      raw_value = static_cast<float>(val16);
    }
  }
  
  // Apply scale and offset
  return (raw_value * scale) + offset_val;
}

int16_t DeyeInverter::parse_int16_value(const std::vector<uint8_t>& data, size_t offset) {
  if (offset + 2 > data.size()) return 0;
  
  uint16_t value = (data[offset] << 8) | data[offset + 1];
  return static_cast<int16_t>(value);
}

int32_t DeyeInverter::parse_int32_value(const std::vector<uint8_t>& data, size_t offset, bool reversed) {
  if (offset + 4 > data.size()) return 0;
  
  uint32_t value;
  if (reversed) {
    // Low-high order
    value = (static_cast<uint32_t>(data[offset + 2]) << 24) |
            (static_cast<uint32_t>(data[offset + 3]) << 16) |
            (static_cast<uint32_t>(data[offset]) << 8) |
            static_cast<uint32_t>(data[offset + 1]);
  } else {
    // High-low order (standard Modbus)
    value = (static_cast<uint32_t>(data[offset]) << 24) |
            (static_cast<uint32_t>(data[offset + 1]) << 16) |
            (static_cast<uint32_t>(data[offset + 2]) << 8) |
            static_cast<uint32_t>(data[offset + 3]);
  }
  
  return static_cast<int32_t>(value);
}

uint32_t DeyeInverter::parse_uint32(const std::vector<uint8_t>& data, size_t offset, bool reversed) {
  if (offset + 4 > data.size()) return 0;
  
  uint32_t value;
  if (reversed) {
    // U_DWORD_R: low-high order (registers are [low, high])
    value = (static_cast<uint32_t>(data[offset + 2]) << 24) |
            (static_cast<uint32_t>(data[offset + 3]) << 16) |
            (static_cast<uint32_t>(data[offset]) << 8) |
            static_cast<uint32_t>(data[offset + 1]);
  } else {
    // U_DWORD: high-low order (standard Modbus)
    value = (static_cast<uint32_t>(data[offset]) << 24) |
            (static_cast<uint32_t>(data[offset + 1]) << 16) |
            (static_cast<uint32_t>(data[offset + 2]) << 8) |
            static_cast<uint32_t>(data[offset + 3]);
  }
  
  return value;
}

int32_t DeyeInverter::parse_int32(const std::vector<uint8_t>& data, size_t offset, bool is_signed) {
  if (offset + 4 > data.size()) return 0;
  
  // Modbus uses big-endian format
  uint32_t value = (static_cast<uint32_t>(data[offset]) << 24) |
                   (static_cast<uint32_t>(data[offset + 1]) << 16) |
                   (static_cast<uint32_t>(data[offset + 2]) << 8) |
                   static_cast<uint32_t>(data[offset + 3]);
  
  if (is_signed && (value & 0x80000000)) {
    // Handle negative value
    return static_cast<int32_t>(value | 0xFFFFFFFF00000000ULL);
  }
  
  return static_cast<int32_t>(value);
}

int16_t DeyeInverter::parse_int16(const std::vector<uint8_t>& data, size_t offset, bool is_signed) {
  if (offset + 2 > data.size()) return 0;
  
  uint16_t value = (data[offset] << 8) | data[offset + 1];
  
  if (is_signed && (value & 0x8000)) {
    // Handle negative value
    return static_cast<int16_t>(value | 0xFFFF0000);
  }
  
  return static_cast<int16_t>(value);
}

uint16_t DeyeInverter::parse_uint16(const std::vector<uint8_t>& data, size_t offset) {
  if (offset + 2 > data.size()) return 0;
  return (data[offset] << 8) | data[offset + 1];
}

std::string DeyeInverter::parse_string(const std::vector<uint8_t>& data, size_t offset, size_t length) {
  if (offset + length > data.size()) return "";
  
  std::string result;
  result.reserve(length);
  
  // Modbus strings are typically stored as 2 characters per register (big-endian)
  for (size_t i = offset; i < offset + length && i < data.size(); i += 2) {
    char high_byte = data[i];
    char low_byte = (i + 1 < data.size()) ? data[i + 1] : 0;
    
    // Skip null terminators and non-printable characters
    if (high_byte >= 32 && high_byte < 127) result += high_byte;
    if (low_byte >= 32 && low_byte < 127) result += low_byte;
  }
  
  return result;
}

// =============================================================================
// WRITE METHODS
// =============================================================================

void DeyeInverter::write_register(uint16_t address, uint16_t value) {
  ESP_LOGD(TAG, "Writing register 0x%04X = 0x%04X", address, value);
  
  auto cmd = modbus_controller::ModbusCommandItem::create_write_single_command(
      this, address, value);
  this->queue_command(cmd);
}

void DeyeInverter::write_register_masked(uint16_t address, uint16_t value, uint16_t mask) {
  ESP_LOGD(TAG, "Writing register 0x%04X with mask 0x%04X = 0x%04X", address, mask, value);
  
  auto cmd = modbus_controller::ModbusCommandItem::create_write_single_command(
      this, address, value & mask);
  this->queue_command(cmd);
}

}  // namespace deye_inverter
}  // namespace esphome
