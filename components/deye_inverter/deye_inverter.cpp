#include "deye_inverter.h"
#include "esphome/core/log.h"

namespace esphome
{
  namespace deye_inverter
  {

    static const char *const TAG = "deye_inverter";

    // =============================================================================
    // SIMPLIFIED REGISTER RANGE DEFINITIONS - Big contiguous blocks
    // =============================================================================

    // Device Info Range
    const RegisterRange DeyeInverter::DEVICE_INFO_RANGES[] = {
        {DEV_INFO_ADDR, DEV_INFO_LEN, "Device Info"}};

    // Time Range
    const RegisterRange DeyeInverter::TIME_RANGES[] = {
        {REG_SYSTEM_TIME_BYTE1, 3, "Time"}};

    // Livedata Ranges
    const RegisterRange DeyeInverter::LIVE_RANGES[] = {
        {LIVE_PART1_ADDR, LIVE_PART1_LEN, "Livedata Part 1"},
        {LIVE_PART2_ADDR, LIVE_PART2_LEN, "Livedata Part 2"}};

    // Statistics Ranges
    const RegisterRange DeyeInverter::STATS_RANGES[] = {
        {STATS_DAILY_ADDR, STATS_DAILY_LEN, "Daily Stats"},
        {STATS_BATTERY_ADDR, STATS_BATTERY_LEN, "Battery Stats"},
        {STATS_GRID_ADDR, STATS_GRID_LEN, "Grid Stats"},
        {STATS_PV_ADDR, STATS_PV_LEN, "PV Stats"}};

    // Settings Ranges (split into 2 blocks, max 128 per request)
    const RegisterRange DeyeInverter::SETTINGS_RANGES[] = {
        {SETTINGS_PART1_ADDR, SETTINGS_PART1_LEN, "Settings Part 1"},
        {SETTINGS_PART2_ADDR, SETTINGS_PART2_LEN, "Settings Part 2"}};

    // Settings 2 Range
    const RegisterRange DeyeInverter::SETTINGS_2_RANGES[] = {
        {SETTINGS2_ADDR, SETTINGS2_LEN, "Settings 2"}};

    // BMS Registers (2000-2999 range, actual = table + 2000)
    const RegisterRange DeyeInverter::BATTERY_MODULE_RANGES[] = {
        {BMS_IDS_ADDR, BMS_IDS_LEN, "BMS IDs"},
        {BMS_DATA_1_8_ADDR, BMS_DATA_1_8_LEN, "BMS Data 1-8"},
        {BMS_DATA_9_16_ADDR, BMS_DATA_9_16_LEN, "BMS Data 9-16"}};

    // =============================================================================
    // SETUP METHOD
    // =============================================================================

    // Calculate GCD of two numbers
    uint32_t DeyeInverter::gcd(uint32_t a, uint32_t b) {
      while (b != 0) {
        uint32_t temp = b;
        b = a % b;
        a = temp;
      }
      return a;
    }

    // Format version number (e.g., 0x1234 -> "18.52")
    std::string DeyeInverter::format_version(uint16_t value) {
      uint8_t major = (value >> 8) & 0xFF;
      uint8_t minor = value & 0xFF;
      char buffer[16];
      snprintf(buffer, sizeof(buffer), "%u.%02u", major, minor);
      return std::string(buffer);
    }

    // Format time point (e.g., 1430 -> "14:30")
    std::string DeyeInverter::format_time_point(uint16_t value) {
      uint8_t hours = value / 100;
      uint8_t minutes = value % 100;
      char buffer[16];
      snprintf(buffer, sizeof(buffer), "%02u:%02u", hours, minutes);
      return std::string(buffer);
    }

    void DeyeInverter::setup()
    {
      ESP_LOGCONFIG(TAG, "Setting up Deye Inverter...");
      ESP_LOGCONFIG(TAG, "  Update intervals:");
      ESP_LOGCONFIG(TAG, "    Live: %u ms", this->interval_live_);
      ESP_LOGCONFIG(TAG, "    Statistics: %u ms", this->interval_statistics_);
      ESP_LOGCONFIG(TAG, "    Settings: %u ms", this->interval_settings_);
      ESP_LOGCONFIG(TAG, "    Battery: %u ms", this->interval_battery_modules_);
      ESP_LOGCONFIG(TAG, "    Device Info: %u ms", this->interval_device_info_);

      // Calculate GCD of all intervals and set update interval to GCD/5
      // This ensures update() is called often enough to catch all intervals
      uint32_t g = gcd(this->interval_live_, this->interval_statistics_);
      g = gcd(g, this->interval_statistics_);
      g = gcd(g, this->interval_settings_);
      g = gcd(g, this->interval_battery_modules_);
      g = gcd(g, this->interval_device_info_);

      uint32_t update_interval = g / 5;
      if (update_interval < 50) update_interval = 50;  // Minimum 50ms
      if (update_interval > 1000) update_interval = 1000;  // Maximum 1s

      ESP_LOGCONFIG(TAG, "  Calculated update interval: %u ms (GCD/5)", update_interval);
      this->set_update_interval(update_interval);
    }

    // =============================================================================
    // UPDATE METHOD - TO BE IMPLEMENTED
    // =============================================================================

    void DeyeInverter::update()
    {
      check_request_due();
      get_next_request();
    }

    void DeyeInverter::check_request_due()
    {
      uint32_t now = millis();
      if (now >= this->next_device_info_request_)
      {
        this->pending_requests_ |= PENDING_DEVICE_INFO;
        this->next_device_info_request_ = now + this->interval_device_info_;
      }

      if (now >= this->next_settings_request_)
      {
        this->pending_requests_ |= PENDING_SETTINGS_0 | PENDING_SETTINGS_1 | PENDING_SETTINGS_2;
        this->next_settings_request_ = now + this->interval_settings_;
      }
      if (now >= this->next_live_request_)
      {
        this->pending_requests_ |= PENDING_LIVE_0 | PENDING_LIVE_1;
        this->next_live_request_ = now + this->interval_live_;
      }
      if (now >= this->next_stats_request_)
      {
        this->pending_requests_ |= PENDING_STATS_0 | PENDING_STATS_1 | PENDING_STATS_2 | PENDING_STATS_3;
        this->next_stats_request_ = now + this->interval_statistics_;
      }
      if (now >= this->next_battery_request_)
      {
        this->pending_requests_ |= PENDING_BATTERY_0 | PENDING_BATTERY_1 | PENDING_BATTERY_2;
        this->next_battery_request_ = now + this->interval_battery_modules_;
      }
    }

    void DeyeInverter::get_next_request()
    {
      if (this->pending_requests_ == 0)
        return;
      if (this->request_in_progress_ && millis() - this->request_start_time_ < REQUEST_TIMEOUT)
        return;

      // Get the highest priority pending request
      uint32_t now = millis();
      uint32_t range_bit = 0;
      const RegisterRange *range = nullptr;

      // Priority order: Check highest priority first
      if (this->pending_requests_ & PENDING_DEVICE_INFO)
      {
        range_bit = PENDING_DEVICE_INFO;
        range = &DEVICE_INFO_RANGES[0];
        this->pending_requests_ &= ~PENDING_DEVICE_INFO;
      }
      else if (this->pending_requests_ & PENDING_TIME)
      {
        range_bit = PENDING_TIME;
        range = &TIME_RANGES[0];
        this->pending_requests_ &= ~PENDING_TIME;
      }
      else if (this->pending_requests_ & PENDING_LIVE_0)
      {
        range_bit = PENDING_LIVE_0;
        range = &LIVE_RANGES[0];
        this->pending_requests_ &= ~PENDING_LIVE_0;
      }
      else if (this->pending_requests_ & PENDING_LIVE_1)
      {
        range_bit = PENDING_LIVE_1;
        range = &LIVE_RANGES[1];
        this->pending_requests_ &= ~PENDING_LIVE_1;
      }
      else if (this->pending_requests_ & PENDING_STATS_0)
      {
        range_bit = PENDING_STATS_0;
        range = &STATS_RANGES[0];
        this->pending_requests_ &= ~PENDING_STATS_0;
      }
      else if (this->pending_requests_ & PENDING_STATS_1)
      {
        range_bit = PENDING_STATS_1;
        range = &STATS_RANGES[1];
        this->pending_requests_ &= ~PENDING_STATS_1;
      }
      else if (this->pending_requests_ & PENDING_STATS_2)
      {
        range_bit = PENDING_STATS_2;
        range = &STATS_RANGES[2];
        this->pending_requests_ &= ~PENDING_STATS_2;
      }
      else if (this->pending_requests_ & PENDING_STATS_3)
      {
        range_bit = PENDING_STATS_3;
        range = &STATS_RANGES[3];
        this->pending_requests_ &= ~PENDING_STATS_3;
      }
      else if (this->pending_requests_ & PENDING_SETTINGS_0)
      {
        range_bit = PENDING_SETTINGS_0;
        range = &SETTINGS_RANGES[0];
        this->pending_requests_ &= ~PENDING_SETTINGS_0;
      }
      else if (this->pending_requests_ & PENDING_SETTINGS_1)
      {
        range_bit = PENDING_SETTINGS_1;
        range = &SETTINGS_RANGES[1];
        this->pending_requests_ &= ~PENDING_SETTINGS_1;
      }
      else if (this->pending_requests_ & PENDING_SETTINGS_2)
      {
        range_bit = PENDING_SETTINGS_2;
        range = &SETTINGS_2_RANGES[0];
        this->pending_requests_ &= ~PENDING_SETTINGS_2;
      }
      else if (this->pending_requests_ & PENDING_BATTERY_0)
      {
        range_bit = PENDING_BATTERY_0;
        range = &BATTERY_MODULE_RANGES[0];
        this->pending_requests_ &= ~PENDING_BATTERY_0;
      }
      else if (this->pending_requests_ & PENDING_BATTERY_1)
      {
        range_bit = PENDING_BATTERY_1;
        range = &BATTERY_MODULE_RANGES[1];
        this->pending_requests_ &= ~PENDING_BATTERY_1;
      }
      else if (this->pending_requests_ & PENDING_BATTERY_2)
      {
        range_bit = PENDING_BATTERY_2;
        range = &BATTERY_MODULE_RANGES[2];
        this->pending_requests_ &= ~PENDING_BATTERY_2;
      }
      else
        return;

      this->send_next_request(range_bit, range);
    }

    void DeyeInverter::send_next_request(const uint32_t range_bit, const RegisterRange *range)
    {
      ESP_LOGV(TAG, "Queueing request: %s (0x%04X, %d registers)",
               range->name, range->start, range->count);

      auto cmd = modbus_controller::ModbusCommandItem::create_read_command(
          this, modbus_controller::ModbusRegisterType::HOLDING,
          range->start, range->count);

      this->request_in_progress_ = true;
      this->request_start_time_ = millis();

      cmd.on_data_func = [this, range_bit, range](modbus_controller::ModbusRegisterType rt, uint16_t addr,
                                                  const std::vector<uint8_t> &data)
      {
        // Callback: Clear active bit
        this->request_in_progress_ = false;

        // Update appropriate timestamp based on range category
        switch (range_bit)
        {
        case PENDING_DEVICE_INFO:
          this->handle_device_info_response(data, range->start);
          break;
        case PENDING_TIME:
          this->handle_time_response(data, range->start);
          break;
        case PENDING_LIVE_0:
        case PENDING_LIVE_1:
          this->handle_live_data_response(data, range->start);
          break;
        case PENDING_STATS_0:
        case PENDING_STATS_1:
        case PENDING_STATS_2:
        case PENDING_STATS_3:
          this->handle_statistics_response(data, range->start);
          break;
        case PENDING_SETTINGS_0:
        case PENDING_SETTINGS_1:
        case PENDING_SETTINGS_2:
          this->handle_settings_response(data, range->start);
          break;
        case PENDING_BATTERY_0:
          this->handle_battery_module_response(data, range->start, 0);
          break;
        case PENDING_BATTERY_1:
          this->handle_battery_module_response(data, range->start, 1);
          break;
        case PENDING_BATTERY_2:
          this->handle_battery_module_response(data, range->start, 2);
          break;
        }
      };

      this->queue_command(cmd);
    }

    // =============================================================================
    // CONFIG DUMP
    // =============================================================================

    void DeyeInverter::dump_config()
    {
      ESP_LOGCONFIG(TAG, "Deye Inverter:");
      // TODO: Add config dump
    }

    // =============================================================================
    // HANDLER IMPLEMENTATIONS
    // =============================================================================

void DeyeInverter::handle_time_response(const std::vector<uint8_t> &data, uint16_t start_address) {
  ESP_LOGV(TAG, "Received time response: %zu bytes for register 0x%04X", data.size(), start_address);
  
  // Reset consecutive timeouts counter on successful response
  if (this->consecutive_timeouts_ > 0) {
    ESP_LOGV(TAG, "Resetting consecutive timeouts (was %d)", this->consecutive_timeouts_);
    this->consecutive_timeouts_ = 0;
  }
  
  this->request_in_progress_ = false;
  
  // Clear pending flag on successful response (TIME is read on-demand, not periodically)
  this->pending_requests_ &= ~PENDING_TIME;
  
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
  
  // Note: request_in_progress_, pending flag, and timestamp are managed in the callback
  // based on outstanding_commands_ counter
  
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

void DeyeInverter::handle_battery_module_response(const std::vector<uint8_t> &data, uint16_t start_address, uint8_t block_index) {
  ESP_LOGV(TAG, "Received battery block %d response: %zu bytes for register 0x%04X", 
           block_index + 1, data.size(), start_address);
  
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
  
  // Update battery sensors (2000-2999 range)
#ifdef USE_SENSOR
  this->update_sensors_from_data(start_address, data);
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
  
  if (start_address >= REG_RANGE_SERIAL_START && start_address <= REG_RANGE_SERIAL_END) {
#ifdef USE_TEXT_SENSOR
    this->update_serial_number_from_data(start_address, data);
#endif
  } else if (start_address >= REG_RANGE_FW_INFO_START && start_address <= REG_RANGE_FW_INFO_END) {
#ifdef USE_TEXT_SENSOR
    this->update_firmware_info_from_data(start_address, data);
#endif
  }
  
  // Update all entity types consistently
  this->update_all_entities(start_address, data);
}

    // =============================================================================
    // ENTITY REGISTRATION
    // =============================================================================

    void DeyeInverter::register_sensor(sensor::Sensor *sensor)
    {
      this->sensors_.push_back(sensor);
    }

#ifdef USE_BINARY_SENSOR
    void DeyeInverter::register_binary_sensor(binary_sensor::BinarySensor *sensor)
    {
      this->binary_sensors_.push_back(sensor);
    }
#endif

#ifdef USE_TEXT_SENSOR
    void DeyeInverter::register_text_sensor(text_sensor::TextSensor *sensor)
    {
      this->text_sensors_.push_back(sensor);
    }
#endif

#ifdef USE_SWITCH
    void DeyeInverter::register_switch(switch_::Switch *sw)
    {
      this->switches_.push_back(sw);
    }
#endif

#ifdef USE_NUMBER
    void DeyeInverter::register_number(number::Number *num)
    {
      this->numbers_.push_back(num);
    }
#endif

#ifdef USE_SELECT
    void DeyeInverter::register_select(select::Select *sel)
    {
      this->selects_.push_back(sel);
    }
#endif

#ifdef USE_DATETIME
    void DeyeInverter::register_datetime(datetime::DateTimeEntity *dt)
    {
      this->datetimes_.push_back(dt);
    }
#endif

#ifdef USE_TIME
    void DeyeInverter::register_time(time::RealTimeClock *tm)
    {
      this->times_.push_back(tm);
    }
#endif

    // =============================================================================
    // SENSOR METHODS
    // =============================================================================

#ifdef USE_SENSOR
    void DeyeSensor::setup()
    {
      ESP_LOGCONFIG(TAG, "Setting up Deye Sensor at address 0x%04X...", this->address_);
    }

    void DeyeSensor::dump_config()
    {
      ESP_LOGCONFIG(TAG, "Deye Sensor:");
      ESP_LOGCONFIG(TAG, "  Address: 0x%04X", this->address_);
      ESP_LOGCONFIG(TAG, "  Scale: %f", this->scale_);
      ESP_LOGCONFIG(TAG, "  Offset: %f", this->offset_);
    }

    void DeyeSensor::update_value(uint16_t raw_value)
    {
      float value = (static_cast<float>(raw_value) * this->scale_) + this->offset_;
      this->publish_state(value);
    }

    void DeyeSensor::update_value_32(uint32_t raw_value)
    {
      float value = (static_cast<float>(raw_value) * this->scale_) + this->offset_;
      this->publish_state(value);
    }

    void DeyeSensor::update_value_signed(int16_t raw_value)
    {
      float value = (static_cast<float>(raw_value) * this->scale_) + this->offset_;
      this->publish_state(value);
    }

    void DeyeSensor::update_value_32_signed(int32_t raw_value)
    {
      float value = (static_cast<float>(raw_value) * this->scale_) + this->offset_;
      this->publish_state(value);
    }

    void DeyeInverter::update_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
      for (auto *base_sensor : this->sensors_) {
        auto *sensor = static_cast<DeyeSensor*>(base_sensor);
        uint16_t sensor_addr = sensor->get_address();
        uint8_t sensor_bytes = sensor->get_bytes();

        // Check if sensor is within this data block
        if (sensor_addr >= start_address &&
            sensor_addr + (sensor_bytes / 2) <= start_address + (data.size() / 2)) {

          size_t offset = (sensor_addr - start_address) * 2;

          if (sensor_bytes == 4) {
            // 32-bit value
            DataType data_type = sensor->get_data_type();
            bool reversed = (data_type == DataType::U_DWORD_R || data_type == DataType::S_DWORD_R);

            if (data_type == DataType::S_DWORD || data_type == DataType::S_DWORD_R) {
              int32_t raw_value = reversed ? this->parse_int32_r(data, offset) : this->parse_int32(data, offset);
              sensor->update_value_32_signed(raw_value);
            } else {
              uint32_t raw_value = reversed ? this->parse_uint32_r(data, offset) : this->parse_uint32(data, offset);
              sensor->update_value_32(raw_value);
            }
          } else {
            // 16-bit value
            uint16_t raw_value = this->parse_uint16(data, offset);
            DataType data_type = sensor->get_data_type();

            if (data_type == DataType::S_WORD) {
              sensor->update_value_signed(static_cast<int16_t>(raw_value));
            } else {
              sensor->update_value(raw_value);
            }
          }
        }
      }
    }
#endif

    // =============================================================================
    // OTHER ENTITY METHODS
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
          std::string value = this->parse_ascii(data, offset, length);
          sensor->update_string(value);
        }
      }
    }
  }
}

void DeyeInverter::update_serial_number_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  if (start_address > REG_RANGE_SERIAL_END) return;

  for (auto *base_sensor : this->text_sensors_) {
    auto *sensor = static_cast<DeyeTextSensor*>(base_sensor);
    if (!sensor->get_is_serial_number()) continue;

    uint16_t sensor_start = sensor->get_address();
    uint8_t sensor_count = sensor->get_register_count();

    if (sensor_start >= start_address &&
        sensor_start + sensor_count <= start_address + (data.size() / 2)) {
      size_t offset = (sensor_start - start_address) * 2;
      size_t length = sensor_count * 2;

      if (offset + length <= data.size()) {
        std::string value = this->parse_ascii(data, offset, length);
        sensor->update_string(value);
      }
    }
  }
}

void DeyeInverter::update_firmware_info_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  if (start_address > REG_RANGE_FW_INFO_END) return;

  for (auto *base_sensor : this->text_sensors_) {
    auto *sensor = static_cast<DeyeTextSensor*>(base_sensor);
    if (!sensor->get_is_firmware_version() && !sensor->get_is_hardware_version()) continue;

    uint16_t sensor_addr = sensor->get_address();

    if (sensor_addr >= start_address && sensor_addr < start_address + (data.size() / 2)) {
      size_t offset = (sensor_addr - start_address) * 2;

      if (offset + 2 <= data.size()) {
        uint16_t raw_value = this->parse_uint16(data, offset);
        sensor->update_value(raw_value);
      }
    }
  }
}
#endif

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

void DeyeInverter::update_switches_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  for (auto *base_switch : this->switches_) {
    auto *sw = static_cast<DeyeSwitch*>(base_switch);
    uint16_t switch_addr = sw->get_address();

    if (switch_addr >= start_address && switch_addr < start_address + (data.size() / 2)) {
      size_t offset = (switch_addr - start_address) * 2;

      if (offset + 2 <= data.size()) {
        uint16_t reg_value = this->parse_uint16(data, offset);
        sw->update_value(reg_value);
      }
    }
  }
}
#endif

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

  uint16_t year_month_value = (static_cast<uint16_t>(year_offset) << 8) | month;
  uint16_t day_hour_value = (static_cast<uint16_t>(day) << 8) | hour;
  uint16_t minute_second_value = (static_cast<uint16_t>(minute) << 8) | second;

  this->parent_->write_register(REG_SYSTEM_TIME_BYTE1, year_month_value);
  this->parent_->write_register(REG_SYSTEM_TIME_BYTE3, day_hour_value);
  this->parent_->write_register(REG_SYSTEM_TIME_BYTE5, minute_second_value);

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

void DeyeInverter::update_system_time_from_data(uint16_t start_address, const std::vector<uint8_t>& data) {
  if (data.size() < 6) return;

  uint8_t year = data[0];
  uint8_t month = data[1];
  uint8_t day = data[2];
  uint8_t hour = data[3];
  uint8_t minute = data[4];
  uint8_t second = data[5];

  for (auto *base_time : this->times_) {
    auto *time = static_cast<DeyeTime*>(base_time);
    time->on_system_time_received(year, month, day, hour, minute, second);
  }
}
#endif

void DeyeInverter::update_all_entities(uint16_t start_address, const std::vector<uint8_t>& data) {
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

    // =============================================================================
    // WRITE REGISTER METHODS
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
    // UTILITY METHODS
    // =============================================================================

    uint16_t DeyeInverter::parse_uint16(const std::vector<uint8_t> &data, size_t offset)
    {
      if (offset + 2 > data.size())
        return 0;
      return (static_cast<uint16_t>(data[offset]) << 8) | data[offset + 1];
    }

    int16_t DeyeInverter::parse_int16(const std::vector<uint8_t> &data, size_t offset)
    {
      return static_cast<int16_t>(this->parse_uint16(data, offset));
    }

    uint32_t DeyeInverter::parse_uint32(const std::vector<uint8_t> &data, size_t offset)
    {
      if (offset + 4 > data.size())
        return 0;
      return (static_cast<uint32_t>(data[offset]) << 24) |
             (static_cast<uint32_t>(data[offset + 1]) << 16) |
             (static_cast<uint32_t>(data[offset + 2]) << 8) |
             data[offset + 3];
    }

    int32_t DeyeInverter::parse_int32(const std::vector<uint8_t> &data, size_t offset)
    {
      return static_cast<int32_t>(this->parse_uint32(data, offset));
    }

    uint32_t DeyeInverter::parse_uint32_r(const std::vector<uint8_t> &data, size_t offset)
    {
      if (offset + 4 > data.size())
        return 0;
      return (static_cast<uint32_t>(data[offset + 2]) << 24) |
             (static_cast<uint32_t>(data[offset + 3]) << 16) |
             (static_cast<uint32_t>(data[offset]) << 8) |
             data[offset + 1];
    }

    int32_t DeyeInverter::parse_int32_r(const std::vector<uint8_t> &data, size_t offset)
    {
      return static_cast<int32_t>(this->parse_uint32_r(data, offset));
    }

    std::string DeyeInverter::parse_ascii(const std::vector<uint8_t> &data, size_t offset, size_t len)
    {
      if (offset + len > data.size())
        return "";
      std::string result;
      bool all_ff = true;
      for (size_t i = 0; i < len; i++) {
        uint8_t byte = data[offset + i];
        if (byte != 0xFF) {
          all_ff = false;
        }
        // Only accept printable ASCII (0x20-0x7E) and common control chars
        if (byte >= 0x20 && byte < 0x7F) {
          result += static_cast<char>(byte);
        }
      }
      // If all bytes are 0xFF (uninitialized), return "Unknown"
      if (all_ff || result.empty()) {
        return "Unknown";
      }
      return result;
    }

  } // namespace deye_inverter
} // namespace esphome
