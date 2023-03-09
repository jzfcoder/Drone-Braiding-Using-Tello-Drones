
class PIDController:
    def __init__(self, P, I, D, minOut, maxOut, minIn, maxIn):
        self.P = P
        self.I = I
        self.D = D

        self.minOut = minOut
        self.maxOut = maxOut

        self.minIn = minIn
        self.maxIn = maxIn
        self.point = 0
        self.setPoint(0)
        self.prev_err = 0
        self.total_err = 0

    def set_point(self, new_point):
        self.point = new_point

    def get_correction(self, cur):
        err = self.point - cur
        correction = 0

        kp_correction = err * self.P
        kd_correction = (err - self.prev_err) * self.D

        ki_correction = (self.total_err + err) * self.I

        if kp_correction <= self.minOut or kp_correction >= self.maxOut:
            ki_correction = 0

        if self.minOut < ki_correction < self.maxOut:
            self.total_err += err

        correction = kp_correction + ki_correction + kd_correction

        if correction < self.minOut:
            correction = self.minOut
        elif correction > self.maxOut:
            correction = self.maxOut

        self.prev_err = err

        return correction
