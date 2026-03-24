#pragma once

#include "esphome/core/component.h"
#include "esphome/components/modbus_controller/modbus_controller.h"

#ifdef USE_SENSOR
#include "esphome/components/sensor/sensor.h"
#endif
#ifdef USE_BINARY_SENSOR
#include "esphome/components/binary_sensor/binary_sensor.h"
#endif
#ifdef USE_TEXT_SENSOR
#include "esphome/components/text_sensor/text_sensor.h"
#endif
#ifdef USE_SWITCH
#include "esphome/components/switch/switch.h"
#endif
#ifdef USE_NUMBER
#include "esphome/components/number/number.h"
#endif
#ifdef USE_SELECT
#include "esphome/components/select/select.h"
#endif
#ifdef USE_DATETIME
#include "esphome/components/datetime/datetime.h"
#endif
#ifdef USE_TIME
#include "esphome/components/time/real_time_clock.h"
#endif

#include "registers.h"
#include <map>
#include <vector>
#include <string>

namespace esphome {
namespace deye_inverter {

// Forward declarations
class DeyeInverter;
#ifdef USE_SENSOR
class DeyeSensor;
#endif
#ifdef USE_BINARY_SENSOR
class DeyeBinarySensor;
#endif
#ifdef USE_TEXT_SENSOR
class DeyeTextSensor;
#endif
#ifdef USE_SWITCH
class DeyeSwitch;
#endif
#ifdef USE_NUMBER
class DeyeNumber;
#endif
#ifdef USE_SELECT
class DeyeSelect;
#endif
#ifdef USE_DATETIME
class DeyeDateTime;
#endif
#ifdef USE_TIME
class DeyeTime;
#endif

// =============================================================================
// DATA TYPES
// =============================================================================
enum class DataType {
  U_WORD,      // Unsigned 16-bit (single register)
  S_WORD,      // Signed 16-bit
  U_DWORD_R,   // Unsigned 32-bit (2 registers, reversed order)
  S_DWORD_R,   // Signed 32-bit (reversed)
  U_DWORD,     // Unsigned 32-bit (normal order)
  S_DWORD,     // Signed 32-bit (normal)
  ASCII,       // ASCII string
  BITMASK,     // Bitmask for flags
};

// =============================================================================
// DEYE INVERTER CLASS
// =============================================================================
class DeyeInverter : public modbus_controller::ModbusController {
 public:
  // Update intervals (in ms)
  uint32_t interval_time_{60000};          // Time sync interval
  uint32_t interval_live_{1000};
  uint32_t interval_statistics_{5000};
  uint32_t interval_settings_{60000};
  uint32_t interval_system_settings_{120000};
  uint32_t interval_grid_protection_{120000};
  uint32_t interval_extended_settings_{120000};
  uint32_t interval_california_settings_{300000};
  uint32_t interval_battery_modules_{5000};
  uint32_t interval_device_info_{300000};

  void setup() override;
  void update() override;
  void dump_config() override;

  // Setter methods for update intervals
  void set_update_interval(uint32_t interval) { interval_live_ = interval; }
  void set_update_interval_time(uint32_t interval) { interval_time_ = interval; }
  void set_update_interval_live(uint32_t interval) { interval_live_ = interval; }
  void set_update_interval_statistics(uint32_t interval) { interval_statistics_ = interval; }
  void set_update_interval_settings(uint32_t interval) { interval_settings_ = interval; }
  void set_update_interval_system_settings(uint32_t interval) { interval_system_settings_ = interval; }
  void set_update_interval_grid_protection(uint32_t interval) { interval_grid_protection_ = interval; }
  void set_update_interval_extended_settings(uint32_t interval) { interval_extended_settings_ = interval; }
  void set_update_interval_california_settings(uint32_t interval) { interval_california_settings_ = interval; }
  void set_update_interval_battery_modules(uint32_t interval) { interval_battery_modules_ = interval; }
  void set_update_interval_device_info(uint32_t interval) { interval_device_info_ = interval; }

  // Register entities with the component
  void register_sensor(sensor::Sensor *sensor);
  void register_binary_sensor(binary_sensor::BinarySensor *sensor);
  void register_text_sensor(text_sensor::TextSensor *sensor);
  void register_switch(switch_::Switch *sw);
#ifdef USE_NUMBER
  void register_number(number::Number *num);
#endif
  void register_select(select::Select *sel);
#ifdef USE_DATETIME
  void register_datetime(datetime::DateTimeEntity *dt);
#endif
  void register_time(time::RealTimeClock *tm);

  // Write methods using modbus_controller
  void write_register(uint16_t address, uint16_t value);
  void write_register_masked(uint16_t address, uint16_t value, uint16_t mask);

  // Static helper methods
  static DataType parse_data_type(const std::string& str);
  static float convert_value(uint16_t raw, DataType type, float scale, float offset);
  static float convert_value_32(uint32_t raw, DataType type, float scale, float offset);
  static std::string format_time_point(uint16_t value);
  static std::string format_version(uint16_t value);
  static std::string parse_firmware_version(const std::vector<uint8_t>& data, size_t offset);

  // Data parsing helpers
  float parse_value(const std::vector<uint8_t>& data, size_t offset,
                    uint8_t bytes, DataType data_type, float scale, float offset_val);
  int16_t parse_int16_value(const std::vector<uint8_t>& data, size_t offset);
  int32_t parse_int32_value(const std::vector<uint8_t>& data, size_t offset, bool reversed);
  uint32_t parse_uint32(const std::vector<uint8_t>& data, size_t offset, bool reversed);
  int32_t parse_int32(const std::vector<uint8_t>& data, size_t offset, bool is_signed);
  int16_t parse_int16(const std::vector<uint8_t>& data, size_t offset, bool is_signed);
  uint16_t parse_uint16(const std::vector<uint8_t>& data, size_t offset);
  std::string parse_string(const std::vector<uint8_t>& data, size_t offset, size_t length);

  // Request queue management (following ds100_meter pattern)
  // Priority order: TIME → LIVEDATA → STATISTICS → SETTINGS → DEVICE_INFO
  enum class RequestType : uint8_t {
    TIME = 0,               // Highest priority - system time sync
    LIVEDATA = 1,           // Real-time data
    STATISTICS = 2,         // Energy statistics
    BATTERY_MODULES = 3,    // Battery module data
    SETTINGS = 4,           // Device settings
    SYSTEM_SETTINGS = 5,    // System configuration
    GRID_PROTECTION = 6,    // Grid protection settings
    EXTENDED_SETTINGS = 7,  // Extended monitoring settings
    CALIFORNIA_SETTINGS = 8,// California compliance settings
    DEVICE_INFO = 9,        // Device information (lowest priority)
  };

  void queue_request(RequestType type);
  RequestType get_highest_priority_pending();
  void process_next_request();

  // Response handlers for ModbusCommandItem callbacks
  // Priority order: TIME → LIVEDATA → STATISTICS → SETTINGS → DEVICE_INFO
  void handle_time_response(const std::vector<uint8_t> &data, uint16_t start_address);
  void handle_live_data_response(const std::vector<uint8_t> &data, uint16_t start_address);
  void handle_statistics_response(const std::vector<uint8_t> &data, uint16_t start_address);
  void handle_battery_module_response(const std::vector<uint8_t> &data, uint16_t start_address, uint8_t module_index);
  void handle_settings_response(const std::vector<uint8_t> &data, uint16_t start_address);
  void handle_system_settings_response(const std::vector<uint8_t> &data, uint16_t start_address);
  void handle_grid_protection_response(const std::vector<uint8_t> &data, uint16_t start_address);
  void handle_extended_settings_response(const std::vector<uint8_t> &data, uint16_t start_address);
  void handle_california_settings_response(const std::vector<uint8_t> &data, uint16_t start_address);
  void handle_device_info_response(const std::vector<uint8_t> &data, uint16_t start_address);

 protected:
  // Entity storage - using base types but storing Deye specialized classes
#ifdef USE_SENSOR
  std::vector<sensor::Sensor *> sensors_;
#endif
#ifdef USE_BINARY_SENSOR
  std::vector<binary_sensor::BinarySensor *> binary_sensors_;
#endif
#ifdef USE_TEXT_SENSOR
  std::vector<text_sensor::TextSensor *> text_sensors_;
#endif
#ifdef USE_SWITCH
  std::vector<switch_::Switch *> switches_;
#endif
#ifdef USE_NUMBER
  std::vector<number::Number *> numbers_;
#endif
#ifdef USE_SELECT
  std::vector<select::Select *> selects_;
#endif
#ifdef USE_DATETIME
  std::vector<datetime::DateTimeEntity *> datetimes_;
#endif
#ifdef USE_TIME
  std::vector<time::RealTimeClock *> times_;
#endif

  // Static register range arrays
  static const RegisterRange LIVE_RANGES[];
  static const RegisterRange STATS_RANGES[];
  static const RegisterRange SETTINGS_RANGES[];
  static const RegisterRange SETTINGS_SYSTEM_RANGES[];
  static const RegisterRange SETTINGS_GRID_PROTECTION_RANGES[];
  static const RegisterRange SETTINGS_EXTENDED_RANGES[];
  static const RegisterRange SETTINGS_CALIFORNIA_RANGES[];
  static const RegisterRange BATTERY_MODULE_RANGES[];
  static const RegisterRange DEVICE_INFO_RANGES[];

  // Range counts
  static constexpr size_t LIVE_RANGES_COUNT = 11;
  static constexpr size_t STATS_RANGES_COUNT = 4;
  static constexpr size_t SETTINGS_RANGES_COUNT = 12;  // Adjusted based on actual array
  static constexpr size_t SETTINGS_SYSTEM_RANGES_COUNT = 4;
  static constexpr size_t SETTINGS_GRID_PROTECTION_RANGES_COUNT = 2;
  static constexpr size_t SETTINGS_EXTENDED_RANGES_COUNT = 6;
  static constexpr size_t SETTINGS_CALIFORNIA_RANGES_COUNT = 6;
  static constexpr size_t BATTERY_MODULE_RANGES_COUNT = 9;
  static constexpr size_t DEVICE_INFO_RANGES_COUNT = 4;

  // Timing variables
  uint32_t last_time_update_{0};
  uint32_t last_live_update_{0};
  uint32_t last_stats_update_{0};
  uint32_t last_settings_update_{0};
  uint32_t last_system_settings_update_{0};
  uint32_t last_grid_protection_update_{0};
  uint32_t last_extended_settings_update_{0};
  uint32_t last_california_settings_update_{0};
  uint32_t last_battery_modules_update_{0};
  uint32_t last_device_info_update_{0};

  // State tracking
  bool device_info_initialized_{false};
  
  // Pending requests bitmask (following ds100_meter pattern)
  static const uint16_t PENDING_TIME = 0x0001;            // Highest priority
  static const uint16_t PENDING_LIVEDATA = 0x0002;
  static const uint16_t PENDING_STATISTICS = 0x0004;
  static const uint16_t PENDING_BATTERY_MODULES = 0x0008;
  static const uint16_t PENDING_SETTINGS = 0x0010;
  static const uint16_t PENDING_SYSTEM_SETTINGS = 0x0020;
  static const uint16_t PENDING_GRID_PROTECTION = 0x0040;
  static const uint16_t PENDING_EXTENDED_SETTINGS = 0x0080;
  static const uint16_t PENDING_CALIFORNIA_SETTINGS = 0x0100;
  static const uint16_t PENDING_DEVICE_INFO = 0x0200;

  uint16_t pending_requests_{0};      // Bitmask of pending request types
  bool request_in_progress_{false};   // True if waiting for Modbus response
  uint32_t last_request_time_{0};     // Timestamp of last request for timeout tracking

  // Current request type being processed
  RequestType current_request_type_{RequestType::LIVEDATA};

  // Range index tracking for phased requests (queue one range at a time)
  size_t current_range_index_{0};              // For LIVEDATA ranges
  size_t current_battery_module_range_{0};     // For BATTERY_MODULES ranges

  // Consecutive timeout tracking (following ds100_meter pattern)
  uint8_t consecutive_timeouts_{0};
  static const uint8_t MAX_CONSECUTIVE_TIMEOUTS = 3;

  // Entity update methods
#ifdef USE_SENSOR
  void update_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_battery_module_sensors(uint16_t start_address, const std::vector<uint8_t>& data);
#endif
#ifdef USE_BINARY_SENSOR
  void update_binary_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
#endif
#ifdef USE_TEXT_SENSOR
  void update_text_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_serial_number_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_firmware_info_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
#endif
#ifdef USE_SWITCH
  void update_switches_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
#endif
#ifdef USE_NUMBER
  void update_numbers_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
#endif
#ifdef USE_SELECT
  void update_selects_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
#endif
#ifdef USE_DATETIME
  void update_datetimes_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
#endif
#ifdef USE_TIME
  void update_system_time_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
#endif

  // Battery module helper
  float parse_battery_module_value(const std::vector<uint8_t>& data, size_t offset, 
                                   uint8_t module_index, uint8_t cell_index, 
                                   bool is_cell_voltage);

  // Helper to send register range read command
  void send_register_range_read(const RegisterRange& range);
};

// =============================================================================
// SENSOR CLASS
// =============================================================================
#ifdef USE_SENSOR
class DeyeSensor : public sensor::Sensor, public Component {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void set_parent(DeyeInverter *parent) { parent_ = parent; }
  void set_address(uint16_t address) { address_ = address; }
  void set_scale(float scale) { scale_ = scale; }
  void set_offset(float offset) { offset_ = offset; }
  void set_data_type(DataType data_type) { data_type_ = data_type; }
  void set_bytes(uint8_t bytes) { bytes_ = bytes; }
  void set_signed(bool signed_val) { signed_ = signed_val; }
  void set_is_battery_module(bool is_module) { is_battery_module_ = is_module; }
  void set_module_index(uint8_t index) { module_index_ = index; }
  void set_is_cell_voltage(bool is_cell) { is_cell_voltage_ = is_cell; }
  void set_cell_index(uint8_t index) { cell_index_ = index; }

  uint16_t get_address() const { return address_; }
  uint8_t get_bytes() const { return bytes_; }
  DataType get_data_type() const { return data_type_; }
  bool get_is_battery_module() const { return is_battery_module_; }
  uint8_t get_module_index() const { return module_index_; }
  bool get_is_cell_voltage() const { return is_cell_voltage_; }
  uint8_t get_cell_index() const { return cell_index_; }

  void update_value(uint16_t raw_value);
  void update_value_32(uint32_t raw_value);
  void update_value_signed(int16_t raw_value);
  void update_value_32_signed(int32_t raw_value);

 protected:
  DeyeInverter *parent_{nullptr};
  uint16_t address_{0};
  float scale_{1.0f};
  float offset_{0.0f};
  DataType data_type_{DataType::U_WORD};
  uint8_t bytes_{2};
  bool signed_{false};
  bool is_battery_module_{false};
  uint8_t module_index_{0};
  bool is_cell_voltage_{false};
  uint8_t cell_index_{0};
};
#endif

// =============================================================================
// BINARY SENSOR CLASS
// =============================================================================
#ifdef USE_BINARY_SENSOR
class DeyeBinarySensor : public binary_sensor::BinarySensor, public Component {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void set_parent(DeyeInverter *parent) { parent_ = parent; }
  void set_address(uint16_t address) { address_ = address; }
  void set_bitmask(uint16_t bitmask) { bitmask_ = bitmask; }

  uint16_t get_address() const { return address_; }

  void update_value(uint16_t raw_value);

 protected:
  DeyeInverter *parent_{nullptr};
  uint16_t address_{0};
  uint16_t bitmask_{0xFFFF};
};
#endif

// =============================================================================
// TEXT SENSOR CLASS
// =============================================================================
#ifdef USE_TEXT_SENSOR
class DeyeTextSensor : public text_sensor::TextSensor, public Component {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void set_parent(DeyeInverter *parent) { parent_ = parent; }
  void set_address(uint16_t address) { address_ = address; }
  void set_is_status(bool is_status) { is_status_ = is_status; }
  void set_is_device_type(bool is_device_type) { is_device_type_ = is_device_type; }
  void set_is_serial_number(bool is_serial) { is_serial_number_ = is_serial; }
  void set_is_firmware_version(bool is_firmware) { is_firmware_version_ = is_firmware; }
  void set_is_hardware_version(bool is_hardware) { is_hardware_version_ = is_hardware; }
  void set_is_time_point(bool is_time) { is_time_point_ = is_time; }
  void set_register_count(uint8_t count) { register_count_ = count; }
  void set_mapping(const std::map<uint16_t, std::string>& mapping) { mapping_ = mapping; }

  uint16_t get_address() const { return address_; }
  uint8_t get_register_count() const { return register_count_; }
  bool get_is_serial_number() const { return is_serial_number_; }
  bool get_is_firmware_version() const { return is_firmware_version_; }
  bool get_is_hardware_version() const { return is_hardware_version_; }
  bool get_is_time_point() const { return is_time_point_; }
  bool get_is_status() const { return is_status_; }
  bool get_is_device_type() const { return is_device_type_; }

  void update_value(uint16_t raw_value);
  void update_string(const std::string& value);

 protected:
  DeyeInverter *parent_{nullptr};
  uint16_t address_{0};
  bool is_status_{false};
  bool is_device_type_{false};
  bool is_serial_number_{false};
  bool is_firmware_version_{false};
  bool is_hardware_version_{false};
  bool is_time_point_{false};
  uint8_t register_count_{1};
  std::map<uint16_t, std::string> mapping_;
};
#endif

// =============================================================================
// SWITCH CLASS
// =============================================================================
#ifdef USE_SWITCH
class DeyeSwitch : public switch_::Switch, public Component {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void set_parent(DeyeInverter *parent) { parent_ = parent; }
  void set_address(uint16_t address) { address_ = address; }
  void set_bitmask(uint16_t bitmask) { bitmask_ = bitmask; }
  void set_is_2bit_field(bool is_2bit) { is_2bit_field_ = is_2bit; }
  void set_value_enable(uint16_t value) { value_enable_ = value; }
  void set_value_disable(uint16_t value) { value_disable_ = value; }
  void set_bit_shift(uint8_t shift) { bit_shift_ = shift; }

  uint16_t get_address() const { return address_; }

  void update_value(uint16_t raw_value);
  void write_state(bool state) override;

 protected:
  DeyeInverter *parent_{nullptr};
  uint16_t address_{0};
  uint16_t bitmask_{0x0001};
  bool is_2bit_field_{false};
  uint16_t value_enable_{0x03};
  uint16_t value_disable_{0x02};
  uint8_t bit_shift_{0};
};
#endif

// =============================================================================
// NUMBER CLASS
// =============================================================================
#ifdef USE_NUMBER
class DeyeNumber : public number::Number, public Component {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void set_parent(DeyeInverter *parent) { parent_ = parent; }
  void set_address(uint16_t address) { address_ = address; }
  void set_scale(float scale) { scale_ = scale; }
  void set_offset(float offset) { offset_ = offset; }
  void set_data_type(DataType data_type) { data_type_ = data_type; }
  void set_is_time_point(bool is_time) { is_time_point_ = is_time; }

  uint16_t get_address() const { return address_; }

  void update_value(uint16_t raw_value);
  void control(float value) override;

 protected:
  DeyeInverter *parent_{nullptr};
  uint16_t address_{0};
  float scale_{1.0f};
  float offset_{0.0f};
  DataType data_type_{DataType::U_WORD};
  bool is_time_point_{false};
};
#endif

// =============================================================================
// SELECT CLASS
// =============================================================================
#ifdef USE_SELECT
class DeyeSelect : public select::Select, public Component {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void set_parent(DeyeInverter *parent) { parent_ = parent; }
  void set_address(uint16_t address) { address_ = address; }
  void set_options_map(const std::map<uint16_t, std::string>& options) { 
    options_map_ = options; 
    // Build reverse map
    for (const auto& pair : options) {
      reverse_map_[pair.second] = pair.first;
    }
  }

  uint16_t get_address() const { return address_; }

  void update_value(uint16_t raw_value);
  void control(const std::string &value) override;

 protected:
  DeyeInverter *parent_{nullptr};
  uint16_t address_{0};
  std::map<uint16_t, std::string> options_map_;
  std::map<std::string, uint16_t> reverse_map_;
};
#endif

// =============================================================================
// DATETIME CLASS
// =============================================================================
#ifdef USE_DATETIME
class DeyeDateTime : public datetime::DateTimeEntity, public Component {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void set_parent(DeyeInverter *parent) { parent_ = parent; }
  void set_address(uint16_t address) { address_ = address; }
  void set_is_time(bool is_time) { is_time_ = is_time; }

  uint16_t get_address() const { return address_; }

  void update_value(uint16_t raw_value);
  void control(const datetime::DateTimeCall &call) override;

  static void parse_hhmm(uint16_t value, uint8_t& hour, uint8_t& minute);
  static uint16_t format_hhmm(uint8_t hour, uint8_t minute);

 protected:
  DeyeInverter *parent_{nullptr};
  uint16_t address_{0};
  bool is_time_{false};
};
#endif

// =============================================================================
// TIME CLASS (for system time sync)
// =============================================================================
#ifdef USE_TIME
class DeyeTime : public time::RealTimeClock {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void set_parent(DeyeInverter *parent) { parent_ = parent; }
  void set_max_time_diff(uint32_t max_time_diff) { max_time_diff_ = max_time_diff; }
  void update() override;

  void on_system_time_received(uint8_t year, uint8_t month, uint8_t day,
                               uint8_t hour, uint8_t minute, uint8_t second);

 protected:
  DeyeInverter *parent_{nullptr};
  uint32_t max_time_diff_{10000};  // 10 seconds default
  bool inverter_time_valid_{false};
  ESPTime inverter_time_;
  bool time_just_set_{false};

  void sync_time_if_needed();
  void write_time_to_inverter();
};
#endif

}  // namespace deye_inverter
}  // namespace esphome
