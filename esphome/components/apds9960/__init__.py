import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c
from esphome.const import CONF_ID

DEPENDENCIES = ['i2c']
AUTO_LOAD = ['sensor', 'binary_sensor']
MULTI_CONF = True

CONF_APDS9960_ID = 'apds9960_id'
CONF_ATIME = 'als_integration'
CONF_AGAIN = 'als_gain'

apds9960_nds = cg.esphome_ns.namespace('apds9960')
APDS9960 = apds9960_nds.class_('APDS9960', cg.PollingComponent, i2c.I2CDevice)

APDS9960ALSGain = apds9960_nds.enum('APDS9960ALSGain')
AGAIN_OPTIONS = {
    '1x': APDS9960ALSGain.APDS9960_ALS_GAIN_1X,
    '4x': APDS9960ALSGain.APDS9960_ALS_GAIN_4X,
    '16x': APDS9960ALSGain.APDS9960_ALS_GAIN_16X,
    '64x': APDS9960ALSGain.APDS9960_ALS_GAIN_64X,
}

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(APDS9960),
    cv.Optional(CONF_ATIME, default='0xDB'): cv.int_range(min=0, max=255),
    cv.Optional(CONF_AGAIN, default='4x'): cv.enum(AGAIN_OPTIONS),
}).extend(cv.polling_component_schema('60s')).extend(i2c.i2c_device_schema(0x39))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield i2c.register_i2c_device(var, config)
    cg.add(var.set_als_integration(config[CONF_ATIME]))
    cg.add(var.set_als_gain(config[CONF_AGAIN]))
