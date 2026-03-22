"""Binary Sensor platform for Deye Inverter component."""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_CONNECTIVITY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_PROBLEM,
)

from . import (
    CONF_DEYE_INVERTER_ID,
    CONF_STATUS,
    CONF_WARNINGS,
    CONF_RELAY_INVERTER,
    CONF_RELAY_LOAD,
    CONF_RELAY_GRID,
    CONF_RELAY_GENERATOR,
    DeyeInverter,
)

AUTO_LOAD = ["modbus_controller"]

# Namespace for DeyeBinarySensor
DeyeBinarySensor = cg.esphome_ns.namespace("deye_inverter").class_(
    "DeyeBinarySensor", binary_sensor.BinarySensor, cg.Component
)

CODEOWNERS = ["@maringeph"]

# =============================================================================
# CONF CONSTANTS FOR BINARY SENSORS - Status Group
# =============================================================================

# Status Bits (Register 551)
CONF_GRID_CONNECTED = "grid_connected"
CONF_GENERATOR_CONNECTED = "generator_connected"
CONF_SOLAR_SELL_STATUS = "solar_sell_status"
CONF_TIME_OF_USE_STATUS = "time_of_use_status"
CONF_BATTERY_CHARGING = "battery_charging"
CONF_BATTERY_DISCHARGING = "battery_discharging"

# Relay Status Bits (Register 552)
CONF_RELAY_INVERTER_RUN = "relay_inverter_run"
CONF_RELAY_STATUS = "relay_status"
CONF_RELAY_GRID_RELAY = "relay_grid_relay"
CONF_RELAY_GEN_RELAY = "relay_gen_relay"
CONF_RELAY_GRID_RUN = "relay_grid_run"
CONF_RELAY_GEN_RUN = "relay_gen_run"
CONF_RELAY_AC_RELAY = "relay_ac_relay"

# Warning Bits (Register 553 - Warning 1)
CONF_WARNING_BATTERY_LOW = "warning_battery_low"
CONF_WARNING_BATTERY_SHUTDOWN = "warning_battery_shutdown"
CONF_WARNING_BATTERY_OVER_VOLTAGE = "warning_battery_over_voltage"
CONF_WARNING_BATTERY_SOC_LOW = "warning_battery_soc_low"
CONF_WARNING_PV_OVER_VOLTAGE = "warning_pv_over_voltage"
CONF_WARNING_GRID_VOLTAGE_HIGH = "warning_grid_voltage_high"
CONF_WARNING_GRID_VOLTAGE_LOW = "warning_grid_voltage_low"
CONF_WARNING_GRID_FREQ_HIGH = "warning_grid_freq_high"
CONF_WARNING_GRID_FREQ_LOW = "warning_grid_freq_low"

# Warning Bits (Register 554 - Warning 2)
CONF_WARNING_TEMP_HIGH = "warning_temp_high"
CONF_WARNING_OVERLOAD = "warning_overload"


# =============================================================================
# CONFIGURATION SCHEMA
# =============================================================================

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(cg.EntityBase),
        cv.GenerateID(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        # Status Group - all relay/power status sensors
        cv.Optional(CONF_STATUS): cv.Schema(
            {
                cv.Optional(CONF_GRID_CONNECTED): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_CONNECTIVITY,
                ),
                cv.Optional(
                    CONF_GENERATOR_CONNECTED
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_CONNECTIVITY,
                ),
                cv.Optional(CONF_SOLAR_SELL_STATUS): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
                cv.Optional(
                    CONF_TIME_OF_USE_STATUS
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
                cv.Optional(CONF_BATTERY_CHARGING): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
                cv.Optional(
                    CONF_BATTERY_DISCHARGING
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
            }
        ),
        # Relay Status Group - all relay status sensors
        cv.Optional(CONF_RELAY_GRID): cv.Schema(
            {
                cv.Optional(CONF_RELAY_GRID_RELAY): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
                cv.Optional(CONF_RELAY_GRID_RUN): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
            }
        ),
        cv.Optional(CONF_RELAY_GENERATOR): cv.Schema(
            {
                cv.Optional(CONF_RELAY_GEN_RELAY): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
                cv.Optional(CONF_RELAY_GEN_RUN): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
            }
        ),
        cv.Optional(CONF_RELAY_LOAD): cv.Schema(
            {
                cv.Optional(
                    CONF_RELAY_INVERTER_RUN
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
                cv.Optional(CONF_RELAY_STATUS): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
                cv.Optional(CONF_RELAY_AC_RELAY): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_POWER,
                ),
            }
        ),
        # Warnings Group - all warning sensors
        cv.Optional(CONF_WARNINGS): cv.Schema(
            {
                cv.Optional(
                    CONF_WARNING_BATTERY_LOW
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(
                    CONF_WARNING_BATTERY_SHUTDOWN
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(
                    CONF_WARNING_BATTERY_OVER_VOLTAGE
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(
                    CONF_WARNING_BATTERY_SOC_LOW
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(
                    CONF_WARNING_PV_OVER_VOLTAGE
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(
                    CONF_WARNING_GRID_VOLTAGE_HIGH
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(
                    CONF_WARNING_GRID_VOLTAGE_LOW
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(
                    CONF_WARNING_GRID_FREQ_HIGH
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(
                    CONF_WARNING_GRID_FREQ_LOW
                ): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(CONF_WARNING_TEMP_HIGH): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
                cv.Optional(CONF_WARNING_OVERLOAD): binary_sensor.binary_sensor_schema(
                    device_class=DEVICE_CLASS_PROBLEM,
                ),
            }
        ),
    }
)


# =============================================================================
# HELPER FUNCTIONS FOR to_code
# =============================================================================


async def register_binary_sensor(config, key, parent, address, bitmask):
    """Register a single binary sensor with the parent component."""
    if key not in config:
        return

    conf = config[key]
    sens = await binary_sensor.new_binary_sensor(conf)
    cg.add(sens.set_parent(parent))
    cg.add(sens.set_address(address))
    cg.add(sens.set_bitmask(bitmask))

    # Register with parent's binary sensor list
    cg.add(parent.register_binary_sensor(sens))


# =============================================================================
# CODE GENERATION
# =============================================================================


async def to_code(config):
    parent = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Status Sensors (Register 551 - Power Status)
    if CONF_STATUS in config:
        status_conf = config[CONF_STATUS]
        # Bit 0: Grid connected
        await register_binary_sensor(
            status_conf, CONF_GRID_CONNECTED, parent, 551, 0x0001
        )
        # Bit 1: Generator connected
        await register_binary_sensor(
            status_conf, CONF_GENERATOR_CONNECTED, parent, 551, 0x0002
        )
        # Bit 4: Solar sell
        await register_binary_sensor(
            status_conf, CONF_SOLAR_SELL_STATUS, parent, 551, 0x0010
        )
        # Bit 5: Time of use
        await register_binary_sensor(
            status_conf, CONF_TIME_OF_USE_STATUS, parent, 551, 0x0020
        )
        # Bit 8: Battery charging
        await register_binary_sensor(
            status_conf, CONF_BATTERY_CHARGING, parent, 551, 0x0100
        )
        # Bit 9: Battery discharging
        await register_binary_sensor(
            status_conf, CONF_BATTERY_DISCHARGING, parent, 551, 0x0200
        )

    # Relay Status Sensors (Register 552 - Relay Status)
    if CONF_RELAY_GRID in config:
        relay_grid_conf = config[CONF_RELAY_GRID]
        # Bit 2: Grid relay
        await register_binary_sensor(
            relay_grid_conf, CONF_RELAY_GRID_RELAY, parent, 552, 0x0004
        )
        # Bit 4: Grid run
        await register_binary_sensor(
            relay_grid_conf, CONF_RELAY_GRID_RUN, parent, 552, 0x0010
        )

    if CONF_RELAY_GENERATOR in config:
        relay_gen_conf = config[CONF_RELAY_GENERATOR]
        # Bit 3: Gen relay
        await register_binary_sensor(
            relay_gen_conf, CONF_RELAY_GEN_RELAY, parent, 552, 0x0008
        )
        # Bit 5: Gen run
        await register_binary_sensor(
            relay_gen_conf, CONF_RELAY_GEN_RUN, parent, 552, 0x0020
        )

    if CONF_RELAY_LOAD in config:
        relay_load_conf = config[CONF_RELAY_LOAD]
        # Bit 0: Inverter run
        await register_binary_sensor(
            relay_load_conf, CONF_RELAY_INVERTER_RUN, parent, 552, 0x0001
        )
        # Bit 1: Relay
        await register_binary_sensor(
            relay_load_conf, CONF_RELAY_STATUS, parent, 552, 0x0002
        )
        # Bit 7: AC relay
        await register_binary_sensor(
            relay_load_conf, CONF_RELAY_AC_RELAY, parent, 552, 0x0080
        )

    # Warning Sensors (Register 553 - Warning 1)
    if CONF_WARNINGS in config:
        warnings_conf = config[CONF_WARNINGS]
        # Warning 1 bits
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_BATTERY_LOW, parent, 553, 0x0001
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_BATTERY_SHUTDOWN, parent, 553, 0x0002
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_BATTERY_OVER_VOLTAGE, parent, 553, 0x0004
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_BATTERY_SOC_LOW, parent, 553, 0x0008
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_PV_OVER_VOLTAGE, parent, 553, 0x0010
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_GRID_VOLTAGE_HIGH, parent, 553, 0x0020
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_GRID_VOLTAGE_LOW, parent, 553, 0x0040
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_GRID_FREQ_HIGH, parent, 553, 0x0080
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_GRID_FREQ_LOW, parent, 553, 0x0100
        )

        # Warning 2 bits (Register 554)
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_TEMP_HIGH, parent, 554, 0x0001
        )
        await register_binary_sensor(
            warnings_conf, CONF_WARNING_OVERLOAD, parent, 554, 0x0002
        )
