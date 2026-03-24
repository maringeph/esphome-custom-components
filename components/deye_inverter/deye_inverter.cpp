#include "deye_inverter.h"
#include "esphome/core/log.h"

namespace esphome {
namespace deye_inverter {

static const char *const TAG = "deye_inverter";

// =============================================================================
// SIMPLIFIED REGISTER RANGE DEFINITIONS - Big contiguous blocks
// =============================================================================

// Device Info: 0-29 (30 registers) - ONE block
const RegisterRange DeyeInverter::DEVICE_INFO_RANGES[] = {
    {0, 30, "Device Info"}  // 0-29: Device Type, Modbus Address, Serial Number, Firmware
};

// Livedata: 500-683 (184 registers) - ONE block
const RegisterRange DeyeInverter::LIVE_RANGES[] = {
    {500, 184, "Livedata"}  // 500-683: Status, Temps, Battery, Grid, Output, Load, Generator, PV
};

// Statistics: Multiple ranges for different stat categories
const RegisterRange DeyeInverter::STATS_RANGES[] = {
    {501, 14, "Daily Stats"},   // 501-514
    {514, 6, "Battery Stats"},  // 514-519
    {520, 10, "Grid Stats"},    // 520-529
    {529, 11, "PV Stats"}       // 529-539
};

// Settings: 60-228 (169 registers) - ONE block
const RegisterRange DeyeInverter::SETTINGS_RANGES[] = {
    {60, 169, "Settings"}  // 60-228: System Settings, Battery, Grid, Time Points
};

// Settings 2: 310-419 (110 registers) - ONE block
const RegisterRange DeyeInverter::SETTINGS_2_RANGES[] = {
    {310, 110, "Settings 2"}  // 310-419: Extended Monitoring, California Compliance, Solar
};

// Battery Modules: 9 separate ranges for 9 battery modules (684-809)
const RegisterRange DeyeInverter::BATTERY_MODULE_RANGES[] = {
    {684, 14, "Battery Module 1"},  // 684-697
    {698, 14, "Battery Module 2"},  // 698-711
    {712, 14, "Battery Module 3"},  // 712-725
    {726, 14, "Battery Module 4"},  // 726-739
    {740, 14, "Battery Module 5"},  // 740-753
    {754, 14, "Battery Module 6"},  // 754-767
    {768, 14, "Battery Module 7"},  // 768-781
    {782, 14, "Battery Module 8"},  // 782-795
    {796, 14, "Battery Module 9"}   // 796-809
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
  // Queue device info read on startup
  this->queue_request(RequestType::DEVICE_INFO);
}

void DeyeInverter::dump_config() {
  ESP_LOGCONFIG(TAG, "Deye Inverter:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%02X", this->address_);
  ESP_LOGCONFIG(TAG, "  Live Update Interval: %u ms", this->interval_live_);
  ESP_LOGCONFIG(TAG, "  Stats Update Interval: %u ms", this->interval_statistics_);
  ESP_LOGCONFIG(TAG, "  Settings Update Interval: %u ms", this->interval_settings_);
  ESP_LOGCONFIG(TAG, "  Settings 2 Update Interval: %u ms", this->interval_settings_2_);
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
// UPDATE METHOD - Following ds100_meter pattern
// =============================================================================

void DeyeInverter::update() {
  uint32_t now = millis();

  // Timeout handling: Reset request_in_progress_ if no response for 500ms
  if (this->request_in_progress_ && (now - this->last_request_time_ > 500)) {
    ESP_LOGW(TAG, "Request timeout - resetting request_in_progress");
    this->request_in_progress_ = false;
    this->outstanding_commands_ = 0;  // Reset counter on timeout
    this->last_request_time_ = 0;
    this->consecutive_timeouts_++;
    ESP_LOGV(TAG, "Consecutive timeouts: %d", this->consecutive_timeouts_);
  }

  // Check which categories are due and add them to the request queue
  // Priority order: TIME → LIVEDATA → STATISTICS → SETTINGS → SETTINGS_2 → BATTERY_MODULES → DEVICE_INFO
  if (now - this->last_time_update_ >= this->interval_time_) {
    this->queue_request(RequestType::TIME);
  }
  
  if (now - this->last_live_update_ >= this->interval_live_) {
    this->queue_request(RequestType::LIVEDATA);
  }
  
  if (now - this->last_stats_update_ >= this->interval_statistics_) {
    this->queue_request(RequestType::STATISTICS);
  }
  
  if (now - this->last_settings_update_ >= this->interval_settings_) {
    this->queue_request(RequestType::SETTINGS);
  }
  
  if (now - this->last_settings_2_update_ >= this->interval_settings_2_) {
    this->queue_request(RequestType::SETTINGS_2);
  }
  
  if (now - this->last_battery_modules_update_ >= this->interval_battery_modules_) {
    this->queue_request(RequestType::BATTERY_MODULES);
  }
  
  if (!this->device_info_initialized_ || 
      (now - this->last_device_info_update_ >= this->interval_device_info_)) {
    this->queue_request(RequestType::DEVICE_INFO);
  }

  // Process only ONE request per update() call to avoid bus overload
  // The individual intervals (1s, 5s, 60s) are still respected by queue_request()
  if (!this->request_in_progress_ && this->pending_requests_ != 0) {
    RequestType next = this->get_highest_priority_pending();
    
    // If bus is overloaded, only process high-priority requests (TIME, LIVEDATA, STATISTICS, BATTERY_MODULES)
    if (this->consecutive_timeouts_ >= MAX_CONSECUTIVE_TIMEOUTS) {
      if (next == RequestType::TIME || next == RequestType::LIVEDATA || 
          next == RequestType::STATISTICS || next == RequestType::BATTERY_MODULES) {
        this->process_next_request();
      } else {
        ESP_LOGV(TAG, "Skipping low-priority request %d due to bus overload (timeouts: %d)", 
                 static_cast<int>(next), this->consecutive_timeouts_);
        // Clear this specific pending request to prevent queue buildup
        // BATTERY_MODULES is treated as high-priority, so don't clear it here
        switch (next) {
          case RequestType::SETTINGS: this->pending_requests_ &= ~PENDING_SETTINGS; break;
          case RequestType::SETTINGS_2: this->pending_requests_ &= ~PENDING_SETTINGS_2; break;
          case RequestType::DEVICE_INFO: this->pending_requests_ &= ~PENDING_DEVICE_INFO; break;
          default: break;
        }
      }
    } else {
      this->process_next_request();
    }
  }
}

// =============================================================================
// REQUEST QUEUE MANAGEMENT - Following ds100_meter pattern
// =============================================================================

void DeyeInverter::queue_request(RequestType type) {
  switch (type) {
    case RequestType::TIME:
      this->pending_requests_ |= PENDING_TIME;
      break;
    case RequestType::LIVEDATA:
      this->pending_requests_ |= PENDING_LIVEDATA;
      break;
    case RequestType::STATISTICS:
      this->pending_requests_ |= PENDING_STATISTICS;
      break;
    case RequestType::SETTINGS:
      this->pending_requests_ |= PENDING_SETTINGS;
      break;
    case RequestType::SETTINGS_2:
      this->pending_requests_ |= PENDING_SETTINGS_2;
      break;
    case RequestType::BATTERY_MODULES:
      this->pending_requests_ |= PENDING_BATTERY_MODULES;
      break;
    case RequestType::DEVICE_INFO:
      this->pending_requests_ |= PENDING_DEVICE_INFO;
      break;
  }
}

DeyeInverter::RequestType DeyeInverter::get_highest_priority_pending() {
  // Priority order: TIME → LIVEDATA → STATISTICS → SETTINGS → SETTINGS_2 → BATTERY_MODULES → DEVICE_INFO
  if (this->pending_requests_ & PENDING_TIME)
    return RequestType::TIME;
  if (this->pending_requests_ & PENDING_LIVEDATA)
    return RequestType::LIVEDATA;
  if (this->pending_requests_ & PENDING_STATISTICS)
    return RequestType::STATISTICS;
  if (this->pending_requests_ & PENDING_SETTINGS)
    return RequestType::SETTINGS;
  if (this->pending_requests_ & PENDING_SETTINGS_2)
    return RequestType::SETTINGS_2;
  if (this->pending_requests_ & PENDING_BATTERY_MODULES)
    return RequestType::BATTERY_MODULES;
  if (this->pending_requests_ & PENDING_DEVICE_INFO)
    return RequestType::DEVICE_INFO;
  return RequestType::LIVEDATA;  // Should never reach here if pending_requests_ != 0
}

void DeyeInverter::process_next_request() {
  if (this->pending_requests_ == 0)
    return;

  RequestType next = this->get_highest_priority_pending();
  uint32_t now = millis();
  this->last_request_time_ = now;
  this->request_in_progress_ = true;

  switch (next) {
    case RequestType::TIME: {
      ESP_LOGD(TAG, "Queueing request: time sync");
      // Don't clear pending flag here - wait for successful response in handler
      // Don't update timestamp here - wait for successful response
      
      // Read system time registers (62-64)
      auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
          this, modbus_controller::ModbusRegisterType::HOLDING, 62, 3);
      cmd.on_data_func = [this](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                 const std::vector<uint8_t> &data) {
        this->handle_time_response(data, 62);
      };
      this->queue_command(cmd);
      break;
    }

    case RequestType::LIVEDATA: {
      ESP_LOGD(TAG, "Queueing request: livedata");
      // Single block - no phasing needed
      auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
          this, modbus_controller::ModbusRegisterType::HOLDING,
          LIVE_RANGES[0].start, LIVE_RANGES[0].count);
      cmd.on_data_func = [this](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                const std::vector<uint8_t> &data) {
        this->handle_live_data_response(data, addr);
      };
      this->queue_command(cmd);
      break;
    }

    case RequestType::STATISTICS: {
      ESP_LOGD(TAG, "Queueing request: statistics");
      // Don't clear pending flag here - wait for successful response in handler
      // Don't update timestamp here - wait for successful response

      // Initialize command counter for multi-command request
      this->outstanding_commands_ = STATS_RANGES_COUNT;

      // Queue all statistics ranges
      for (size_t i = 0; i < STATS_RANGES_COUNT; i++) {
        auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
            this, modbus_controller::ModbusRegisterType::HOLDING,
            STATS_RANGES[i].start, STATS_RANGES[i].count);
        cmd.on_data_func = [this, i](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                      const std::vector<uint8_t> &data) {
          this->handle_statistics_response(data, STATS_RANGES[i].start);
          // Guard against underflow if timeout already reset the counter
          if (this->outstanding_commands_ > 0) {
            this->outstanding_commands_--;
            if (this->outstanding_commands_ == 0) {
              this->request_in_progress_ = false;
              this->pending_requests_ &= ~PENDING_STATISTICS;
              this->last_stats_update_ = millis();
            }
          }
        };
        this->queue_command(cmd);
      }
      break;
    }

    case RequestType::BATTERY_MODULES: {
      ESP_LOGD(TAG, "Queueing request: battery modules (range %zu/%zu: %s)",
               this->current_battery_module_range_ + 1, BATTERY_MODULE_RANGES_COUNT,
               BATTERY_MODULE_RANGES[this->current_battery_module_range_].name);
      
      // Queue ONLY ONE range per call to allow interleaving with other categories
      const RegisterRange& range = BATTERY_MODULE_RANGES[this->current_battery_module_range_];
      uint8_t module_idx = static_cast<uint8_t>(this->current_battery_module_range_);
      auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
          this, modbus_controller::ModbusRegisterType::HOLDING,
          range.start, range.count);
      cmd.on_data_func = [this, module_idx](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                            const std::vector<uint8_t> &data) {
        this->handle_battery_module_response(data, addr, module_idx);
      };
      this->queue_command(cmd);
      
      // Don't clear pending flag here - wait for last range to complete in handler
      // Don't update timestamp here - wait for last range to complete
      
      // Increment index for next time (will be checked in handler for completion)
      this->current_battery_module_range_++;
      if (this->current_battery_module_range_ >= BATTERY_MODULE_RANGES_COUNT) {
        this->current_battery_module_range_ = 0;
      }
      break;
    }

    case RequestType::SETTINGS: {
      ESP_LOGD(TAG, "Queueing request: settings (60-228, 169 registers)");
      // Single big block read - 60-228: System Settings, Battery, Grid, Time Points
      auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
          this, modbus_controller::ModbusRegisterType::HOLDING,
          SETTINGS_RANGES[0].start, SETTINGS_RANGES[0].count);
      cmd.on_data_func = [this](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                const std::vector<uint8_t> &data) {
        this->handle_settings_response(data, addr);
        this->request_in_progress_ = false;
        this->pending_requests_ &= ~PENDING_SETTINGS;
        this->last_settings_update_ = millis();
      };
      this->queue_command(cmd);
      break;
    }

    case RequestType::SETTINGS_2: {
      ESP_LOGD(TAG, "Queueing request: settings 2 (310-419, 110 registers)");
      // Single big block read - 310-419: Extended Monitoring, California Compliance, Solar
      auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
          this, modbus_controller::ModbusRegisterType::HOLDING,
          SETTINGS_2_RANGES[0].start, SETTINGS_2_RANGES[0].count);
      cmd.on_data_func = [this](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                const std::vector<uint8_t> &data) {
        this->handle_settings_2_response(data, addr);
        this->request_in_progress_ = false;
        this->pending_requests_ &= ~PENDING_SETTINGS_2;
        this->last_settings_2_update_ = millis();
      };
      this->queue_command(cmd);
      break;
    }

    case RequestType::DEVICE_INFO: {
      ESP_LOGD(TAG, "Queueing request: device info (0-29, 30 registers)");
      // Single big block read - 0-29: Device Type, Serial Number, Firmware
      auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
          this, modbus_controller::ModbusRegisterType::HOLDING,
          DEVICE_INFO_RANGES[0].start, DEVICE_INFO_RANGES[0].count);
      cmd.on_data_func = [this](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                const std::vector<uint8_t> &data) {
        this->handle_device_info_response(data, addr);
        this->request_in_progress_ = false;
        this->pending_requests_ &= ~PENDING_DEVICE_INFO;
        this->last_device_info_update_ = millis();
        this->device_info_initialized_ = true;
      };
      this->queue_command(cmd);
      break;
    }
  }
}

// =============================================================================
// REGISTER READ COMMAND HELPER
// =============================================================================

void DeyeInverter::send_register_range_read(const RegisterRange& range) {
  ESP_LOGD(TAG, "Queueing Modbus read: register 0x%04X, count %u (%s)", 
           range.start, range.count, range.name);
  
  auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
      this, modbus_controller::ModbusRegisterType::HOLDING, range.start, range.count);
  cmd.on_data_func = [this, range](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                    const std::vector<uint8_t> &data) {
    this->handle_live_data_response(data, range.start);
  };
  this->queue_command(cmd);
}

// =============================================================================
// RESPONSE HANDLERS
// =============================================================================

void DeyeInverter::handle_time_response(const std::vector<uint8_t> &data, uint16_t start_address) {
  ESP_LOGV(TAG, "Received time response: %zu bytes for register 0x%04X", data.size(), start_address);
  
  // Reset consecutive timeouts counter on successful response
  if (this->consecutive_timeouts_ > 0) {
    ESP_LOGV(TAG, "Resetting consecutive timeouts (was %d)", this->consecutive_timeouts_);
    this->consecutive_timeouts_ = 0;
  }
  
  this->request_in_progress_ = false;
  
  // Clear pending flag and update timestamp on successful response
  this->pending_requests_ &= ~PENDING_TIME;
  this->last_time_update_ = millis();
  
  // Process time data (registers 62-64)
  if (data.size() >= 6) {
#ifdef USE_TIME
    this->update_system_time_from_data(start_address, data);
#endif
  }
}

void DeyeInverter::handle_live_data_response(const std::vector<uint8_t> &data, uint16_t start_address) {
  ESP_LOGV(TAG, "Received livedata response: %zu bytes for register 0x%04X", data.size(), start_address);
  
  // Reset consecutive timeouts counter on successful response
  if (this->consecutive_timeouts_ > 0) {
    ESP_LOGV(TAG, "Resetting consecutive timeouts (was %d)", this->consecutive_timeouts_);
    this->consecutive_timeouts_ = 0;
  }
  
  this->request_in_progress_ = false;
  
  // Clear pending flag and update timestamp (single block, no phasing)
  this->pending_requests_ &= ~PENDING_LIVEDATA;
  this->last_live_update_ = millis();
  
  // LIVEDATA only handles registers 500-683, other address ranges are handled elsewhere
  
#ifdef USE_SENSOR
  this->update_sensors_from_data(start_address, data);
#endif
#ifdef USE_BINARY_SENSOR
  this->update_binary_sensors_from_data(start_address, data);
#endif
#ifdef USE_TEXT_SENSOR
  this->update_text_sensors_from_data(start_address, data);
#endif
#ifdef USE_SWITCH
  this->update_switches_from_data(start_address, data);
#endif
#ifdef USE_NUMBER
  this->update_numbers_from_data(start_address, data);
#endif
#ifdef USE_SELECT
  this->update_selects_from_data(start_address, data);
#endif
#ifdef USE_DATETIME
  this->update_datetimes_from_data(start_address, data);
#endif
}

void DeyeInverter::handle_statistics_response(const std::vector<uint8_t> &data, uint16_t start_address) {
  ESP_LOGV(TAG, "Received statistics response: %zu bytes for register 0x%04X", data.size(), start_address);

  if (this->consecutive_timeouts_ > 0) {
    this->consecutive_timeouts_ = 0;
  }

  // Note: request_in_progress_, pending flag, and timestamp are now managed in the callback
  // based on outstanding_commands_ counter
  
#ifdef USE_SENSOR
  this->update_sensors_from_data(start_address, data);
#endif
#ifdef USE_BINARY_SENSOR
  this->update_binary_sensors_from_data(start_address, data);
#endif
#ifdef USE_TEXT_SENSOR
  this->update_text_sensors_from_data(start_address, data);
#endif
#ifdef USE_SWITCH
  this->update_switches_from_data(start_address, data);
#endif
#ifdef USE_NUMBER
  this->update_numbers_from_data(start_address, data);
#endif
#ifdef USE_SELECT
  this->update_selects_from_data(start_address, data);
#endif
#ifdef USE_DATETIME
  this->update_datetimes_from_data(start_address, data);
#endif
}

void DeyeInverter::handle_battery_module_response(const std::vector<uint8_t> &data, uint16_t start_address, uint8_t module_index) {
  ESP_LOGV(TAG, "Received battery module %d response: %zu bytes for register 0x%04X", 
           module_index + 1, data.size(), start_address);
  
  if (this->consecutive_timeouts_ > 0) {
    this->consecutive_timeouts_ = 0;
  }
  
  this->request_in_progress_ = false;
  
  // For phased requests: clear flag and update timestamp only when last range completes
  // The index was already incremented in process_next_request(), so 0 means we just wrapped
  if (this->current_battery_module_range_ == 0) {
    this->pending_requests_ &= ~PENDING_BATTERY_MODULES;
    this->last_battery_modules_update_ = millis();
  }
  
  // Update battery module sensors first (special handling)
#ifdef USE_SENSOR
  this->update_battery_module_sensors(start_address, data);
#endif
  
  // Then update all other entity types consistently
  this->update_all_entities(start_address, data);
}

void DeyeInverter::handle_settings_response(const std::vector<uint8_t> &data, uint16_t start_address) {
  ESP_LOGV(TAG, "Received settings response: %zu bytes for register 0x%04X", data.size(), start_address);

  if (this->consecutive_timeouts_ > 0) {
    this->consecutive_timeouts_ = 0;
  }

  // Note: request_in_progress_, pending flag, and timestamp are now managed in the callback
  // based on outstanding_commands_ counter
  
#ifdef USE_SENSOR
  this->update_sensors_from_data(start_address, data);
#endif
#ifdef USE_BINARY_SENSOR
  this->update_binary_sensors_from_data(start_address, data);
#endif
#ifdef USE_TEXT_SENSOR
  this->update_text_sensors_from_data(start_address, data);
#endif
#ifdef USE_SWITCH
  this->update_switches_from_data(start_address, data);
#endif
#ifdef USE_NUMBER
  this->update_numbers_from_data(start_address, data);
#endif
#ifdef USE_SELECT
  this->update_selects_from_data(start_address, data);
#endif
#ifdef USE_DATETIME
  this->update_datetimes_from_data(start_address, data);
#endif
}

void DeyeInverter::handle_settings_2_response(const std::vector<uint8_t> &data, uint16_t start_address) {
  ESP_LOGV(TAG, "Received settings 2 response: %zu bytes for register 0x%04X", data.size(), start_address);

  if (this->consecutive_timeouts_ > 0) {
    this->consecutive_timeouts_ = 0;
  }

  // Note: request_in_progress_, pending flag, and timestamp are managed in the callback
  
  // Update all entity types consistently
  this->update_all_entities(start_address, data);
}

void DeyeInverter::handle_device_info_response(const std::vector<uint8_t> &data, uint16_t start_address) {
  ESP_LOGV(TAG, "Received device info response: %zu bytes for register 0x%04X", data.size(), start_address);

  if (this->consecutive_timeouts_ > 0) {
    this->consecutive_timeouts_ = 0;
  }

  // Note: request_in_progress_, pending flag, timestamp, and device_info_initialized_ are now managed in the callback
  // based on outstanding_commands_ counter
  
  if (start_address >= 3 && start_address <= 14) {
#ifdef USE_TEXT_SENSOR
    this->update_serial_number_from_data(start_address, data);
#endif
  } else if (start_address >= 27 && start_address <= 29) {
#ifdef USE_TEXT_SENSOR
    this->update_firmware_info_from_data(start_address, data);
#endif
  }
  
  // Update all entity types consistently
  this->update_all_entities(start_address, data);
}

// =============================================================================
// WRITE METHODS
// =============================================================================

void DeyeInverter::write_register(uint16_t address, uint16_t value) {
  ESP_LOGD(TAG, "Writing register 0x%04X = 0x%04X", address, value);
  
  auto cmd = modbus_controller::ModbusCommandItem::create_write_single_command(this, address, value);
  this->queue_command(cmd);
}

void DeyeInverter::write_register_masked(uint16_t address, uint16_t value, uint16_t mask) {
  ESP_LOGD(TAG, "Writing register 0x%04X with mask 0x%04X = 0x%04X", address, mask, value);
  
  // For masked writes, we need to read the current value first, then modify and write back
  // Create a read command to get current value
  auto read_cmd = modbus_controller::ModbusCommandItem::create_read_command(
      this, modbus_controller::ModbusRegisterType::HOLDING, address, 1);
  read_cmd.on_data_func = [this, address, value, mask](modbus_controller::ModbusRegisterType rt, 
                                                        uint16_t addr, 
                                                        const std::vector<uint8_t> &data) {
    if (data.size() >= 2) {
      uint16_t current_value = (data[0] << 8) | data[1];
      uint16_t new_value = (current_value & ~mask) | (value & mask);
      ESP_LOGD(TAG, "Read-Modify-Write: current=0x%04X, mask=0x%04X, value=0x%04X, new=0x%04X",
               current_value, mask, value, new_value);
      this->write_register(address, new_value);
    }
  };
  this->queue_command(read_cmd);
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
