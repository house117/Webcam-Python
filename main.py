# coding:utf-8
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
import time
import cv2
from functools import partial

Config.set('graphics', 'width', '625')
Config.set('graphics', 'height', '650')
Config.set('graphics','resizable',0)
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
#Lo que hace el botonciiito (por ahora no usamos esto)
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
            
class MainFrame(GridLayout):
    
    def build(self):
        #Layout principal y camara
        self.rows = 2
        self.cols = 1
        self.orientation = 'vertical'
        self.capture = cv2.VideoCapture(0)
        #self.my_camera = KivyCamera(capture=self.capture, fps=60)
        self.add_widget(KivyCamera(capture=self.capture, fps=60))
        #Down Part of the frame
        LayoutBotonCaptura = FloatLayout(size_hint_x=1, size_hint_y =.4)
        #Main button to capture image
        btnCaptura = Button(text='Tomar Foto',
                           size_hint=(.15, .15),
                           pos=(20,110))
        btnCaptura.bind(on_press=self.auth)
        #Group of buttons to select the color of the image:
        LayoutBotonesColor = BoxLayout(size_hint=(.2, .8),
                                       pos=(150, 60))
        LayoutBotonesColor.orientation = 'vertical'
        lblTitleColor = Label(text='Selección de color:')
        btnColorFull = ToggleButton(text='A color', group='color', state='down')
        btnColorBN = ToggleButton(text='B/N', group='color')
        btnColorBin = ToggleButton(text='Binarizada', group='color')
        LayoutBotonesColor.add_widget(lblTitleColor)
        LayoutBotonesColor.add_widget(btnColorFull)
        LayoutBotonesColor.add_widget(btnColorBN)
        LayoutBotonesColor.add_widget(btnColorBin)
        #Group of buttons to select the format to save the image:
        LayoutBotonesFormato = BoxLayout(size_hint=(.2, .8),
                                       pos=(310, 60))
        LayoutBotonesFormato.orientation = 'vertical'
        lblTitleFormato = Label(text='Selección de formato:')
        btnColorPNG = ToggleButton(text='PNG', group='Formato', state='down')
        btnColorJPG = ToggleButton(text='JPG', group='Formato')
        btnColorGIF = ToggleButton(text='GIF', group='Formato')
        btnColorBMP = ToggleButton(text='BMP', group='Formato')
        LayoutBotonesFormato.add_widget(lblTitleFormato)
        LayoutBotonesFormato.add_widget(btnColorPNG)
        LayoutBotonesFormato.add_widget(btnColorJPG)
        LayoutBotonesFormato.add_widget(btnColorGIF)
        LayoutBotonesFormato.add_widget(btnColorBMP)

        #Adding Layouts to lower layout
        LayoutBotonCaptura.add_widget(btnCaptura)
        LayoutBotonCaptura.add_widget(LayoutBotonesColor)
        LayoutBotonCaptura.add_widget(LayoutBotonesFormato)
        self.add_widget(LayoutBotonCaptura)
        return self

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()
    def auth(self, instance):
        #Obtenemos fecha para el nombre de la imagen
        timestr = time.strftime("%Y%m%d-%H%M%S")
        #Obtenemos el color
        currentColor=[t for t in ToggleButton.get_widgets('color') if t.state=='down'][0]
        currentFormat=[t for t in ToggleButton.get_widgets('color') if t.state=='down'][0]
        print(currentColor.text)
        ret,foto = self.capture.read()
        if currentColor.text == 'A color':
            print('Pidio a color el prro')
        elif currentColor.text == 'B/N':
            foto = cv2.cvtColor(foto, cv2.COLOR_RGB2GRAY)
            print('Pidio B/N el prro')
        elif currentColor.text == 'Binarizada':
            foto = cv2.cvtColor(foto, cv2.COLOR_RGB2GRAY)
            #NORMAL thresholding (global)
            #ret,foto = cv2.threshold(foto,127,255,cv2.THRESH_BINARY)
            #Adaptive MEAN Thresholding
            #foto = cv2.adaptiveThreshold(foto,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            #cv2.THRESH_BINARY,11,2)
            #Adaptive Gaussian Thresholding
            foto = cv2.adaptiveThreshold(foto,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY, 11, 2)

        #FORMATO A GUARDAR
        if currentColor.text == 'PNG':
            print('Pidio PNG el prro')
        elif currentColor.text == 'JPG':
            print('Pidio JPG el prro')
        elif currentColor.text == 'GIF':
            print('La pidio GIF el prro')
        elif currentColor.text == 'BMP':
            print('La pidio BMP el prro')
        
        cv2.imwrite(timestr+'.png', foto)
        
    
class CamApp(App):
    def build(self):
        frame = MainFrame()
        return frame.build()
if __name__ == '__main__':
    CamApp().run()