#!/usr/bin/env python3
from panda import Panda
from openpilot.common.params import Params
from opendbc.car import get_safety_config, structs
from opendbc.car.interfaces import CarInterfaceBase
from opendbc.car.tesla.values import CAR

class CarInterface(CarInterfaceBase):

  @staticmethod
  def _get_params(ret: structs.CarParams, candidate, fingerprint, car_fw, experimental_long, docs) -> structs.CarParams:
    ret.carName = "tesla"

    # Needs safety validation and final testing before pulling out of dashcam
    ret.dashcamOnly = False

    # Not merged yet
    params = Params()
    stock_acc = params.get_bool("StockTaccEnabledToggle")
    ret.safetyConfigs = [get_safety_config(structs.CarParams.SafetyModel.tesla)]
    
    if not stock_acc:
      ret.safetyConfigs[0].safetyParam |= Panda.FLAG_TESLA_LONG_CONTROL
    ret.openpilotLongitudinalControl = not stock_acc

    ret.steerLimitTimer = 1.0
    ret.steerActuatorDelay = 0.25

    ret.steerControlType = structs.CarParams.SteerControlType.angle
    ret.radarUnavailable = True


    return ret
