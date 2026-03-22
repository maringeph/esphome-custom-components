"""Deye Inverter datetime platform for ESPHome.

This module provides datetime entities for Time of Use (ToU) start times.
Register values are stored as HHMM (e.g., 1000 = "10:00") for ToU.
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import datetime
from esphome.const import CONF_ID, CONF_NAME, CONF_DISABLED_BY_DEFAULT

# Import from parent component
from . import (
    CONF_DEYE_INVERTER_ID,
    DeyeInverter,
    deye_inverter_ns,
    # Time Point Start constants
    CONF_TIME_POINT_1_START,
    CONF_TIME_POINT_2_START,
    CONF_TIME_POINT_3_START,
    CONF_TIME_POINT_4_START,
    CONF_TIME_POINT_5_START,
    CONF_TIME_POINT_6_START,
)

# =============================================================================
# DATETIME ENTITY SCHEMA
# =============================================================================
DATETIME_ENTITY_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_NAME): cv.string,
        cv.Required(CONF_ID): cv.declare_id(datetime.DateTime),
        cv.Optional(CONF_DISABLED_BY_DEFAULT, default=False): cv.boolean,
    }
)

# =============================================================================
# TIME OF USE DATETIME SCHEMA
# =============================================================================
CONF_SETTINGS_TIME_OF_USE_DATETIME = "settings_time_of_use_datetime"

SETTINGS_TIME_OF_USE_DATETIME_SCHEMA = cv.Schema(
    {
        # Time Point Start times as datetime entities (addresses 148-153)
        cv.Optional(CONF_TIME_POINT_1_START): DATETIME_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_2_START): DATETIME_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_3_START): DATETIME_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_4_START): DATETIME_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_5_START): DATETIME_ENTITY_SCHEMA,
        cv.Optional(CONF_TIME_POINT_6_START): DATETIME_ENTITY_SCHEMA,
    }
)

# =============================================================================
# CONFIG SCHEMA
# =============================================================================
CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(
            CONF_SETTINGS_TIME_OF_USE_DATETIME
        ): SETTINGS_TIME_OF_USE_DATETIME_SCHEMA,
    }
)


# =============================================================================
# CODE GENERATION
# =============================================================================
async def to_code(config):
    """Generate code for Deye Inverter datetime entities."""
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Process time of use datetime entities
    if CONF_SETTINGS_TIME_OF_USE_DATETIME in config:
        tou_config = config[CONF_SETTINGS_TIME_OF_USE_DATETIME]

        # Time point addresses (registers 148-153)
        time_points = [
            (CONF_TIME_POINT_1_START, "time_point_1_start", 148),
            (CONF_TIME_POINT_2_START, "time_point_2_start", 149),
            (CONF_TIME_POINT_3_START, "time_point_3_start", 150),
            (CONF_TIME_POINT_4_START, "time_point_4_start", 151),
            (CONF_TIME_POINT_5_START, "time_point_5_start", 152),
            (CONF_TIME_POINT_6_START, "time_point_6_start", 153),
        ]

        for conf_key, entity_key, address in time_points:
            if conf_key in tou_config:
                entity_config = tou_config[conf_key]
                entity = cg.new_Pvariable(entity_config[CONF_ID])
                cg.add(entity.set_name(entity_config[CONF_NAME]))
                cg.add(
                    entity.set_disabled_by_default(
                        entity_config[CONF_DISABLED_BY_DEFAULT]
                    )
                )
                cg.add(entity.set_address(address))
                cg.add(getattr(var, f"set_{entity_key}")(entity))
                await datetime.register_datetime(entity, entity_config)
