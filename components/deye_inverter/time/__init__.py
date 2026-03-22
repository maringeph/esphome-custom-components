"""Deye Inverter time platform for ESPHome.

This module provides a time entity for synchronizing ESPHome time
to the Deye inverter's system time (registers 62-64).

The time is only written to the inverter when:
1. The local time has been set (e.g., DST change) - always syncs
2. The time difference is greater than max_time_diff (if > 0)

Setting max_time_diff: 0s disables auto-sync, only syncs on time change/DST.

Register format (6 bytes across 3 registers):
- Register 62: Year (byte 1), Month (byte 2)
- Register 63: Day (byte 3), Hour (byte 4)
- Register 64: Minute (byte 5), Second (byte 6)

Format: YY, MM, DD, HH, mm, ss
Base year: 2000 (YY=24 means 2024)

Actions:
  - deye_inverter.write_time: Manually trigger time sync
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import time
from esphome.const import CONF_ID

# Import from parent component
from .. import (
    CONF_DEYE_INVERTER_ID,
    DeyeInverter,
    deye_inverter_ns,
)

# Declare DeyeTime class
DeyeTime = deye_inverter_ns.class_("DeyeTime", time.RealTimeClock, cg.Component)

# =============================================================================
# CONF CONSTANTS
# =============================================================================
CONF_MAX_TIME_DIFF = "max_time_diff"

# =============================================================================
# PLATFORM SCHEMA
# =============================================================================
PLATFORM_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_MAX_TIME_DIFF, default="10s"): cv.positive_time_period_seconds,
    }
)


# =============================================================================
# CODE GENERATION
# =============================================================================
async def to_code(config):
    """Generate code for Deye Inverter time synchronization."""
    var = await time.new_time(config)
    await cg.register_component(var, config)

    # Get the DeyeInverter parent
    parent = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])
    cg.add(var.set_parent(parent))

    # Set max diff parameter
    cg.add(var.set_max_time_diff(config[CONF_MAX_TIME_DIFF]))

    return var
