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

    void DeyeInverter::handle_time_response(const std::vector<uint8_t> &data, uint16_t start_address)
    {
      // TODO
    }

    void DeyeInverter::handle_live_data_response(const std::vector<uint8_t> &data, uint16_t start_address)
    {
      // TODO
    }

    void DeyeInverter::handle_statistics_response(const std::vector<uint8_t> &data, uint16_t start_address)
    {
      // TODO
    }

    void DeyeInverter::handle_battery_module_response(const std::vector<uint8_t> &data, uint16_t start_address, uint8_t block_index)
    {
      // TODO
    }

    void DeyeInverter::handle_settings_response(const std::vector<uint8_t> &data, uint16_t start_address)
    {
      // TODO
    }

    void DeyeInverter::handle_settings_2_response(const std::vector<uint8_t> &data, uint16_t start_address)
    {
      // TODO
    }

    void DeyeInverter::handle_device_info_response(const std::vector<uint8_t> &data, uint16_t start_address)
    {
      // TODO
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
#endif

    // =============================================================================
    // OTHER ENTITY METHODS
    // =============================================================================

#ifdef USE_BINARY_SENSOR
    void DeyeBinarySensor::setup() {}
    void DeyeBinarySensor::dump_config() {}
#endif

#ifdef USE_TEXT_SENSOR
    void DeyeTextSensor::setup() {}
    void DeyeTextSensor::dump_config() {}
#endif

#ifdef USE_SWITCH
    void DeyeSwitch::setup() {}
    void DeyeSwitch::dump_config() {}
    void DeyeSwitch::write_state(bool state) {}
#endif

#ifdef USE_NUMBER
    void DeyeNumber::setup() {}
    void DeyeNumber::dump_config() {}
    void DeyeNumber::control(float value) {}
#endif

#ifdef USE_SELECT
    void DeyeSelect::setup() {}
    void DeyeSelect::dump_config() {}
    void DeyeSelect::control(const std::string &value) {}
#endif

#ifdef USE_DATETIME
    void DeyeDateTime::setup() {}
    void DeyeDateTime::dump_config() {}
    void DeyeDateTime::update_value(uint16_t year, uint8_t month, uint8_t day, uint8_t hour, uint8_t minute, uint8_t second) {}
#endif

#ifdef USE_TIME
    void DeyeTime::setup() {}
    void DeyeTime::dump_config() {}
    void DeyeTime::update() {}
    void DeyeTime::on_system_time_received(uint8_t year, uint8_t month, uint8_t day,
                                           uint8_t hour, uint8_t minute, uint8_t second) {}
#endif

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
      for (size_t i = 0; i < len; i += 2)
      {
        if (data[offset + i] != 0)
          result += static_cast<char>(data[offset + i]);
        if (data[offset + i + 1] != 0)
          result += static_cast<char>(data[offset + i + 1]);
      }
      return result;
    }

  } // namespace deye_inverter
} // namespace esphome
