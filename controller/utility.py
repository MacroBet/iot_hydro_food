

class Utility:

  # temperature or humidity or co2 
#openWindow = shouldOpenWindow(32, 24, 35, 25) or shouldOpenWindow(40, 35, 35, 25)
#temperatureOutside = None
    def shouldOpenWindow(_in, _out, _max, _min):
        # 40, 35, 35, 25 => open
        # 32, 24, 35, 25 => close
        delta_in = abs(_in - _max) + abs(_in - _min)
        # 3 + 7
        delta_out = abs(_out - _max) + abs(_out - _min)
        # 11 + 1
        return delta_in > delta_out


    def shouldCharge(level):
        return level < 20
