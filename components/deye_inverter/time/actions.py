import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import automation
from esphome.const import CONF_ID
from esphome.cpp_types import Action

from .. import deye_inverter_ns

# Get DeyeTime class
DeyeTime = deye_inverter_ns.class_("DeyeTime")

# =============================================================================
# ACTION: Write Time to Inverter
# =============================================================================
DeyeTimeWriteAction = deye_inverter_ns.class_(
    "DeyeTimeWriteAction",
    Action,
    cg.Parented.template(DeyeTime),
)

DEYE_TIME_WRITE_ACTION_SCHEMA = cv.maybe_simple_value(
    {
        cv.GenerateID(): cv.use_id(DeyeTime),
    },
    key=CONF_ID,
)


@automation.register_action(
    "deye_inverter.write_time",
    DeyeTimeWriteAction,
    DEYE_TIME_WRITE_ACTION_SCHEMA,
)
async def deye_time_write_action_to_code(config, action_id, template_arg, args):
    """Generate code for write_time action."""
    paren = await cg.get_variable(config[CONF_ID])
    return cg.new_Pvariable(action_id, template_arg, paren)
