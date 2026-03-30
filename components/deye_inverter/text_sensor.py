import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID

# Import only the parent class reference from __init__.py
from . import CONF_DEYE_INVERTER_ID, CONF_DEVICE_ID, DeyeInverter

# Namespace für DeyeTextSensor
DeyeTextSensor = cg.esphome_ns.namespace("deye_inverter").class_(
    "DeyeTextSensor", text_sensor.TextSensor, cg.Component
)

# =============================================================================
# LOCAL CONF CONSTANTS for Text Sensors
# =============================================================================
CONF_DEVICE_TYPE = "device_type"
CONF_RUNNING_STATUS = "running_status"
CONF_SERIAL_NUMBER = "serial_number"
CONF_FIRMWARE_VERSION = "firmware_version"
CONF_HARDWARE_VERSION = "hardware_version"
CONF_INVERTER_MODEL = "inverter_model"
CONF_COMMUNICATION_PROTOCOL = "communication_protocol"

# =============================================================================
# LOCAL SCHEMA DEFINITIONS
# =============================================================================

TEXT_ENTITY_SCHEMA = text_sensor.text_sensor_schema(DeyeTextSensor)

# =============================================================================
# PLATFORM SCHEMA
# =============================================================================

CONFIG_SCHEMA = cv.Schema(
    {
        cv.Required(CONF_DEYE_INVERTER_ID): cv.use_id(DeyeInverter),
        cv.Optional(CONF_DEVICE_ID): cv.string,
        # Device Type (Register 0)
        cv.Optional(CONF_DEVICE_TYPE): text_sensor.text_sensor_schema(
            DeyeTextSensor,
            icon="mdi:server",
        ),
        # Communication Protocol Version (Register 2)
        cv.Optional(CONF_COMMUNICATION_PROTOCOL): text_sensor.text_sensor_schema(
            DeyeTextSensor,
            icon="mdi:protocol",
        ),
        # Running Status (Register 500)
        cv.Optional(CONF_RUNNING_STATUS): text_sensor.text_sensor_schema(
            DeyeTextSensor,
            icon="mdi:state-machine",
        ),
        # Serial Number (Registers 3-14)
        cv.Optional(CONF_SERIAL_NUMBER): text_sensor.text_sensor_schema(
            DeyeTextSensor,
            icon="mdi:barcode",
        ),
        # Firmware Version (Register 18 - Comm Board Firmware Version)
        cv.Optional(CONF_FIRMWARE_VERSION): text_sensor.text_sensor_schema(
            DeyeTextSensor,
            icon="mdi:update",
        ),
        # Hardware Version (Register 15 - Control Board Firmware Version)
        cv.Optional(CONF_HARDWARE_VERSION): text_sensor.text_sensor_schema(
            DeyeTextSensor,
            icon="mdi:cog",
        ),
        # Inverter Model (Register 15 - Control Board Firmware Version)
        cv.Optional(CONF_INVERTER_MODEL): text_sensor.text_sensor_schema(
            DeyeTextSensor,
            icon="mdi:inverter",
        ),
    }
)


# =============================================================================
# HELPER FUNCTIONS FOR to_code
# =============================================================================


async def register_text_sensor(
    config,
    key,
    parent,
    address,
    is_status=False,
    is_device_type=False,
    is_serial_number=False,
    is_firmware_version=False,
    is_hardware_version=False,
    register_count=1,
    device_obj=None,
):
    """Register a single text sensor with the parent component."""
    if key not in config:
        return

    conf = config[key]
    # Create DeyeTextSensor instead of base text sensor
    sens = cg.new_Pvariable(conf[CONF_ID])
    await text_sensor.register_text_sensor(sens, conf)
    cg.add(sens.set_parent(parent))
    cg.add(sens.set_address(address))
    cg.add(sens.set_is_status(is_status))
    cg.add(sens.set_is_device_type(is_device_type))
    cg.add(sens.set_is_serial_number(is_serial_number))
    cg.add(sens.set_is_firmware_version(is_firmware_version))
    cg.add(sens.set_is_hardware_version(is_hardware_version))
    cg.add(sens.set_register_count(register_count))

    # Register with parent's text sensor list
    cg.add(parent.register_text_sensor(sens))

    # Associate with device if provided
    if device_obj is not None:
        cg.add(sens.set_device(device_obj))


# =============================================================================
# CODE GENERATION
# =============================================================================


async def to_code(config):
    var = await cg.get_variable(config[CONF_DEYE_INVERTER_ID])

    # Handle device_id for Home Assistant grouping
    from . import get_or_create_device

    device_id = config.get(CONF_DEVICE_ID)
    device_obj = await get_or_create_device(device_id)

    # Device Type (Register 0)
    if CONF_DEVICE_TYPE in config:
        await register_text_sensor(
            config,
            CONF_DEVICE_TYPE,
            var,
            cg.RawExpression("esphome::deye_inverter::REG_DEVICE_TYPE"),
            is_status=False,
            is_device_type=True,
            device_obj=device_obj,
        )

    # Communication Protocol Version (Register 2)
    if CONF_COMMUNICATION_PROTOCOL in config:
        await register_text_sensor(
            config,
            CONF_COMMUNICATION_PROTOCOL,
            var,
            cg.RawExpression("esphome::deye_inverter::REG_COMM_PROTOCOL_VERSION"),
            is_status=False,
            is_device_type=False,
            device_obj=device_obj,
        )

    # Running Status (Register 500)
    if CONF_RUNNING_STATUS in config:
        await register_text_sensor(
            config,
            CONF_RUNNING_STATUS,
            var,
            cg.RawExpression("esphome::deye_inverter::REG_RUNNING_STATUS"),
            is_status=True,
            is_device_type=False,
            device_obj=device_obj,
        )

    # Serial Number (Register 3 - start of 12 registers for ASCII serial)
    if CONF_SERIAL_NUMBER in config:
        await register_text_sensor(
            config,
            CONF_SERIAL_NUMBER,
            var,
            cg.RawExpression("esphome::deye_inverter::REG_SERIAL_NUMBER_01"),
            is_status=False,
            is_device_type=False,
            is_serial_number=True,
            register_count=12,  # 12 registers for full serial number
            device_obj=device_obj,
        )

    # Firmware Version (Register 18 - Comm Board Firmware Version)
    if CONF_FIRMWARE_VERSION in config:
        await register_text_sensor(
            config,
            CONF_FIRMWARE_VERSION,
            var,
            cg.RawExpression("esphome::deye_inverter::REG_COMM_BOARD_FIRMWARE_VERSION"),
            is_status=False,
            is_device_type=False,
            is_firmware_version=True,
            device_obj=device_obj,
        )

    # Hardware Version (Register 15 - Control Board Firmware Version)
    if CONF_HARDWARE_VERSION in config:
        await register_text_sensor(
            config,
            CONF_HARDWARE_VERSION,
            var,
            cg.RawExpression(
                "esphome::deye_inverter::REG_CONTROL_BOARD_FIRMWARE_VERSION"
            ),
            is_status=False,
            is_device_type=False,
            is_hardware_version=True,
            device_obj=device_obj,
        )

    # Inverter Model (Register 15)
    if CONF_INVERTER_MODEL in config:
        await register_text_sensor(
            config,
            CONF_INVERTER_MODEL,
            var,
            cg.RawExpression(
                "esphome::deye_inverter::REG_CONTROL_BOARD_FIRMWARE_VERSION"
            ),
            is_status=False,
            is_device_type=False,
            device_obj=device_obj,
        )
