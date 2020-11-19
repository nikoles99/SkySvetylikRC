from utils.config_utils import ConfigUtils

GAS_MIN = ConfigUtils.read_value('calibration.leftVertical.min')
GAS_MAX = ConfigUtils.read_value('calibration.leftVertical.max')
YAW_MIN = ConfigUtils.read_value('calibration.leftHorizontal.min')
YAW_MAX = ConfigUtils.read_value('calibration.leftHorizontal.max')
PITCH_MIN = ConfigUtils.read_value('calibration.rightVertical.min')
PITCH_MAX = ConfigUtils.read_value('calibration.rightVertical.max')
ROLL_MIN = ConfigUtils.read_value('calibration.rightHorizontal.min')
ROLL_MAX = ConfigUtils.read_value('calibration.rightHorizontal.max')
ERROR_MS = 10
