"""Deye Inverter Sensor Platform - Helper module.

This module provides sensor registration helpers for the Deye Inverter component.
All configuration schemas have been moved to __init__.py.
"""

import esphome.codegen as cg
from esphome.components import sensor
from esphome.const import (
    CONF_ID,
)

# Import all CONF constants from the main component
from . import (
    CONF_BATTERY,
    CONF_BATTERY_VOLTAGE,
    CONF_BATTERY_CURRENT,
    CONF_BATTERY_POWER,
    CONF_BATTERY_SOC,
    CONF_BATTERY_TEMPERATURE,
    CONF_BATTERY_CAPACITY,
    CONF_PV1,
    CONF_PV2,
    CONF_PV3,
    CONF_PV4,
    CONF_PV_VOLTAGE,
    CONF_PV_CURRENT,
    CONF_PV_POWER,
    CONF_GRID,
    CONF_GRID_VOLTAGE_L1,
    CONF_GRID_VOLTAGE_L2,
    CONF_GRID_VOLTAGE_L3,
    CONF_GRID_CURRENT_L1,
    CONF_GRID_CURRENT_L2,
    CONF_GRID_CURRENT_L3,
    CONF_GRID_POWER_L1,
    CONF_GRID_POWER_L2,
    CONF_GRID_POWER_L3,
    CONF_GRID_POWER_TOTAL,
    CONF_GRID_FREQUENCY,
    CONF_GRID_SIDE_A_PHASE_POWER,
    CONF_GRID_SIDE_B_PHASE_POWER,
    CONF_GRID_SIDE_C_PHASE_POWER,
    CONF_GRID_SIDE_TOTAL_POWER,
    CONF_TOTAL_GRID_POWER,
    CONF_LOAD_GRID,
    CONF_LOAD_GRID_VOLTAGE_L1,
    CONF_LOAD_GRID_VOLTAGE_L2,
    CONF_LOAD_GRID_VOLTAGE_L3,
    CONF_LOAD_GRID_POWER_L1,
    CONF_LOAD_GRID_POWER_L2,
    CONF_LOAD_GRID_POWER_L3,
    CONF_LOAD_GRID_POWER_TOTAL,
    CONF_LOAD_GRID_PORT,
    CONF_LOAD_PORT_VOLTAGE_L1,
    CONF_LOAD_PORT_VOLTAGE_L2,
    CONF_LOAD_PORT_VOLTAGE_L3,
    CONF_LOAD_PORT_CURRENT_L1,
    CONF_LOAD_PORT_CURRENT_L2,
    CONF_LOAD_PORT_CURRENT_L3,
    CONF_LOAD_PORT_POWER_L1,
    CONF_LOAD_PORT_POWER_L2,
    CONF_LOAD_PORT_POWER_L3,
    CONF_LOAD_REAL_POWER,
    CONF_LOAD_APPARENT_POWER,
    CONF_LOAD_FREQUENCY,
    CONF_LOAD_UPS,
    CONF_LOAD_UPS_VOLTAGE_L1,
    CONF_LOAD_UPS_VOLTAGE_L2,
    CONF_LOAD_UPS_VOLTAGE_L3,
    CONF_LOAD_UPS_POWER_L1,
    CONF_LOAD_UPS_POWER_L2,
    CONF_LOAD_UPS_POWER_L3,
    CONF_LOAD_UPS_POWER_TOTAL,
    CONF_LOAD_UPS_FREQUENCY,
    CONF_GENERATOR,
    CONF_GENERATOR_VOLTAGE_L1,
    CONF_GENERATOR_VOLTAGE_L2,
    CONF_GENERATOR_VOLTAGE_L3,
    CONF_GENERATOR_CURRENT_L1,
    CONF_GENERATOR_CURRENT_L2,
    CONF_GENERATOR_CURRENT_L3,
    CONF_GENERATOR_POWER_L1,
    CONF_GENERATOR_POWER_L2,
    CONF_GENERATOR_POWER_L3,
    CONF_GENERATOR_POWER_TOTAL,
    CONF_GENERATOR_FREQUENCY,
    CONF_GENERATOR_PORT,
    CONF_GEN_PORT_VOLTAGE_L1,
    CONF_GEN_PORT_VOLTAGE_L2,
    CONF_GEN_PORT_VOLTAGE_L3,
    CONF_GEN_PORT_CURRENT_L1,
    CONF_GEN_PORT_CURRENT_L2,
    CONF_GEN_PORT_CURRENT_L3,
    CONF_GEN_PORT_POWER_L1,
    CONF_GEN_PORT_POWER_L2,
    CONF_GEN_PORT_POWER_L3,
    CONF_GEN_PORT_POWER_TOTAL,
    CONF_GEN_PORT_FREQUENCY,
    CONF_TEMPERATURES,
    CONF_TEMP_HEATSINK,
    CONF_TEMP_DC_TRANSFORMER,
    CONF_INVERTER,
    CONF_INVERTER_VOLTAGE_L1,
    CONF_INVERTER_VOLTAGE_L2,
    CONF_INVERTER_VOLTAGE_L3,
    CONF_INVERTER_REAL_POWER_L1,
    CONF_INVERTER_REAL_POWER_L2,
    CONF_INVERTER_REAL_POWER_L3,
    CONF_INVERTER_REAL_POWER,
    CONF_INVERTER_APPARENT_POWER,
    CONF_INVERTER_FREQUENCY,
    CONF_DC,
    CONF_DC5_CURRENT,
    CONF_DC6_VOLTAGE,
    CONF_DC6_CURRENT,
    CONF_DC7_VOLTAGE,
    CONF_DC7_CURRENT,
    CONF_DC8_VOLTAGE,
    CONF_DC8_CURRENT,
    CONF_BATTERY_MODULE_1,
    CONF_BATTERY_MODULE_2,
    CONF_BATTERY_MODULE_3,
    CONF_BATTERY_MODULE_4,
    CONF_BATTERY_MODULE_5,
    CONF_BATTERY_MODULE_6,
    CONF_BATTERY_MODULE_7,
    CONF_BATTERY_MODULE_8,
    CONF_BATTERY_MODULE_9,
    CONF_BM_VOLTAGE,
    CONF_BM_CURRENT,
    CONF_BM_SOC,
    CONF_BM_TEMPERATURE,
    CONF_BM_STATUS,
    CONF_BM_FAULT_CODE,
    CONF_BM_CYCLE_COUNT,
    CONF_BM_CAPACITY_REMAINING,
    CONF_BM_CAPACITY_TOTAL,
    CONF_BM_POWER,
    CONF_BM_CELL_MAX_VOLTAGE,
    CONF_BM_CELL_MIN_VOLTAGE,
    CONF_BM_CELL_MAX_TEMP,
    CONF_BM_CELL_MIN_TEMP,
    CONF_STATISTICS,
    CONF_DAILY,
    CONF_TOTAL,
    CONF_PRODUCTION,
    CONF_BATTERY_CHARGE,
    CONF_BATTERY_DISCHARGE,
    CONF_GRID_IMPORT,
    CONF_GRID_EXPORT,
    CONF_CONSUMPTION,
    CONF_PV_PRODUCTION,
    CONF_DAILY_PV1_PRODUCTION,
    CONF_DAILY_PV2_PRODUCTION,
    CONF_DAILY_PV3_PRODUCTION,
    CONF_DAILY_PV4_PRODUCTION,
    CONF_DAILY_GENERATOR_ON_TIME,
    CONF_DAILY_ACTIVE_POWER_GENERATION,
    CONF_ACTIVE_POWER_GENERATION_TODAY,
    CONF_DAILY_GRID_CONNECTION_TIME,
    CONF_TOTAL_ACTIVE_POWER_GENERATION,
    CONF_TOTAL_REACTIVE_POWER_GENERATION,
    CONF_TOTAL_BATTERY_CHARGE_32,
    CONF_TOTAL_BATTERY_DISCHARGE_32,
    CONF_TOTAL_GRID_IMPORT_32,
    CONF_TOTAL_GRID_EXPORT_32,
    CONF_TOTAL_CONSUMPTION_32,
    CONF_STATUS,
    CONF_WARNING_1_RAW,
    CONF_WARNING_2_RAW,
    CONF_ERROR_1_RAW,
    CONF_ERROR_2_RAW,
    CONF_ERROR_3_RAW,
    CONF_ERROR_4_RAW,
    CONF_COMMUNICATION_BOARD_FAILURE,
    deye_inverter_ns,
)


# =============================================================================
# HELPER FUNCTION
# =============================================================================
async def register_single_sensor(
    config,
    key,
    parent,
    address,
    scale=1.0,
    offset=0.0,
    signed=False,
    value_type="U_WORD",
):
    """Register a single sensor with the parent component."""
    if key not in config:
        return

    conf = config[key]
    sens = await sensor.new_sensor(conf)
    cg.add(sens.set_parent(parent))
    cg.add(sens.set_address(address))
    cg.add(sens.set_scale(scale))
    cg.add(sens.set_offset(offset))

    # Set bytes based on value type
    if value_type in ["U_DWORD", "U_DWORD_R", "S_DWORD", "S_DWORD_R"]:
        cg.add(sens.set_bytes(4))
        cg.add(sens.set_data_type(getattr(deye_inverter_ns.DataType, value_type)))
    else:
        cg.add(sens.set_bytes(2))
        if signed:
            cg.add(sens.set_data_type(deye_inverter_ns.DataType.S_WORD))
        else:
            cg.add(sens.set_data_type(deye_inverter_ns.DataType.U_WORD))

    # Register with parent's sensor list
    cg.add(parent.register_sensor(sens))


# =============================================================================
# MAIN SENSOR REGISTRATION FUNCTION
# =============================================================================
async def register_sensors(parent, config):
    """Register all sensors with the parent component."""

    # =============================================================================
    # PROCESS BATTERY SENSORS
    # =============================================================================
    if CONF_BATTERY in config:
        battery_conf = config[CONF_BATTERY]
        await register_single_sensor(
            battery_conf, CONF_BATTERY_VOLTAGE, parent, 587, scale=0.1
        )
        await register_single_sensor(
            battery_conf, CONF_BATTERY_CURRENT, parent, 591, scale=0.01, signed=True
        )
        await register_single_sensor(
            battery_conf, CONF_BATTERY_POWER, parent, 590, scale=1.0, signed=True
        )
        await register_single_sensor(
            battery_conf, CONF_BATTERY_SOC, parent, 588, scale=1.0
        )
        await register_single_sensor(
            battery_conf,
            CONF_BATTERY_TEMPERATURE,
            parent,
            586,
            scale=0.1,
            offset=-100.0,
        )
        await register_single_sensor(
            battery_conf, CONF_BATTERY_CAPACITY, parent, 592, scale=1.0
        )

    # =============================================================================
    # PROCESS PV STRING SENSORS
    # =============================================================================
    for pv_group, base_addr in [
        (CONF_PV1, 672),
        (CONF_PV2, 673),
        (CONF_PV3, 674),
        (CONF_PV4, 675),
    ]:
        if pv_group in config:
            pv_conf = config[pv_group]
            voltage_addr = 676 + (base_addr - 672) * 2
            current_addr = 677 + (base_addr - 672) * 2
            await register_single_sensor(
                pv_conf, CONF_PV_VOLTAGE, parent, voltage_addr, scale=0.1
            )
            await register_single_sensor(
                pv_conf, CONF_PV_CURRENT, parent, current_addr, scale=0.1
            )
            await register_single_sensor(
                pv_conf, CONF_PV_POWER, parent, base_addr, scale=1.0
            )

    # =============================================================================
    # PROCESS GRID SENSORS
    # =============================================================================
    if CONF_GRID in config:
        grid_conf = config[CONF_GRID]
        await register_single_sensor(
            grid_conf, CONF_GRID_VOLTAGE_L1, parent, 598, scale=0.1
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_VOLTAGE_L2, parent, 599, scale=0.1
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_VOLTAGE_L3, parent, 600, scale=0.1
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_CURRENT_L1, parent, 610, scale=0.01
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_CURRENT_L2, parent, 611, scale=0.01
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_CURRENT_L3, parent, 612, scale=0.01
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_POWER_L1, parent, 604, scale=1.0, signed=True
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_POWER_L2, parent, 605, scale=1.0, signed=True
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_POWER_L3, parent, 606, scale=1.0, signed=True
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_POWER_TOTAL, parent, 607, scale=1.0, signed=True
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_FREQUENCY, parent, 609, scale=0.01
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_SIDE_A_PHASE_POWER, parent, 622, scale=1.0
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_SIDE_B_PHASE_POWER, parent, 623, scale=1.0
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_SIDE_C_PHASE_POWER, parent, 624, scale=1.0
        )
        await register_single_sensor(
            grid_conf, CONF_TOTAL_GRID_POWER, parent, 625, scale=1.0, signed=True
        )
        await register_single_sensor(
            grid_conf, CONF_GRID_SIDE_TOTAL_POWER, parent, 626, scale=1.0
        )

    # =============================================================================
    # PROCESS LOAD GRID SENSORS
    # =============================================================================
    if CONF_LOAD_GRID in config:
        load_grid_conf = config[CONF_LOAD_GRID]
        await register_single_sensor(
            load_grid_conf, CONF_LOAD_GRID_VOLTAGE_L1, parent, 644, scale=0.1
        )
        await register_single_sensor(
            load_grid_conf, CONF_LOAD_GRID_VOLTAGE_L2, parent, 645, scale=0.1
        )
        await register_single_sensor(
            load_grid_conf, CONF_LOAD_GRID_VOLTAGE_L3, parent, 646, scale=0.1
        )
        await register_single_sensor(
            load_grid_conf, CONF_LOAD_GRID_POWER_L1, parent, 650, scale=1.0
        )
        await register_single_sensor(
            load_grid_conf, CONF_LOAD_GRID_POWER_L2, parent, 651, scale=1.0
        )
        await register_single_sensor(
            load_grid_conf, CONF_LOAD_GRID_POWER_L3, parent, 652, scale=1.0
        )
        await register_single_sensor(
            load_grid_conf, CONF_LOAD_GRID_POWER_TOTAL, parent, 653, scale=1.0
        )

    # =============================================================================
    # PROCESS LOAD GRID PORT SENSORS
    # =============================================================================
    if CONF_LOAD_GRID_PORT in config:
        load_port_conf = config[CONF_LOAD_GRID_PORT]
        await register_single_sensor(
            load_port_conf, CONF_LOAD_PORT_VOLTAGE_L1, parent, 644, scale=0.1
        )
        await register_single_sensor(
            load_port_conf, CONF_LOAD_PORT_VOLTAGE_L2, parent, 645, scale=0.1
        )
        await register_single_sensor(
            load_port_conf, CONF_LOAD_PORT_VOLTAGE_L3, parent, 646, scale=0.1
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_CURRENT_L1,
            parent,
            647,
            scale=0.01,
            signed=True,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_CURRENT_L2,
            parent,
            648,
            scale=0.01,
            signed=True,
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_PORT_CURRENT_L3,
            parent,
            649,
            scale=0.01,
            signed=True,
        )
        await register_single_sensor(
            load_port_conf, CONF_LOAD_PORT_POWER_L1, parent, 650, scale=1.0, signed=True
        )
        await register_single_sensor(
            load_port_conf, CONF_LOAD_PORT_POWER_L2, parent, 651, scale=1.0, signed=True
        )
        await register_single_sensor(
            load_port_conf, CONF_LOAD_PORT_POWER_L3, parent, 652, scale=1.0, signed=True
        )
        await register_single_sensor(
            load_port_conf, CONF_LOAD_REAL_POWER, parent, 653, scale=1.0, signed=True
        )
        await register_single_sensor(
            load_port_conf,
            CONF_LOAD_APPARENT_POWER,
            parent,
            654,
            scale=1.0,
            signed=True,
        )
        await register_single_sensor(
            load_port_conf, CONF_LOAD_FREQUENCY, parent, 655, scale=0.01
        )

    # =============================================================================
    # PROCESS LOAD UPS SENSORS
    # =============================================================================
    if CONF_LOAD_UPS in config:
        load_ups_conf = config[CONF_LOAD_UPS]
        await register_single_sensor(
            load_ups_conf, CONF_LOAD_UPS_VOLTAGE_L1, parent, 627, scale=0.1
        )
        await register_single_sensor(
            load_ups_conf, CONF_LOAD_UPS_VOLTAGE_L2, parent, 628, scale=0.1
        )
        await register_single_sensor(
            load_ups_conf, CONF_LOAD_UPS_VOLTAGE_L3, parent, 629, scale=0.1
        )
        await register_single_sensor(
            load_ups_conf, CONF_LOAD_UPS_POWER_L1, parent, 640, scale=1.0
        )
        await register_single_sensor(
            load_ups_conf, CONF_LOAD_UPS_POWER_L2, parent, 641, scale=1.0
        )
        await register_single_sensor(
            load_ups_conf, CONF_LOAD_UPS_POWER_L3, parent, 642, scale=1.0
        )
        await register_single_sensor(
            load_ups_conf, CONF_LOAD_UPS_POWER_TOTAL, parent, 643, scale=1.0
        )
        await register_single_sensor(
            load_ups_conf, CONF_LOAD_UPS_FREQUENCY, parent, 638, scale=0.01
        )

    # =============================================================================
    # PROCESS GENERATOR SENSORS
    # =============================================================================
    if CONF_GENERATOR in config:
        gen_conf = config[CONF_GENERATOR]
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_VOLTAGE_L1, parent, 661, scale=0.1
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_VOLTAGE_L2, parent, 662, scale=0.1
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_VOLTAGE_L3, parent, 663, scale=0.1
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_CURRENT_L1, parent, 668, scale=0.01
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_CURRENT_L2, parent, 669, scale=0.01
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_CURRENT_L3, parent, 670, scale=0.01
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_POWER_L1, parent, 664, scale=1.0
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_POWER_L2, parent, 665, scale=1.0
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_POWER_L3, parent, 666, scale=1.0
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_POWER_TOTAL, parent, 667, scale=1.0
        )
        await register_single_sensor(
            gen_conf, CONF_GENERATOR_FREQUENCY, parent, 671, scale=0.01
        )

    # =============================================================================
    # PROCESS GENERATOR PORT SENSORS
    # =============================================================================
    if CONF_GENERATOR_PORT in config:
        gen_port_conf = config[CONF_GENERATOR_PORT]
        await register_single_sensor(
            gen_port_conf, CONF_GEN_PORT_VOLTAGE_L1, parent, 661, scale=0.1
        )
        await register_single_sensor(
            gen_port_conf, CONF_GEN_PORT_VOLTAGE_L2, parent, 662, scale=0.1
        )
        await register_single_sensor(
            gen_port_conf, CONF_GEN_PORT_VOLTAGE_L3, parent, 663, scale=0.1
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_CURRENT_L1,
            parent,
            668,
            scale=0.01,
            signed=True,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_CURRENT_L2,
            parent,
            669,
            scale=0.01,
            signed=True,
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_CURRENT_L3,
            parent,
            670,
            scale=0.01,
            signed=True,
        )
        await register_single_sensor(
            gen_port_conf, CONF_GEN_PORT_POWER_L1, parent, 664, scale=1.0, signed=True
        )
        await register_single_sensor(
            gen_port_conf, CONF_GEN_PORT_POWER_L2, parent, 665, scale=1.0, signed=True
        )
        await register_single_sensor(
            gen_port_conf, CONF_GEN_PORT_POWER_L3, parent, 666, scale=1.0, signed=True
        )
        await register_single_sensor(
            gen_port_conf,
            CONF_GEN_PORT_POWER_TOTAL,
            parent,
            667,
            scale=1.0,
            signed=True,
        )
        await register_single_sensor(
            gen_port_conf, CONF_GEN_PORT_FREQUENCY, parent, 671, scale=0.01
        )

    # =============================================================================
    # PROCESS INVERTER SENSORS
    # =============================================================================
    if CONF_INVERTER in config:
        inverter_conf = config[CONF_INVERTER]
        await register_single_sensor(
            inverter_conf, CONF_INVERTER_VOLTAGE_L1, parent, 627, scale=0.1
        )
        await register_single_sensor(
            inverter_conf, CONF_INVERTER_VOLTAGE_L2, parent, 628, scale=0.1
        )
        await register_single_sensor(
            inverter_conf, CONF_INVERTER_VOLTAGE_L3, parent, 629, scale=0.1
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_REAL_POWER_L1,
            parent,
            633,
            scale=1.0,
            signed=True,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_REAL_POWER_L2,
            parent,
            634,
            scale=1.0,
            signed=True,
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_REAL_POWER_L3,
            parent,
            635,
            scale=1.0,
            signed=True,
        )
        await register_single_sensor(
            inverter_conf, CONF_INVERTER_REAL_POWER, parent, 636, scale=1.0, signed=True
        )
        await register_single_sensor(
            inverter_conf,
            CONF_INVERTER_APPARENT_POWER,
            parent,
            637,
            scale=1.0,
            signed=True,
        )
        await register_single_sensor(
            inverter_conf, CONF_INVERTER_FREQUENCY, parent, 638, scale=0.01
        )

    # =============================================================================
    # PROCESS DC SENSORS
    # =============================================================================
    if CONF_DC in config:
        dc_conf = config[CONF_DC]
        await register_single_sensor(dc_conf, CONF_DC5_CURRENT, parent, 212, scale=0.1)
        await register_single_sensor(dc_conf, CONF_DC6_VOLTAGE, parent, 213, scale=0.1)
        await register_single_sensor(dc_conf, CONF_DC6_CURRENT, parent, 214, scale=0.1)
        await register_single_sensor(dc_conf, CONF_DC7_VOLTAGE, parent, 215, scale=0.1)
        await register_single_sensor(dc_conf, CONF_DC7_CURRENT, parent, 216, scale=0.1)
        await register_single_sensor(dc_conf, CONF_DC8_VOLTAGE, parent, 217, scale=0.1)
        await register_single_sensor(dc_conf, CONF_DC8_CURRENT, parent, 218, scale=0.1)

    # =============================================================================
    # PROCESS TEMPERATURE SENSORS
    # =============================================================================
    if CONF_TEMPERATURES in config:
        temp_conf = config[CONF_TEMPERATURES]
        await register_single_sensor(
            temp_conf, CONF_TEMP_DC_TRANSFORMER, parent, 540, scale=0.1, offset=-100.0
        )
        await register_single_sensor(
            temp_conf, CONF_TEMP_HEATSINK, parent, 541, scale=0.1, offset=-100.0
        )

    # =============================================================================
    # PROCESS BATTERY MODULE SENSORS
    # =============================================================================
    battery_modules = [
        (CONF_BATTERY_MODULE_1, 350),
        (CONF_BATTERY_MODULE_2, 364),
        (CONF_BATTERY_MODULE_3, 378),
        (CONF_BATTERY_MODULE_4, 392),
        (CONF_BATTERY_MODULE_5, 406),
        (CONF_BATTERY_MODULE_6, 420),
        (CONF_BATTERY_MODULE_7, 434),
        (CONF_BATTERY_MODULE_8, 448),
        (CONF_BATTERY_MODULE_9, 462),
    ]

    for module_conf_name, base_address in battery_modules:
        if module_conf_name in config:
            bm_conf = config[module_conf_name]
            await register_single_sensor(
                bm_conf, CONF_BM_VOLTAGE, parent, base_address, scale=0.01
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CURRENT,
                parent,
                base_address + 1,
                scale=0.01,
                signed=True,
            )
            await register_single_sensor(
                bm_conf, CONF_BM_SOC, parent, base_address + 2, scale=1.0
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_TEMPERATURE,
                parent,
                base_address + 3,
                scale=0.1,
                offset=-100.0,
            )
            await register_single_sensor(
                bm_conf, CONF_BM_STATUS, parent, base_address + 4, scale=1.0
            )
            await register_single_sensor(
                bm_conf, CONF_BM_FAULT_CODE, parent, base_address + 5, scale=1.0
            )
            await register_single_sensor(
                bm_conf, CONF_BM_CYCLE_COUNT, parent, base_address + 6, scale=1.0
            )
            await register_single_sensor(
                bm_conf, CONF_BM_CAPACITY_REMAINING, parent, base_address + 7, scale=0.1
            )
            await register_single_sensor(
                bm_conf, CONF_BM_CAPACITY_TOTAL, parent, base_address + 8, scale=0.1
            )
            await register_single_sensor(
                bm_conf, CONF_BM_POWER, parent, base_address + 9, scale=1.0, signed=True
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CELL_MAX_VOLTAGE,
                parent,
                base_address + 10,
                scale=0.001,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CELL_MIN_VOLTAGE,
                parent,
                base_address + 11,
                scale=0.001,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CELL_MAX_TEMP,
                parent,
                base_address + 12,
                scale=0.1,
                offset=-100.0,
            )
            await register_single_sensor(
                bm_conf,
                CONF_BM_CELL_MIN_TEMP,
                parent,
                base_address + 13,
                scale=0.1,
                offset=-100.0,
            )

    # =============================================================================
    # PROCESS STATISTICS SENSORS
    # =============================================================================
    if CONF_STATISTICS in config:
        stats_conf = config[CONF_STATISTICS]

        if CONF_DAILY in stats_conf:
            daily_conf = stats_conf[CONF_DAILY]
            await register_single_sensor(
                daily_conf, CONF_PRODUCTION, parent, 501, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_BATTERY_CHARGE, parent, 514, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_BATTERY_DISCHARGE, parent, 515, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_GRID_IMPORT, parent, 520, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_GRID_EXPORT, parent, 521, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_CONSUMPTION, parent, 526, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_PV_PRODUCTION, parent, 529, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_DAILY_PV1_PRODUCTION, parent, 530, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_DAILY_PV2_PRODUCTION, parent, 531, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_DAILY_PV3_PRODUCTION, parent, 532, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_DAILY_PV4_PRODUCTION, parent, 533, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_DAILY_GENERATOR_ON_TIME, parent, 539, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_DAILY_ACTIVE_POWER_GENERATION, parent, 501, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_ACTIVE_POWER_GENERATION_TODAY, parent, 502, scale=0.1
            )
            await register_single_sensor(
                daily_conf, CONF_DAILY_GRID_CONNECTION_TIME, parent, 503, scale=1.0
            )

        if CONF_TOTAL in stats_conf:
            total_conf = stats_conf[CONF_TOTAL]
            # 32-bit values
            await register_single_sensor(
                total_conf,
                CONF_PRODUCTION,
                parent,
                504,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_BATTERY_CHARGE,
                parent,
                516,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_BATTERY_DISCHARGE,
                parent,
                518,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_GRID_IMPORT,
                parent,
                522,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_GRID_EXPORT,
                parent,
                524,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_CONSUMPTION,
                parent,
                527,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_PV_PRODUCTION,
                parent,
                534,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_ACTIVE_POWER_GENERATION,
                parent,
                504,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_REACTIVE_POWER_GENERATION,
                parent,
                506,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_BATTERY_CHARGE_32,
                parent,
                516,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_BATTERY_DISCHARGE_32,
                parent,
                518,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_GRID_IMPORT_32,
                parent,
                522,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_GRID_EXPORT_32,
                parent,
                524,
                scale=0.1,
                value_type="U_DWORD_R",
            )
            await register_single_sensor(
                total_conf,
                CONF_TOTAL_CONSUMPTION_32,
                parent,
                527,
                scale=0.1,
                value_type="U_DWORD_R",
            )

    # =============================================================================
    # PROCESS STATUS SENSORS
    # =============================================================================
    if CONF_STATUS in config:
        status_conf = config[CONF_STATUS]
        await register_single_sensor(
            status_conf, CONF_WARNING_1_RAW, parent, 230, scale=1.0
        )
        await register_single_sensor(
            status_conf, CONF_WARNING_2_RAW, parent, 231, scale=1.0
        )
        await register_single_sensor(
            status_conf, CONF_ERROR_1_RAW, parent, 232, scale=1.0
        )
        await register_single_sensor(
            status_conf, CONF_ERROR_2_RAW, parent, 233, scale=1.0
        )
        await register_single_sensor(
            status_conf, CONF_ERROR_3_RAW, parent, 234, scale=1.0
        )
        await register_single_sensor(
            status_conf, CONF_ERROR_4_RAW, parent, 235, scale=1.0
        )
        await register_single_sensor(
            status_conf, CONF_COMMUNICATION_BOARD_FAILURE, parent, 545, scale=1.0
        )
