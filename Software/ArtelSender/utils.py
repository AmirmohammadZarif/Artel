from numpy.lib import utils


class Utils:
    '''
    Colored printing
    '''
    def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
    def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
    def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
    def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
    def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
    def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
    def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
    def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

    '''
    ##################
    Translate function
    ##################
    '''
    def translate(value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

class Log:
    def error(self, msg):
        Utils.prRed("[ERROR] : {}".format(msg))

    def info(self, msg):
        Utils.prLightGray("[INFO] : {}".format(msg))
    
    def warn(self, msg):
        Utils.prYellow("[WARNING] : {}".format(msg))
        
    def verbose(self, msg):
        Utils.prCyan("[VERBOSE] : {}".format(msg))
