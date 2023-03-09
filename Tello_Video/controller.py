import tello
import PIDController

class Controller:
    def __init__(self):
        print("init controller")
        self.drone = tello.Tello('', 8889)
        self.error = 0
        self.target_pose = [0, 0, 0]
        self.current_pose = [0, 0, 0]
        self.pose_error = [0, 0, 0]
        self.frame = None

        self.xpid = PIDController.PIDController(8, 0.02, 10, 75, 75, 100, 100)
        self.ypid = PIDController.PIDController(4, 2.35, 8, 75, 75, 100, 100)
        self.zpid = PIDController.PIDController(8, 0.02, 10, 75, 75, 100, 100)

    def send_command(self, cmd):
        if cmd.contains("takeoff") or cmd.contains("land"):
            self.drone.send_command(cmd)
        else:
            self.target_pose = cmd.split(' ')
            self.xpid.set_point(self.target_pose[0])
            self.ypid.set_point(self.target_pose[1])
            self.zpid.set_point(self.target_pose[2])

    def update(self):

        self.pose_error = [self.target_pose[0] - self.current_pose[0], self.target_pose[1] - self.current_pose[1], self.target_pose[2] - self.current_pose[2]]
        self.error = sum(self.pose_error) / len(self.pose_error)

        self.frame = self.drone.read()
        if self.frame is None or self.frame.size == 0:
            return
        else:
            self.current_pose = self.process_frame()
            correction = self.calculate_correction(self.current_pose[0], self.current_pose[1], self.current_pose[2])
            self.drone.send_command('go {} {} {} 10'.format(self.target_pose[0] + correction[0], self.target_pose[1] + correction[1], self.target_pose[2] + correction[2]))

    def process_frame(self):
        return [0, 0, 0]

    def calculate_correction(self, cur_x, cur_y, cur_z):
        return self.xpid.get_correction(cur_x), self.ypid.get_correction(cur_y), self.zpid.get_correction(cur_z)
