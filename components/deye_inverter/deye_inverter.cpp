#include "deye_inverter.h"
#include "esphome/core/log.h"

namespace esphome {
namespace deye_inverter {

static const char *const TAG = "deye_inverter";

// =============================================================================
// STATIC REGISTER RANGE DEFINITIONS
// =============================================================================

const RegisterRange DeyeInverter::LIVE_RANGES[] = {
    {212, 7, "DC Extended"},
    {500, 1, "Running Status"},
    {548, 38, "Comm Status"},
    {540, 8, "Temperatures"},
    {586, 12, "Battery Live"},
    {598, 15, "Grid Port Live"},
    {613, 14, "Grid Meter Live"},
    {627, 13, "Inverter Output Live"},
    {640, 4, "UPS Load Live"},
    {644, 17, "Load Port Live"},
    {661, 11, "Generator Port Live"},
    {672, 12, "PV Live"}
};

const RegisterRange DeyeInverter::STATS_RANGES[] = {
    {501, 14, "Daily Stats"},
    {514, 6, "Battery Stats"},
    {520, 10, "Grid Stats"},
    {529, 11, "PV Stats"}
};

const RegisterRange DeyeInverter::SETTINGS_RANGES[] = {
    {98, 23, "Battery Settings 1"},
    {121, 7, "Generator Settings 1"},
    {128, 20, "Grid Settings"},
    {148, 6, "Time Point Start"},
    {154, 6, "Time Point Power"},
    {160, 6, "Time Point Voltage"},
    {166, 6, "Time Point Capacity"},
    {172, 6, "Time Point Charge"},
    {178, 7, "Special Functions"},
    {201, 22, "Battery Settings 2"},
    {223, 8, "Generator Settings 2"},
    {340, 1, "Solar Settings"}
};

const RegisterRange DeyeInverter::SETTINGS_SYSTEM_RANGES[] = {
    {60, 10, "System Settings 60-69"},
    {70, 10, "System Settings 70-79"},
    {80, 10, "System Settings 80-89"},
    {90, 8, "System Settings 90-97"}
};

const RegisterRange DeyeInverter::SETTINGS_GRID_PROTECTION_RANGES[] = {
    {185, 8, "Grid Protection 185-192"},
    {193, 8, "Grid Protection 193-200"}
};

const RegisterRange DeyeInverter::SETTINGS_EXTENDED_RANGES[] = {
    {231, 15, "Extended Settings 231-245"},
    {246, 15, "Extended Settings 246-260"},
    {261, 15, "Extended Settings 261-275"},
    {276, 15, "Extended Settings 276-290"},
    {291, 24, "Extended Settings 291-314"},
    {315, 25, "Extended Settings 315-339"}
};

const RegisterRange DeyeInverter::SETTINGS_CALIFORNIA_RANGES[] = {
    {340, 20, "California Settings 340-359"},
    {360, 20, "California Settings 360-379"},
    {380, 20, "California Settings 380-399"},
    {400, 40, "California Settings 400-439"},
    {440, 30, "California Settings 440-469"},
    {470, 30, "California Settings 470-499"}
};

const RegisterRange DeyeInverter::BATTERY_MODULE_RANGES[] = {
    {684, 14, "Battery Module 1"},
    {698, 14, "Battery Module 2"},
    {712, 14, "Battery Module 3"},
    {726, 14, "Battery Module 4"},
    {740, 14, "Battery Module 5"},
    {754, 14, "Battery Module 6"},
    {768, 14, "Battery Module 7"},
    {782, 14, "Battery Module 8"},
    {796, 14, "Battery Module 9"}
};

const RegisterRange DeyeInverter::DEVICE_INFO_RANGES[] = {
    {0, 2, "Device Info"},
    {3, 12, "Serial Number"},
    {20, 7, "Device Details"},
    {27, 3, "Firmware Versions"},
    {40, 20, "Hardware Info"}
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
  return DataType::U_WORD;
}

float DeyeInverter::convert_value(uint16_t raw, DataType type, float scale, float offset) {
  float value;
  switch (type) {
    case DataType::S_WORD:
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
  uint8_t hours = value / 100;
  uint8_t minutes = value % 100;
  char buffer[6];
  snprintf(buffer, sizeof(buffer), "%02d:%02d", hours, minutes);
  return std::string(buffer);
}

std::string DeyeInverter::format_version(uint16_t value) {
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

void DeyeSensor::setup() {
  if (this->parent_ != nullptr) {
    this->parent_->register_sensor(this);
  }
}

void DeyeSensor::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Sensor:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%04X", this->address_);
  ESP_LOGCONFIG(TAG, "  Scale: %f", this->scale_);
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

void DeyeBinarySensor::setup() {
  if (this->parent_ != nullptr) {
    this->parent_->register_binary_sensor(this);
  }
}

void DeyeBinarySensor::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Binary Sensor:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%04X", this->address_);
}
#endif

// =============================================================================
// DEYE TEXT SENSOR IMPLEMENTATION
// =============================================================================
#ifdef USE_TEXT_SENSOR

void DeyeTextSensor::update_value(uint16_t raw_value) {
  if (this->is_status_) {
    switch (raw_value) {
      case 0: this->publish_state("Standby"); break;
      case 1: this->publish_state("Self-Check"); break;
      case 2: this->publish_state("Normal"); break;
      case 3: this->publish_state("Alarm"); break;
      case 4: this->publish_state("Fault"); break;
      default: this->publish_state("Unknown"); break;
    }
  } else if (this->is_device_type_) {
    switch (raw_value) {
      case 0x0200: this->publish_state("String Inverter"); break;
      case 0x0300: this->publish_state("Single Phase Hybrid"); break;
      case 0x0400: this->publish_state("Micro Inverter"); break;
      case 0x0500: this->publish_state("Three Phase Hybrid"); break;
      default: this->publish_state("Unknown (" + std::to_string(raw_value) + ")"); break;
    }
  } else if (this->is_firmware_version_ || this->is_hardware_version_) {
    this->publish_state(DeyeInverter::format_version(raw_value));
  } else if (this->is_time_point_) {
    this->publish_state(DeyeInverter::format_time_point(raw_value));
  } else if (!this->mapping_.empty()) {
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

void DeyeTextSensor::setup() {
  if (this->parent_ != nullptr) {
    this->parent_->register_text_sensor(this);
  }
}

void DeyeTextSensor::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Text Sensor:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%04X", this->address_);
}
#endif

// =============================================================================
// DEYE SWITCH IMPLEMENTATION
// =============================================================================
#ifdef USE_SWITCH

void DeyeSwitch::update_value(uint16_t raw_value) {
  if (this->is_2bit_field_) {
    uint16_t field_value = (raw_value & this->bitmask_) >> this->bit_shift_;
    bool state = (field_value == 0x03);
    this->publish_state(state);
  } else {
    bool state = (raw_value & this->bitmask_) != 0;
    this->publish_state(state);
  }
}

void DeyeSwitch::write_state(bool state) {
  this->publish_state(state);
  
  if (this->parent_ != nullptr) {
    if (this->is_2bit_field_) {
      uint16_t value = state ? this->value_enable_ : this->value_disable_;
      this->parent_->write_register_masked(this->address_, value, this->bitmask_);
    } else {
      uint16_t value = state ? 0xFFFF : 0x0000;
      this->parent_->write_register_masked(this->address_, value, this->bitmask_);
    }
  }
}

void DeyeSwitch::setup() {
  if (this->parent_ != nullptr) {
    this->parent_->register_switch(this);
  }
}

void DeyeSwitch::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Switch:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%04X", this->address_);
}
#endif

// =============================================================================
// DEYE NUMBER IMPLEMENTATION
// =============================================================================
#ifdef USE_NUMBER

void DeyeNumber::update_value(uint16_t raw_value) {
  float value;
  if (this->is_time_point_) {
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
      raw_value = static_cast<uint16_t>(value);
    } else {
      raw_value = static_cast<uint16_t>(value / this->scale_);
    }
    this->parent_->write_register(this->address_, raw_value);
  }
}

void DeyeNumber::setup() {
  if (this->parent_ != nullptr) {
    this->parent_->register_number(this);
  }
}

void DeyeNumber::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Number:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%04X", this->address_);
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
      this->parent_->write_register(this->address_, it->second);
    }
  }
}

void DeyeSelect::setup() {
  if (this->parent_ != nullptr) {
    this->parent_->register_select(this);
  }
}

void DeyeSelect::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Select:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%04X", this->address_);
}
#endif

// =============================================================================
// DEYE DATETIME IMPLEMENTATION
// =============================================================================
#ifdef USE_DATETIME

void DeyeDateTime::update_value(uint16_t raw_value) {
  uint8_t hour, minute;
  parse_hhmm(raw_value, hour, minute);
  
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
  auto time_opt = call.get_hour();
  if (!time_opt.has_value()) return;
  
  uint8_t hour = time_opt.value();
  uint8_t minute = call.get_minute().value_or(0);
  
  uint16_t hhmm_value = format_hhmm(hour, minute);
  
  auto now = ESPTime::from_epoch_utc(0);
  now.year = 1970;
  now.month = 1;
  now.day_of_month = 1;
  now.hour = hour;
  now.minute = minute;
  now.second = 0;
  now.recalc_timestamp_utc(false);
  this->set_datetime(now);
  
  if (this->parent_ != nullptr) {
    this->parent_->write_register(this->address_, hhmm_value);
  }
}

void DeyeDateTime::parse_hhmm(uint16_t value, uint8_t& hour, uint8_t& minute) {
  hour = value / 100;
  minute = value % 100;
  if (hour > 23) hour = 23;
  if (minute > 59) minute = 59;
}

uint16_t DeyeDateTime::format_hhmm(uint8_t hour, uint8_t minute) {
  if (hour > 23) hour = 23;
  if (minute > 59) minute = 59;
  return (hour * 100) + minute;
}

void DeyeDateTime::setup() {
  if (this->parent_ != nullptr) {
    this->parent_->register_datetime(this);
  }
}

void DeyeDateTime::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye DateTime:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%04X", this->address_);
}
#endif

// =============================================================================
// DEYE TIME IMPLEMENTATION
// =============================================================================
#ifdef USE_TIME

void DeyeTime::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Deye Time...");
  if (this->parent_ != nullptr) {
    this->parent_->register_time(this);
  }
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
  
  auto local_time = this->now();
  if (!local_time.is_valid()) {
    ESP_LOGW(TAG, "Current time is not valid, skipping inverter time sync");
    return;
  }
  
  bool should_sync = false;
  
  if (this->time_just_set_) {
    ESP_LOGI(TAG, "Local time was just set, syncing to inverter");
    should_sync = true;
    this->time_just_set_ = false;
  } else if (this->inverter_time_valid_ && this->max_time_diff_ > 0) {
    int64_t diff_seconds = local_time.timestamp - this->inverter_time_.timestamp;
    if (diff_seconds < 0) diff_seconds = -diff_seconds;
    
    if (diff_seconds * 1000 > this->max_time_diff_) {
      ESP_LOGI(TAG, "Time difference too large: %lld seconds, syncing to inverter", diff_seconds);
      should_sync = true;
    } else {
      ESP_LOGV(TAG, "Time difference within limits: %lld seconds", diff_seconds);
    }
  } else {
    ESP_LOGI(TAG, "No inverter time received yet, will sync when available");
  }
  
  if (should_sync) {
    this->write_time_to_inverter();
  }
}

void DeyeTime::write_time_to_inverter() {
  if (this->parent_ == nullptr) {
    return;
  }
  
  auto now_time = this->now();
  if (!now_time.is_valid()) {
    ESP_LOGW(TAG, "Current time is not valid, cannot sync to inverter");
    return;
  }
  
  uint8_t year_offset = now_time.year - 2000;
  uint8_t month = now_time.month;
  uint8_t day = now_time.day_of_month;
  uint8_t hour = now_time.hour;
  uint8_t minute = now_time.minute;
  uint8_t second = now_time.second;
  
  if (month < 1) month = 1;
  if (month > 12) month = 12;
  if (day < 1) day = 1;
  if (day > 31) day = 31;
  if (hour > 23) hour = 0;
  if (minute > 59) minute = 0;
  if (second > 59) second = 0;
  
  uint16_t reg62 = (static_cast<uint16_t>(year_offset) << 8) | month;
  uint16_t reg63 = (static_cast<uint16_t>(day) << 8) | hour;
  uint16_t reg64 = (static_cast<uint16_t>(minute) << 8) | second;
  
  this->parent_->write_register(62, reg62);
  this->parent_->write_register(63, reg63);
  this->parent_->write_register(64, reg64);
  
  ESP_LOGI(TAG, "System time written to inverter: %04d-%02d-%02d %02d:%02d:%02d",
           now_time.year, now_time.month, now_time.day_of_month,
           now_time.hour, now_time.minute, now_time.second);
  
  this->inverter_time_ = now_time;
  this->inverter_time_valid_ = true;
}

void DeyeTime::on_system_time_received(uint8_t year, uint8_t month, uint8_t day,
                                       uint8_t hour, uint8_t minute, uint8_t second) {
  if (month < 1 || month > 12 || day < 1 || day > 31 || hour > 23 || minute > 59 || second > 59) {
    ESP_LOGW(TAG, "Invalid inverter time received: %02d-%02d-%02d %02d:%02d:%02d",
             year, month, day, hour, minute, second);
    this->inverter_time_valid_ = false;
    return;
  }
  
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
  
  this->sync_time_if_needed();
}

void DeyeTime::update() {
  // Called periodically by the time component
}
#endif

// =============================================================================
// DEYE INVERTER SETUP
// =============================================================================

void DeyeInverter::setup() {
  ESP_LOGCONFIG(TAG, "Setting up Deye Inverter...");
  this->update_device_info();
}

void DeyeInverter::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Inverter:");
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
// REGISTER ENTITY METHODS
// =============================================================================

void DeyeInverter::register_sensor(sensor::Sensor *sensor) {
  this->sensors_.push_back(sensor);
}

void DeyeInverter::register_binary_sensor(binary_sensor::BinarySensor *sensor) {
  this->binary_sensors_.push_back(sensor);
}

void DeyeInverter::register_text_sensor(text_sensor::TextSensor *sensor) {
  this->text_sensors_.push_back(sensor);
}

void DeyeInverter::register_switch(switch_::Switch *sw) {
  this->switches_.push_back(sw);
}

#ifdef USE_NUMBER
void DeyeInverter::register_number(number::Number *num) {
  this->numbers_.push_back(num);
}
#endif

#ifdef USE_SELECT
void DeyeInverter::register_select(select::Select *sel) {
  this->selects_.push_back(sel);
}
#endif

#ifdef USE_DATETIME
void DeyeInverter::register_datetime(datetime::DateTimeEntity *dt) {
  this->datetimes_.push_back(dt);
}
#endif

#ifdef USE_TIME
void DeyeInverter::register_time(time::RealTimeClock *tm) {
  this->times_.push_back(tm);
}
#endif

// =============================================================================
// MAIN LOOP
// =============================================================================

void DeyeInverter::loop() {
  const uint32_t now = millis();
  
  ESP_LOGD(TAG, "loop() called, now=%u, last_live=%u, interval=%u", 
           now, this->last_live_update_, this->interval_live_);
  
  if (now - this->last_live_update_ >= this->interval_live_) {
    this->last_live_update_ = now;
    ESP_LOGD(TAG, "Starting live data update");
    this->update_live_data();
  }
  
  if (now - this->last_stats_update_ >= this->interval_statistics_) {
    this->last_stats_update_ = now;
    this->update_statistics();
  }
  
  if (now - this->last_battery_modules_update_ >= this->interval_battery_modules_) {
    this->last_battery_modules_update_ = now;
    this->update_battery_modules();
  }
  
  if (now - this->last_settings_update_ >= this->interval_settings_) {
    this->last_settings_update_ = now;
    this->update_settings();
  }
  
  if (now - this->last_system_settings_update_ >= this->interval_system_settings_) {
    this->last_system_settings_update_ = now;
    this->update_system_settings();
  }
  
  if (now - this->last_grid_protection_update_ >= this->interval_grid_protection_) {
    this->last_grid_protection_update_ = now;
    this->update_grid_protection();
  }
  
  if (now - this->last_extended_settings_update_ >= this->interval_extended_settings_) {
    this->last_extended_settings_update_ = now;
    this->update_extended_settings();
  }
  
  if (now - this->last_california_settings_update_ >= this->interval_california_settings_) {
    this->last_california_settings_update_ = now;
    this->update_california_settings();
  }
  
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
  if (this->current_phase_ == UpdatePhase::IDLE || 
      this->current_phase_ == UpdatePhase::LIVE_DATA) {
    this->current_phase_ = UpdatePhase::LIVE_DATA;
    
    if (this->current_range_index_ < LIVE_RANGES_COUNT) {
      this->update_register_range(LIVE_RANGES[this->current_range_index_]);
      this->current_range_index_++;
    } else {
      this->current_range_index_ = 0;
      this->current_phase_ = UpdatePhase::IDLE;
    }
  }
}

void DeyeInverter::update_statistics() {
  if (this->current_phase_ == UpdatePhase::IDLE) {
    this->current_phase_ = UpdatePhase::STATISTICS;
    
    for (size_t i = 0; i < STATS_RANGES_COUNT; i++) {
      this->update_register_range(STATS_RANGES[i]);
      delay(10);
    }
    
    this->current_phase_ = UpdatePhase::IDLE;
  }
}

void DeyeInverter::update_battery_modules() {
  if (this->current_phase_ == UpdatePhase::IDLE || 
      this->current_phase_ == UpdatePhase::BATTERY_MODULES) {
    this->current_phase_ = UpdatePhase::BATTERY_MODULES;
    
    if (this->current_battery_module_range_ < BATTERY_MODULE_RANGES_COUNT) {
      this->update_register_range(BATTERY_MODULE_RANGES[this->current_battery_module_range_]);
      this->current_battery_module_range_++;
    } else {
      this->current_battery_module_range_ = 0;
      this->current_phase_ = UpdatePhase::IDLE;
    }
  }
}

void DeyeInverter::update_settings() {
  if (this->current_phase_ == UpdatePhase::IDLE) {
    this->current_phase_ = UpdatePhase::SETTINGS;
    
    ESP_LOGD(TAG, "Reading settings...");
    
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
  
  for (size_t i = 0; i < DEVICE_INFO_RANGES_COUNT; i++) {
    this->update_register_range(DEVICE_INFO_RANGES[i]);
    delay(10);
  }
  
  this->device_info_initialized_ = true;
}

void DeyeInverter::update_register_range(const RegisterRange& range) {
  ESP_LOGD(TAG, "Sending Modbus read: register 0x%04X, count %u", 
           range.start, range.count);
  
  uint8_t payload[4];
  payload[0] = (range.start >> 8) & 0xFF;
  payload[1] = range.start & 0xFF;
  payload[2] = (range.count >> 8) & 0xFF;
  payload[3] = range.count & 0xFF;
  
  this->send(0x03, range.start, range.count, 4, payload);
}

// =============================================================================
// WRITE METHODS
// =============================================================================

void DeyeInverter::write_register(uint16_t address, uint16_t value) {
  ESP_LOGD(TAG, "Writing register 0x%04X = 0x%04X", address, value);
  
  uint8_t payload[4];
  payload[0] = (address >> 8) & 0xFF;
  payload[1] = address & 0xFF;
  payload[2] = (value >> 8) & 0xFF;
  payload[3] = value & 0xFF;
  
  this->send(0x06, address, 1, 4, payload);
}

void DeyeInverter::write_register_masked(uint16_t address, uint16_t value, uint16_t mask) {
  ESP_LOGD(TAG, "Writing register 0x%04X with mask 0x%04X = 0x%04X", address, mask, value);
  
  uint16_t masked_value = value & mask;
  this->write_register(address, masked_value);
}

// =============================================================================
// MODBUS CALLBACKS
// =============================================================================

void DeyeInverter::on_modbus_data(const std::vector<uint8_t>& data) {
  if (data.size() < 4) {
    ESP_LOGW(TAG, "Received invalid data (too short: %u bytes)", data.size());
    return;
  }
  
  uint16_t start_address = (data[0] << 8) | data[1];
  std::vector<uint8_t> reg_data(data.begin() + 2, data.end());
  
  ESP_LOGV(TAG, "Received %u bytes for register 0x%04X", reg_data.size(), start_address);
  
  if (start_address >= 3 && start_address <= 14) {
#ifdef USE_TEXT_SENSOR
    this->update_serial_number_from_data(start_address, reg_data);
#endif
  } else if (start_address >= 27 && start_address <= 29) {
#ifdef USE_TEXT_SENSOR
    this->update_firmware_info_from_data(start_address, reg_data);
#endif
  } else if (start_address >= 684 && start_address <= 809) {
#ifdef USE_SENSOR
    this->update_battery_module_sensors(start_address, reg_data);
#endif
  } else if (start_address <= 62 && start_address + (reg_data.size() / 2) > 62) {
#ifdef USE_TIME
    this->update_system_time_from_data(start_address, reg_data);
#endif
  }
  
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
// DATA PARSING HELPERS
// =============================================================================

float DeyeInverter::parse_value(const std::vector<uint8_t>& data, size_t offset,
                                uint8_t bytes, DataType data_type, float scale, float offset_val) {
  float raw_value = 0.0f;
  
  if (bytes == 4) {
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
    if (data_type == DataType::S_WORD) {
      int16_t val16 = this->parse_int16_value(data, offset);
      raw_value = static_cast<float>(val16);
    } else {
      uint16_t val16 = this->parse_uint16(data, offset);
      raw_value = static_cast<float>(val16);
    }
  }
  
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
    value = (static_cast<uint32_t>(data[offset + 2]) << 24) |
            (static_cast<uint32_t>(data[offset + 3]) << 16) |
            (static_cast<uint32_t>(data[offset]) << 8) |
            static_cast<uint32_t>(data[offset + 1]);
  } else {
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
    value = (static_cast<uint32_t>(data[offset + 2]) << 24) |
            (static_cast<uint32_t>(data[offset + 3]) << 16) |
            (static_cast<uint32_t>(data[offset]) << 8) |
            static_cast<uint32_t>(data[offset + 1]);
  } else {
    value = (static_cast<uint32_t>(data[offset]) << 24) |
            (static_cast<uint32_t>(data[offset + 1]) << 16) |
            (static_cast<uint32_t>(data[offset + 2]) << 8) |
            static_cast<uint32_t>(data[offset + 3]);
  }
  
  return value;
}

int32_t DeyeInverter::parse_int32(const std::vector<uint8_t>& data, size_t offset, bool is_signed) {
  if (offset + 4 > data.size()) return 0;
  
  uint32_t value = (static_cast<uint32_t>(data[offset]) << 24) |
                   (static_cast<uint32_t>(data[offset + 1]) << 16) |
                   (static_cast<uint32_t>(data[offset + 2]) << 8) |
                   static_cast<uint32_t>(data[offset + 3]);
  
  if (is_signed && (value & 0x80000000)) {
    return static_cast<int32_t>(value | 0xFFFFFFFF00000000ULL);
  }
  
  return static_cast<int32_t>(value);
}

int16_t DeyeInverter::parse_int16(const std::vector<uint8_t>& data, size_t offset, bool is_signed) {
  if (offset + 2 > data.size()) return 0;
  
  uint16_t value = (data[offset] << 8) | data[offset + 1];
  
  if (is_signed && (value & 0x8000)) {
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
  
  for (size_t i = offset; i < offset + length && i < data.size(); i += 2) {
    char high_byte = data[i];
    char low_byte = (i + 1 < data.size()) ? data[i + 1] : 0;
    
    if (high_byte >= 32 && high_byte < 127) result += high_byte;
    if (low_byte >= 32 && low_byte < 127) result += low_byte;
  }
  
  return result;
}

// =============================================================================
// ENTITY UPDATE METHODS
// =============================================================================

#ifdef USE_SENSOR
void DeyeInverter::update_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *base_sensor : this->sensors_) {
    auto *sensor = static_cast<DeyeSensor*>(base_sensor);
    if (sensor->get_is_battery_module()) continue;
    
    uint16_t sensor_addr = sensor->get_address();
    
    if (sensor_addr >= start_address && 
        sensor_addr < start_address + (data.size() / 2)) {
      size_t offset = (sensor_addr - start_address) * 2;
      
      if (offset + sensor->get_bytes() <= data.size()) {
        if (sensor->get_bytes() == 4) {
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

void DeyeInverter::update_battery_module_sensors(uint16_t start_address, const std::vector<uint8_t>& data) {
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
  
  for (auto *base_sensor : this->sensors_) {
    auto *sensor = static_cast<DeyeSensor*>(base_sensor);
    if (sensor->get_is_battery_module() && sensor->get_module_index() == module_index) {
      uint16_t sensor_addr = sensor->get_address();
      
      if (sensor_addr >= start_address && sensor_addr < start_address + (data.size() / 2)) {
        size_t offset = (sensor_addr - start_address) * 2;
        
        if (offset + 2 <= data.size()) {
          uint16_t raw_value = this->parse_uint16(data, offset);
          
          if (sensor->get_is_cell_voltage()) {
            uint8_t cell_idx = sensor->get_cell_index();
            if (cell_idx < 8) {
              size_t cell_offset = 4 + (cell_idx * 2);
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
    size_t cell_offset = 4 + (cell_index * 2);
    if (cell_offset + 2 <= data.size()) {
      return static_cast<float>(this->parse_uint16(data, cell_offset));
    }
  } else if (offset + 2 <= data.size()) {
    return static_cast<float>(this->parse_uint16(data, offset));
  }
  return 0.0f;
}

#ifdef USE_BINARY_SENSOR
void DeyeInverter::update_binary_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *base_sensor : this->binary_sensors_) {
    auto *sensor = static_cast<DeyeBinarySensor*>(base_sensor);
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
  for (auto *base_sensor : this->text_sensors_) {
    auto *sensor = static_cast<DeyeTextSensor*>(base_sensor);
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
          uint16_t raw_value = this->parse_uint16(data, offset);
          sensor->update_value(raw_value);
        } else {
          std::string value = this->parse_string(data, offset, length);
          sensor->update_string(value);
        }
      }
    }
  }
}

void DeyeInverter::update_serial_number_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  if (start_address > 14) return;
  
  for (auto *base_sensor : this->text_sensors_) {
    auto *sensor = static_cast<DeyeTextSensor*>(base_sensor);
    if (sensor->get_is_serial_number()) {
      std::string serial = this->parse_string(data, 0, data.size());
      sensor->update_string(serial);
    }
  }
}

void DeyeInverter::update_firmware_info_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  if (start_address < 27 || start_address > 29) return;
  
  for (auto *base_sensor : this->text_sensors_) {
    auto *sensor = static_cast<DeyeTextSensor*>(base_sensor);
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

#ifdef USE_SWITCH
void DeyeInverter::update_switches_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *base_sw : this->switches_) {
    auto *sw = static_cast<DeyeSwitch*>(base_sw);
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
  for (auto *base_num : this->numbers_) {
    auto *num = static_cast<DeyeNumber*>(base_num);
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
  for (auto *base_sel : this->selects_) {
    auto *sel = static_cast<DeyeSelect*>(base_sel);
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
  for (auto *base_dt : this->datetimes_) {
    auto *dt = static_cast<DeyeDateTime*>(base_dt);
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
  if (start_address > 62 || data.size() < 6) {
    return;
  }
  
  size_t offset62 = (62 - start_address) * 2;
  if (offset62 + 6 > data.size()) {
    return;
  }
  
  uint8_t year = data[offset62];
  uint8_t month = data[offset62 + 1];
  uint8_t day = data[offset62 + 2];
  uint8_t hour = data[offset62 + 3];
  uint8_t minute = data[offset62 + 4];
  uint8_t second = data[offset62 + 5];
  
  ESP_LOGD(TAG, "Inverter system time: %02d-%02d-%02d %02d:%02d:%02d",
           year, month, day, hour, minute, second);
  
  for (auto *base_tm : this->times_) {
    auto *tm = static_cast<DeyeTime*>(base_tm);
    tm->on_system_time_received(year, month, day, hour, minute, second);
  }
}
#endif

}  // namespace deye_inverter
}  // namespace esphome
