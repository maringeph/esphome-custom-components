#pragma once

#include "esphome/core/component.h"
#include "esphome/components/modbus_controller/modbus_controller.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/number/number.h"
#include "esphome/components/select/select.h"
#include "esphome/components/datetime/datetime.h"
#include "esphome/components/time/real_time_clock.h"
#include "registers.h"
#include <map>
#include <vector>
#include <string>

namespace esphome {
namespace deye_inverter {

// Forward declarations
class DeyeInverter;
class DeyeSensor;
class DeyeBinarySensor;
class DeyeTextSensor;
class DeyeSwitch;
class DeyeNumber;
class DeyeSelect;
class DeyeDateTime;
class DeyeTime;

// =============================================================================
// DATA TYPE ENUM
// =============================================================================
enum class DataType {
  U_WORD,      // Unsigned 16-bit
  S_WORD,      // Signed 16-bit
  U_DWORD,     // Unsigned 32-bit (high-low)
  U_DWORD_R,   // Unsigned 32-bit (low-high, reversed)
  BITMASK,     // Bitmask for switches/binary sensors
  S_DWORD,     // Signed 32-bit (high-low)
  S_DWORD_R    // Signed 32-bit (low-high, reversed)
};

// =============================================================================
// REGISTER INFO STRUCT
// =============================================================================
struct RegisterInfo {
  uint16_t address;
  const char* name;
  DataType data_type;
  float scale;
  float offset;
  uint16_t bitmask;
  bool is_time_point;  // Special formatting for time values (HHMM)
  bool is_string;      // String data (multiple registers as text)
};

// =============================================================================
// SENSOR PLATFORM
// =============================================================================
class DeyeSensor : public sensor::Sensor, public Component {
 public:
  void set_parent(DeyeInverter* parent) { this->parent_ = parent; }
  void set_address(uint16_t address) { this->address_ = address; }
  void set_scale(float scale) { this->scale_ = scale; }
  void set_offset(float offset) { this->offset_ = offset; }
  void set_data_type(DataType data_type) { this->data_type_ = data_type; }
  void set_bytes(uint8_t bytes) { this->bytes_ = bytes; }
  void set_is_battery_module(bool is_battery_module) { this->is_battery_module_ = is_battery_module; }
  void set_module_index(uint8_t index) { this->module_index_ = index; }
  void set_is_cell_voltage(bool is_cell_voltage) { this->is_cell_voltage_ = is_cell_voltage; }
  void set_cell_index(uint8_t index) { this->cell_index_ = index; }
  
  uint16_t get_address() const { return address_; }
  float get_scale() const { return scale_; }
  float get_offset() const { return offset_; }
  DataType get_data_type() const { return data_type_; }
  uint8_t get_bytes() const { return bytes_; }
  bool get_is_battery_module() const { return is_battery_module_; }
  uint8_t get_module_index() const { return module_index_; }
  bool get_is_cell_voltage() const { return is_cell_voltage_; }
  uint8_t get_cell_index() const { return cell_index_; }
  
  void update_value(uint16_t raw_value);
  void update_value_32(uint32_t raw_value);
  void update_value_signed(int16_t raw_value);
  void update_value_32_signed(int32_t raw_value);
  
 protected:
  DeyeInverter* parent_ = nullptr;
  uint16_t address_ = 0;
  float scale_ = 1.0f;
  float offset_ = 0.0f;
  DataType data_type_ = DataType::U_WORD;
  uint8_t bytes_ = 2;  // 2 = 16-bit, 4 = 32-bit
  bool is_battery_module_ = false;
  uint8_t module_index_ = 0;
  bool is_cell_voltage_ = false;
  uint8_t cell_index_ = 0;
};

// =============================================================================
// BINARY SENSOR PLATFORM
// =============================================================================
class DeyeBinarySensor : public binary_sensor::BinarySensor, public Component {
 public:
  void set_parent(DeyeInverter* parent) { this->parent_ = parent; }
  void set_address(uint16_t address) { this->address_ = address; }
  void set_bitmask(uint16_t bitmask) { this->bitmask_ = bitmask; }
  
  uint16_t get_address() const { return address_; }
  uint16_t get_bitmask() const { return bitmask_; }
  
  void update_value(uint16_t raw_value);
  
 protected:
  DeyeInverter* parent_ = nullptr;
  uint16_t address_ = 0;
  uint16_t bitmask_ = 0xFFFF;
};

// =============================================================================
// TEXT SENSOR PLATFORM
// =============================================================================
class DeyeTextSensor : public text_sensor::TextSensor, public Component {
 public:
  void set_parent(DeyeInverter* parent) { this->parent_ = parent; }
  void set_address(uint16_t address) { this->address_ = address; }
  void set_register_count(uint8_t count) { this->register_count_ = count; }
  void set_is_status(bool is_status) { this->is_status_ = is_status; }
  void set_is_device_type(bool is_device_type) { this->is_device_type_ = is_device_type; }
  void set_is_time_point(bool is_time_point) { this->is_time_point_ = is_time_point; }
  void set_is_serial_number(bool is_serial_number) { this->is_serial_number_ = is_serial_number; }
  void set_is_firmware_version(bool is_firmware_version) { this->is_firmware_version_ = is_firmware_version; }
  void set_is_hardware_version(bool is_hardware_version) { this->is_hardware_version_ = is_hardware_version; }
  void set_mapping(const std::map<uint16_t, std::string>& mapping) { this->mapping_ = mapping; }
  
  uint16_t get_address() const { return address_; }
  uint8_t get_register_count() const { return register_count_; }
  bool get_is_status() const { return is_status_; }
  bool get_is_device_type() const { return is_device_type_; }
  bool get_is_time_point() const { return is_time_point_; }
  bool get_is_serial_number() const { return is_serial_number_; }
  bool get_is_firmware_version() const { return is_firmware_version_; }
  bool get_is_hardware_version() const { return is_hardware_version_; }
  
  void update_value(uint16_t raw_value);
  void update_string(const std::string& value);
  
 protected:
  DeyeInverter* parent_ = nullptr;
  uint16_t address_ = 0;
  uint8_t register_count_ = 1;
  bool is_status_ = false;
  bool is_device_type_ = false;
  bool is_time_point_ = false;
  bool is_serial_number_ = false;
  bool is_firmware_version_ = false;
  bool is_hardware_version_ = false;
  std::map<uint16_t, std::string> mapping_;
};

// =============================================================================
// SWITCH PLATFORM
// =============================================================================
class DeyeSwitch : public switch_::Switch, public Component {
 public:
  void set_parent(DeyeInverter* parent) { this->parent_ = parent; }
  void set_address(uint16_t address) { this->address_ = address; }
  void set_bitmask(uint16_t bitmask) { this->bitmask_ = bitmask; }
  void set_is_2bit_field(bool is_2bit) { this->is_2bit_field_ = is_2bit; }
  void set_value_enable(uint16_t value) { this->value_enable_ = value; }
  void set_value_disable(uint16_t value) { this->value_disable_ = value; }
  void set_bit_shift(uint8_t shift) { this->bit_shift_ = shift; }
  
  uint16_t get_address() const { return address_; }
  uint16_t get_bitmask() const { return bitmask_; }
  bool get_is_2bit_field() const { return is_2bit_field_; }
  uint16_t get_value_enable() const { return value_enable_; }
  uint16_t get_value_disable() const { return value_disable_; }
  uint8_t get_bit_shift() const { return bit_shift_; }
  
  void update_value(uint16_t raw_value);
  
 protected:
  void write_state(bool state) override;
  
  DeyeInverter* parent_ = nullptr;
  uint16_t address_ = 0;
  uint16_t bitmask_ = 0x0001;
  bool is_2bit_field_ = false;  // True for 2-bit fields (Special Functions)
  uint16_t value_enable_ = 0x0003;   // 11 = enable
  uint16_t value_disable_ = 0x0002;  // 10 = disable
  uint8_t bit_shift_ = 0;
};

// =============================================================================
// NUMBER PLATFORM
// =============================================================================
class DeyeNumber : public number::Number, public Component {
 public:
  void set_parent(DeyeInverter* parent) { this->parent_ = parent; }
  void set_address(uint16_t address) { this->address_ = address; }
  void set_scale(float scale) { this->scale_ = scale; }
  void set_is_time_point(bool is_time_point) { this->is_time_point_ = is_time_point; }
  
  uint16_t get_address() const { return address_; }
  float get_scale() const { return scale_; }
  bool get_is_time_point() const { return is_time_point_; }
  
  void update_value(uint16_t raw_value);
  
 protected:
  void control(float value) override;
  
  DeyeInverter* parent_ = nullptr;
  uint16_t address_ = 0;
  float scale_ = 1.0f;
  bool is_time_point_ = false;
};

// =============================================================================
// SELECT PLATFORM
// =============================================================================
class DeyeSelect : public select::Select, public Component {
 public:
  void set_parent(DeyeInverter* parent) { this->parent_ = parent; }
  void set_address(uint16_t address) { this->address_ = address; }
  void set_options_map(const std::map<uint16_t, std::string>& options) { 
    this->options_map_ = options;
    // Build reverse map
    for (const auto& pair : options) {
      this->reverse_map_[pair.second] = pair.first;
    }
  }
  
  uint16_t get_address() const { return address_; }
  const std::map<uint16_t, std::string>& get_options_map() const { return options_map_; }
  const std::map<std::string, uint16_t>& get_reverse_map() const { return reverse_map_; }
  
  void update_value(uint16_t raw_value);
  
 protected:
  void control(const std::string& value) override;
  
  DeyeInverter* parent_ = nullptr;
  uint16_t address_ = 0;
  std::map<uint16_t, std::string> options_map_;
  std::map<std::string, uint16_t> reverse_map_;
};

// =============================================================================
// DATETIME PLATFORM - For Time of Use start times
// =============================================================================
class DeyeDateTime : public datetime::DateTime, public Component {
 public:
  void set_parent(DeyeInverter* parent) { this->parent_ = parent; }
  void set_address(uint16_t address) { this->address_ = address; }
  
  uint16_t get_address() const { return address_; }
  
  void update_value(uint16_t raw_value);
  
 protected:
  void control(const datetime::DateTimeCall& call) override;
  
  // Convert HHMM register value to time components
  static void parse_hhmm(uint16_t value, uint8_t& hour, uint8_t& minute);
  // Convert time components to HHMM register value
  static uint16_t format_hhmm(uint8_t hour, uint8_t minute);
  
  DeyeInverter* parent_ = nullptr;
  uint16_t address_ = 0;
};

// =============================================================================
// TIME PLATFORM - For System Time synchronization to inverter (registers 62-64)
// =============================================================================
class DeyeTime : public time::RealTimeClock, public Component {
 public:
  void set_parent(DeyeInverter* parent) { this->parent_ = parent; }
  void set_max_time_diff(uint32_t max_time_diff) { this->max_time_diff_ = max_time_diff; }

  void setup() override;
  void dump_config() override;
  
  // Called when inverter sends system time data (registers 62-64)
  // This triggers the sync check automatically
  void on_system_time_received(uint8_t year, uint8_t month, uint8_t day, 
                               uint8_t hour, uint8_t minute, uint8_t second);

  // Public method for manual time sync (called by action)
  void write_time_to_inverter();

 protected:
  void sync_time_if_needed();

  DeyeInverter* parent_ = nullptr;
  uint32_t max_time_diff_ = 10000;  // Max allowed diff: 10 seconds (default)
  bool time_just_set_ = false;      // True when local time was just set
  
  // Cached inverter time for comparison
  bool inverter_time_valid_ = false;
  time::ESPTime inverter_time_;
};

// =============================================================================
// ACTION: Write Time to Inverter
// =============================================================================
template<typename... Ts> class DeyeTimeWriteAction : public Action<Ts...> {
 public:
  DeyeTimeWriteAction(DeyeTime *time) : time_(time) {}
  void play(Ts... x) override {
    if (this->time_ != nullptr) {
      this->time_->write_time_to_inverter();
    }
  }
 protected:
  DeyeTime *time_;
};

// =============================================================================
// MAIN DEYE INVERTER CLASS
// =============================================================================
class DeyeInverter : public Component, public modbus_controller::ModbusDevice {
 public:
  void setup() override;
  void loop() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  
  // Modbus Callbacks
  void on_modbus_data(const std::vector<uint8_t>& data);
  void on_modbus_error(uint8_t function_code, uint8_t exception_code);
  
  // Configuration
  void set_modbus_controller(modbus_controller::ModbusController* controller) { 
    this->modbus_controller_ = controller; 
  }
  void set_address(uint8_t address) { this->address_ = address; }
  void set_name(const std::string& name) { this->name_ = name; }
  
  // Update Intervals
  void set_update_interval_live(uint32_t interval) { this->interval_live_ = interval; }
  void set_update_interval_statistics(uint32_t interval) { this->interval_statistics_ = interval; }
  void set_update_interval_settings(uint32_t interval) { this->interval_settings_ = interval; }
  void set_update_interval_system_settings(uint32_t interval) { this->interval_system_settings_ = interval; }
  void set_update_interval_grid_protection(uint32_t interval) { this->interval_grid_protection_ = interval; }
  void set_update_interval_extended_settings(uint32_t interval) { this->interval_extended_settings_ = interval; }
  void set_update_interval_california_settings(uint32_t interval) { this->interval_california_settings_ = interval; }
  void set_update_interval_battery_modules(uint32_t interval) { this->interval_battery_modules_ = interval; }
  void set_update_interval_device_info(uint32_t interval) { this->interval_device_info_ = interval; }
  
  // Platform Registration
  void register_sensor(DeyeSensor* sensor) { sensors_.push_back(sensor); }
  void register_binary_sensor(DeyeBinarySensor* sensor) { binary_sensors_.push_back(sensor); }
  void register_text_sensor(DeyeTextSensor* sensor) { text_sensors_.push_back(sensor); }
  void register_switch(DeyeSwitch* sw) { switches_.push_back(sw); }
  void register_number(DeyeNumber* num) { numbers_.push_back(num); }
  void register_select(DeyeSelect* sel) { selects_.push_back(sel); }
  void register_datetime(DeyeDateTime* dt) { datetimes_.push_back(dt); }
  void register_time(DeyeTime* tm) { times_.push_back(tm); }
  
  // Write Methods
  void write_register(uint16_t address, uint16_t value);
  void write_register_masked(uint16_t address, uint16_t value, uint16_t mask);
  
  // Update Methods
  void update_register_range(const RegisterRange& range);
  
  // Data type helpers
  static DataType parse_data_type(const std::string& str);
  static float convert_value(uint16_t raw, DataType type, float scale, float offset);
  static float convert_value_32(uint32_t raw, DataType type, float scale, float offset);
  static std::string format_time_point(uint16_t value);
  static std::string format_version(uint16_t value);
  static std::string parse_firmware_version(const std::vector<uint8_t>& data, size_t offset);

  // Battery module helpers
  void update_battery_module_sensors(uint16_t start_address, const std::vector<uint8_t>& data);
  float parse_battery_module_value(const std::vector<uint8_t>& data, size_t offset, uint8_t module_index, 
                                   uint8_t cell_index = 0xff, bool is_cell_voltage = false);

 protected:
  // Update phases
  void update_live_data();
  void update_statistics();
  void update_settings();
  void update_system_settings();
  void update_grid_protection();
  void update_extended_settings();
  void update_california_settings();
  void update_battery_modules();
  void update_device_info();
  
  // Data parsing helpers
  float parse_value(const std::vector<uint8_t>& data, size_t offset, 
                    uint8_t bytes, DataType data_type, float scale, float offset);
  int16_t parse_int16_value(const std::vector<uint8_t>& data, size_t offset);
  int32_t parse_int32_value(const std::vector<uint8_t>& data, size_t offset, bool reversed);
  uint32_t parse_uint32(const std::vector<uint8_t>& data, size_t offset, bool reversed);
  int32_t parse_int32(const std::vector<uint8_t>& data, size_t offset, bool is_signed);
  int16_t parse_int16(const std::vector<uint8_t>& data, size_t offset, bool is_signed);
  uint16_t parse_uint16(const std::vector<uint8_t>& data, size_t offset);
  std::string parse_string(const std::vector<uint8_t>& data, size_t offset, size_t length);
  
  // Sensor update methods
  void update_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_binary_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_text_sensors_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_switches_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_numbers_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_selects_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_datetimes_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_system_time_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_serial_number_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  void update_firmware_info_from_data(uint16_t start_address, const std::vector<uint8_t>& data);
  
  // Configuration
  std::string name_;
  uint8_t address_ = 1;
  modbus_controller::ModbusController* modbus_controller_ = nullptr;
  
  // Update intervals
  uint32_t interval_live_ = 1000;              // 1 second
  uint32_t interval_statistics_ = 5000;        // 5 seconds
  uint32_t interval_settings_ = 60000;         // 60 seconds
  uint32_t interval_system_settings_ = 120000;     // 2 minutes
  uint32_t interval_grid_protection_ = 120000;     // 2 minutes
  uint32_t interval_extended_settings_ = 120000;   // 2 minutes
  uint32_t interval_california_settings_ = 300000; // 5 minutes
  uint32_t interval_battery_modules_ = 5000;       // 5 seconds
  uint32_t interval_device_info_ = 300000;         // 5 minutes (read once at startup, then rarely)
  
  // Timing
  uint32_t last_live_update_ = 0;
  uint32_t last_stats_update_ = 0;
  uint32_t last_settings_update_ = 0;
  uint32_t last_system_settings_update_ = 0;
  uint32_t last_grid_protection_update_ = 0;
  uint32_t last_extended_settings_update_ = 0;
  uint32_t last_california_settings_update_ = 0;
  uint32_t last_battery_modules_update_ = 0;
  uint32_t last_device_info_update_ = 0;
  bool device_info_initialized_ = false;
  
  // Current update state
  enum class UpdatePhase {
    IDLE,
    LIVE_DATA,
    STATISTICS,
    SETTINGS,
    SYSTEM_SETTINGS,
    GRID_PROTECTION,
    EXTENDED_SETTINGS,
    CALIFORNIA_SETTINGS,
    BATTERY_MODULES,
    DEVICE_INFO
  };
  
  UpdatePhase current_phase_ = UpdatePhase::IDLE;
  size_t current_range_index_ = 0;
  size_t current_battery_module_range_ = 0;
  
  // Register ranges from registers.h
  // Live data ranges (1s interval)
  static const RegisterRange LIVE_RANGES[];
  static constexpr size_t LIVE_RANGES_COUNT = 12;
  
  // Statistics ranges (5s interval)
  static const RegisterRange STATS_RANGES[];
  static constexpr size_t STATS_RANGES_COUNT = 4;
  
  // Settings ranges (60s interval)
  static const RegisterRange SETTINGS_RANGES[];
  static constexpr size_t SETTINGS_RANGES_COUNT = 12;
  
  // System Settings ranges (60-97) - 2 minutes interval
  static const RegisterRange SETTINGS_SYSTEM_RANGES[];
  static constexpr size_t SETTINGS_SYSTEM_RANGES_COUNT = 4;
  
  // Grid Protection Settings ranges (185-200) - 2 minutes interval
  static const RegisterRange SETTINGS_GRID_PROTECTION_RANGES[];
  static constexpr size_t SETTINGS_GRID_PROTECTION_RANGES_COUNT = 2;
  
  // Extended Settings ranges (231-339) - 2 minutes interval
  static const RegisterRange SETTINGS_EXTENDED_RANGES[];
  static constexpr size_t SETTINGS_EXTENDED_RANGES_COUNT = 6;
  
  // California Compliance Settings ranges (340-499) - 5 minutes interval
  static const RegisterRange SETTINGS_CALIFORNIA_RANGES[];
  static constexpr size_t SETTINGS_CALIFORNIA_RANGES_COUNT = 6;
  
  // Battery Module ranges (684-809) - 5 seconds interval
  static const RegisterRange BATTERY_MODULE_RANGES[];
  static constexpr size_t BATTERY_MODULE_RANGES_COUNT = 9;
  
  // Device info ranges (read once at startup, then rarely)
  static const RegisterRange DEVICE_INFO_RANGES[];
  static constexpr size_t DEVICE_INFO_RANGES_COUNT = 5;
  
  // Platform lists
  std::vector<DeyeSensor*> sensors_;
  std::vector<DeyeBinarySensor*> binary_sensors_;
  std::vector<DeyeTextSensor*> text_sensors_;
  std::vector<DeyeSwitch*> switches_;
  std::vector<DeyeNumber*> numbers_;
  std::vector<DeyeSelect*> selects_;
  std::vector<DeyeDateTime*> datetimes_;
  std::vector<DeyeTime*> times_;
};

}  // namespace deye_inverter
}  // namespace esphome
