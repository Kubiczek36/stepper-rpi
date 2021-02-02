from time import sleep
import RPi.GPIO as GPIO

class stepper:
  """
  Třída pro obládání krokových motorů 28BYJ-48. Zbastleno podle [tohoto návodu]
  (https://navody.dratek.cz/navody-k-produktum/krokovy-motor-a-driver.html).
  """
  def __init__(self, in1, in2, in3, in4):
      """
      `in1` - zapojení pinu do příslušné GPIO. [Návod zde](https://www.raspberr
      ypi.org/documentation/usage/gpio/). 
    
      `in2, in3, in4` odbodně.
      """
      if GPIO.getmode() != 11:
          GPIO.setmode(GPIO.BCM) 
#      self.in1 = LED(in1)
#      self.in2 = LED(in2)
#      self.in3 = LED(in3)
#      self.in4 = LED(in4)
#      self.outputArray = [self.in1, self.in2, self.in3, self.in4]
      self.control_pins = [[in1, in2, in3, in4]]
      for pin in range(4):
          print(self.control_pins[0][pin])
      for pin in self.control_pins[0]:
          GPIO.setup(pin, GPIO.OUT)
          GPIO.output(pin, 0)
      self.halfstep_seq = [
          [1,0,0,0],
          [1,1,0,0],
          [0,1,0,0],
          [0,1,1,0],
          [0,0,1,0],
          [0,0,1,1],
          [0,0,0,1],
          [1,0,0,1]
        ]
      self.back_halfstep_seq = [
          [0,0,0,1],
          [0,0,1,1],
          [0,0,1,0],
          [0,1,1,0],
          [0,1,0,0],
          [1,1,0,0],
          [1,0,0,0],
          [1,0,0,1]
        ]
      print("Initiation succesful!")
  def addMotor(self, in1, in2, in3, in4):
      self.control_pins.append([in1, in2, in3, in4])
      for pin in self.control_pins[-1]:
          GPIO.setup(pin, GPIO.OUT)
          GPIO.output(pin, 0)
      print("Motor (axis) no.", len(self.control_pins), "connected!")
  def halfstep(self, axis = 0):
          for halfstep in range(8):
            for pin in range(4):
                GPIO.output(self.control_pins[axis][pin], self.halfstep_seq[halfstep][pin])
            sleep(0.001)
  def halfstepAnti(self, axis = 0):
          for halfstep in range(8):
            for pin in range(4):
                GPIO.output(self.control_pins[axis][pin], self.back_halfstep_seq[halfstep][pin])
            sleep(0.0015)
#  def multiHalfstep(self, axis = 0):
#          for halfstep in range(8):
#            for pin in range(4):
#                GPIO.output(self.control_pins[pin][axis], self.halfstep_seq[halfstep][pin])
#            sleep(0.0015)
#  def multiHalfstepAnti(self, axis = 0):
#          for halfstep in range(8):
#            for pin in range(4):
#                GPIO.output(self.control_pins[pin][axis], self.halfstep_seq[halfstep][pin])
#            sleep(0.0015)
  
  def turnDeg(self, n):
      steps = int((64*abs(n))//45)
      deg = 45*steps//64
      clockwise = (n<0)
      if clockwise:
          for i in range(steps):
              self.halfstep()
      else:
          for i in range(steps):
              self.halfstepAnti()
      return deg
  def turnDegs(self, axes, degs):
      """
      axes - array of axes to be moved. i.e [0,1]
      
      degs - degrees axes should be moved i.e [10, 100]
      """
      l = len(axes)
      steps = []
      clockwise = []
      for i in range(l):
          steps.append(int((64*abs(degs[i]))//45))
          clockwise.append( (degs[i]<0))
      m = max(steps)
      print("Steps:", steps, "m =", m)
      for i in range(m):
          for halfstep in range(8):
              for axis in range(len(axes)):
                  if steps[axis] >= i:
                      if clockwise[axis]:
                          for pin in range(4):
                              GPIO.output(self.control_pins[axis][pin], self.halfstep_seq[halfstep][pin])
                      else:
                          for pin in range(4):
                              GPIO.output(self.control_pins[axis][pin], self.back_halfstep_seq[halfstep][pin])
              sleep(0.0008)
#      if clockwise:
#          for i in range(steps):
#              self.halfstep()
#      else:
#          for i in range(steps):
#              self.halfstepAnti()
#      sleep(0.01)
#      return degs

  def step(self, clockwise = True):
      from time import sleep
      sleep(0.002)
      for i in range(4):
          self.outputArray[i].on()
          sleep(0.002)
          self.outputArray[i].on()
          if i == 3:
              self.outputArray[0].on()
          else:
              self.outputArray[i+1].on()
          sleep(0.002)
  def end(self):
      GPIO.cleanup()

if __name__ == "__main__":
    stp = stepper
    motor = stp(2,3,4,17)
    motor.addMotor(14,15,18,23)
    for i in range(2):
        for j in range(0):
            motor.halfstep(i)
    motor.turnDegs([0, 1], [360,180])
    sleep(2)
    motor.turnDegs([1, 0], [360,-180])

#          
#if __name__ == "__main__":
#    motor = stepper(2, 3, 4, 17)
#    print(motor.outputArray)
#    for i in range(100):
#        motor.step()
#        
#    
#    import RPi.GPIO as GPIO
#    import time
#    
#    #GPIO.setmode(GPIO.BOARD)
#    GPIO.setmode(GPIO.BCM) 
#    
#    control_pins = [2,3,4,17]
#    
#    for pin in control_pins:
#      GPIO.setup(pin, GPIO.OUT)
#      GPIO.output(pin, 0)
#      
#    halfstep_seq = [
#      [1,0,0,0],
#      [1,1,0,0],
#      [0,1,0,0],
#      [0,1,1,0],
#      [0,0,1,0],
#      [0,0,1,1],
#      [0,0,0,1],
#      [1,0,0,1]
#    ]
#    
#    def halfstep():
#      for halfstep in range(8):
#        for pin in range(4):
#          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
#        time.sleep(0.001)
#    
#    for i in range(5*512//360):
#        halfstep()
#        time.sleep(1)
#        
#    GPIO.cleanup()