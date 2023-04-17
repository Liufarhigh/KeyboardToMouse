import keyboard, mouse, time

class keyboardToMouseApp:
    def __init__(self, HOULD_TIME = 2):
        self.run = True
        self.scroll_mode = False
        self.esc = False

        self.mouseX = mouse.get_position()[0]
        self.mouseY = mouse.get_position()[1]
        
        self.mouseSpeedMin = 10
        self.mouseSpeedMax = 50
        self.mouseSpeedStep = 1
        self.mouseSpeed = self.mouseSpeedMin
        self.speedcount = 0
        self.sparse_factor = 3
        self.speedUpStep = self.sparse_factor*2

        self.mouse_left = 'ctrl'
        self.mouse_right = 'e'
        self.mouse_center = 'insert'
        
        self.moving_status = {'left':False, 'right':False, 'up':False, 'down':False}
        self.mouse_right_down = False
        self.mouse_left_down = False
        




        
    
    def main(self):
        self.intro()
        self.lister_move = keyboard.hook(self.filter_move)
        self.lister_control = keyboard.hook(self.filter_control)
        self.lister_key = keyboard.hook(self.filter_key)
        while not self.esc:
            time.sleep(0.1)
            self.moving()

        

        print ('esc key is down exiting')
    
        
    def intro(self):
        print("Mouse Control App")
        print("Simulate mouse press wen key is down")
        # print("Hit 'z' to simulate left mouse press and hold for ", self.HOULD_TIME)
        # print("Hit 'x' to simulate right mouse press and hold for ", self.HOULD_TIME)
        # print("Hit 'c' to simulate center mouse press and hold for ", self.HOULD_TIME)
        # print("Hit 'v' to simulate right mouse click ", self.HOULD_TIME)

    def mouseUp(self, MBUTTON):
        mouse.release(MBUTTON)

    def mouseDown(self, MBUTTON):
        mouse.press(MBUTTON)
    
    def mouseScroll(self, y):
        mouse.wheel(y)

    def mouseMove(self, x, y):
        self.mouseX,self.mouseY = mouse.get_position()
        if self.speedcount == 1 or (self.speedcount%self.sparse_factor==0):
            self.mouseX += x
            self.mouseY += y
            mouse.move(self.mouseX, self.mouseY)
    

    def moving(self):
        self.mouseSpeedUp()
        if self.moving_status['left']:
            self.mouseMove(-self.mouseSpeed, 0)
        if self.moving_status['right']:
            self.mouseMove(self.mouseSpeed, 0)
        if self.moving_status['up']:
            if self.scroll_mode:
                self.mouseScroll(self.mouseSpeed)
            else:
                self.mouseMove(0, -self.mouseSpeed)
        if self.moving_status['down']:
            if self.scroll_mode:
                self.mouseScroll(-self.mouseSpeed)
            else:
                self.mouseMove(0, self.mouseSpeed)

    def stop_moving(self):
        self.mouseSpeedReset()
        self.moving_status = {'left':False, 'right':False, 'up':False, 'down':False}

    def mouseClick(self, MBUTTON):
        mouse.click(MBUTTON)
    
    def mouseSpeedReset(self):
        self.mouseSpeed = self.mouseSpeedMin
        self.speedcount = 0
    
    def mouseSpeedUp(self):
        if self.speedcount <= 2:
            self.mouseSpeed = 1
        else:
            self.mouseSpeed = self.mouseSpeedMin
        self.speedcount += 1
        if self.speedcount > self.sparse_factor*5 and self.speedcount%self.speedUpStep and self.mouseSpeed < self.mouseSpeedMax:
            self.mouseSpeed += self.mouseSpeedStep
            if self.mouseSpeed > self.mouseSpeedMax:
                self.mouseSpeed = self.mouseSpeedMax
        if self.speedcount > self.sparse_factor*15:
            self.mouseSpeed = self.mouseSpeedMax*2

    def filter_control(self,event):
        if event.name == '-' and event.event_type == 'down': 
            if self.run:
                print ('control stop, press alt again to restart')
            else:
                print ('control start, press alt again to stop')
            self.run = not self.run
        if event.name == 'esc':
            self.esc = True 
    def filter_move(self, event):
        if not self.run:
            return
        # time.sleep(0.1)
        # print(event.name, event.event_type)
        if event.name in ['left', 'right', 'up', 'down'] and event.event_type == 'down':
            self.moving_status[event.name] = True
        if event.name in ['left', 'right', 'up', 'down'] and event.event_type == 'up':
            self.moving_status[event.name] = False
            if not any(self.moving_status.values()):
                self.mouseSpeedReset()

    
    def filter_key(self, event):
        if event.name == self.mouse_left and event.event_type == 'down':
            if not self.mouse_left_down:
                self.mouseDown(mouse.LEFT)
            self.mouse_left_down = True
        if event.name == self.mouse_left and event.event_type == 'up':
            self.mouseUp(mouse.LEFT)
            self.mouse_left_down = False
        if event.name == self.mouse_right and event.event_type == 'down':
            if not self.mouse_right_down:
                self.mouseDown(mouse.RIGHT)
            self.mouse_right_down = True
        if event.name == self.mouse_right and event.event_type == 'up':
            self.mouse_right_down = False
            self.mouseUp(mouse.RIGHT)
        if event.name == self.mouse_center and event.event_type == 'down':
            self.scroll_mode = True
            self.stop_moving()
            print('scroll mode on')
        if event.name == self.mouse_center and event.event_type == 'up':
            self.scroll_mode = False
            print('scroll mode off')


if __name__ == "__main__":
    # help(keyboard)
    App = keyboardToMouseApp()
    App.main()
