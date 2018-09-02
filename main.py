# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import time
import cv2
from functools import partial

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='rgba')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
#Lo que hace el botonciiito
def callback(self, event, param):
        cap = cv2.VideoCapture(0)
        ret,frame = cap.read()
        '''
        while(True):
            cv2.imshow('img1',frame) #display the captured image
            if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
                cv2.imwrite('c1.png',frame)
                cv2.destroyAllWindows()
                break
                '''
        cv2.imwrite('c1.png', frame);
        print('Se tomo foto prro')
        cap.release()
            
class MainFrame(BoxLayout):
    
    def build(self):
        
        self.capture = cv2.VideoCapture(0)
        btn1 = Button(text='FOTITO PERRO', size=(200,100))
        arg = 123
        btn1.bind(on_press=self.auth)
        self.add_widget(btn1)
        #self.my_camera = KivyCamera(capture=self.capture, fps=60)
        self.add_widget(KivyCamera(capture=self.capture, fps=60))
        return self

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()
    def auth(self, instance):
        x = 0
        print('auth called')
        ret,foto = self.capture.read()
        cv2.imwrite('capture'+str(x)+'.png', foto)
        x=x+1
        print('El valor de x esta en: '+str(x))
        
    
class CamApp(App):
    def build(self):
        frame = MainFrame()
        return frame.build()
if __name__ == '__main__':
    CamApp().run()