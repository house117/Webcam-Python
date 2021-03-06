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
from PIL import Image as imaag
import time
import cv2
import os
from functools import partial

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '710')
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
            
class MainFrame(GridLayout):
    
    def build(self):
        #Layout principal y camara
        self.rows = 2
        self.cols = 1
        self.orientation = 'vertical'
        self.capture = cv2.VideoCapture(0)
        #self.my_camera = KivyCamera(capture=self.capture, fps=60)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720);
        self.camera = KivyCamera(capture=self.capture, fps=60)
        
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
        btnColorPNG = ToggleButton(text='PNG', group='format', state='down')
        btnColorJPG = ToggleButton(text='JPG', group='format')
        btnColorGIF = ToggleButton(text='GIF', group='format')
        btnColorBMP = ToggleButton(text='BMP', group='format')
        LayoutBotonesFormato.add_widget(lblTitleFormato)
        LayoutBotonesFormato.add_widget(btnColorPNG)
        LayoutBotonesFormato.add_widget(btnColorJPG)
        LayoutBotonesFormato.add_widget(btnColorGIF)
        LayoutBotonesFormato.add_widget(btnColorBMP)
        #Group of buttons to select the size
        LayoutBotonesRes = BoxLayout(size_hint=(.2, .8),
                                       pos=(500, 60))
        LayoutBotonesRes.orientation = 'vertical'
        lblTitleRes = Label(text='Resolucion:')
        btnColor720 = ToggleButton(text='1280x720', group='size', state='down')
        btnColor480 = ToggleButton(text='800x600', group='size')
        btnColor360 = ToggleButton(text='640x360', group='size')
        LayoutBotonesRes.add_widget(lblTitleRes)
        LayoutBotonesRes.add_widget(btnColor720)
        LayoutBotonesRes.add_widget(btnColor480)
        LayoutBotonesRes.add_widget(btnColor360)
        #Adding Layouts to lower layout
        LayoutBotonCaptura.add_widget(btnCaptura)
        LayoutBotonCaptura.add_widget(LayoutBotonesColor)
        LayoutBotonCaptura.add_widget(LayoutBotonesFormato)
        LayoutBotonCaptura.add_widget(LayoutBotonesRes)
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
        currentFormat=[f for f in ToggleButton.get_widgets('format') if f.state=='down'][0]
        currentSize=[s for s in ToggleButton.get_widgets('size') if s.state=='down'][0]
        imageFinalName = ''
        print(currentColor.text)
        ret,foto = self.capture.read()
        if currentColor.text == 'B/N':
            foto = cv2.cvtColor(foto, cv2.COLOR_RGB2GRAY)
        elif currentColor.text == 'Binarizada':
            foto = cv2.cvtColor(foto, cv2.COLOR_RGB2GRAY)
            #NORMAL thresholding (global)
            ret,foto = cv2.threshold(foto,127,255,cv2.THRESH_BINARY)
            #Adaptive MEAN Thresholding
            #foto = cv2.adaptiveThreshold(foto,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            #cv2.THRESH_BINARY,11,2)
            #Adaptive Gaussian Thresholding
            #foto = cv2.adaptiveThreshold(foto,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            #cv2.THRESH_BINARY, 11, 2)
        #Format to save.
        if currentFormat.text == 'PNG':
            compression_params = [cv2.IMWRITE_PNG_COMPRESSION, 9] 
            cv2.imwrite(timestr+'.png', foto, compression_params)
            imageFinalName = timestr+'.png'
        elif currentFormat.text == 'JPG':
            cv2.imwrite(timestr+'.jpg', foto, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            imageFinalName = timestr+'.jpg'
        elif currentFormat.text == 'GIF':
            compression_params = [cv2.IMWRITE_PNG_COMPRESSION, 9] 
            cv2.imwrite(timestr+'.png', foto, compression_params)
            im = imaag.open(timestr+".png")
            im = im.convert('RGB').convert('P', palette=imaag.ADAPTIVE)
            os.remove(timestr+".png")
            im.save(timestr+'.gif')
            imageFinalName = timestr+'.gif'
        elif currentFormat.text == 'BMP':
            print('La pidio BMP el prro')
            compression_params = [cv2.IMWRITE_PNG_COMPRESSION, 9] 
            cv2.imwrite(timestr+'.png', foto, compression_params)
            img = imaag.open(timestr+".png")
            file_out = timestr+'.bmp'
            if len(img.split()) == 4:
                # prevent IOError: cannot write mode RGBA as BMP
                r, g, b, a = img.split()
                img = imaag.merge("RGB", (r, g, b))
                img.save(file_out)
                imageFinalName = file_out
            else:
                img.save(file_out)
                imageFinalName = file_out
                os.remove(timestr+".png")
        else:
            cv2.imwrite(timestr+'.png', foto)
        #Resize if necesary
        if currentSize.text == '800x600':
            print('Entro 360')
            width = 800
            height = 600
            im = imaag.open(imageFinalName)
            im2 = im.resize((width, height), imaag.ANTIALIAS) 
            im2.save('800600'+imageFinalName)
        elif currentSize.text == '640x360':
            print('Entro 360')
            width = 32
            height = 32
            im = imaag.open(imageFinalName)
            im2 = im.resize((width, height), imaag.ANTIALIAS) 
            im2.save('640360'+imageFinalName)
            im3 = imaag.open('640360'+imageFinalName)
            F=[-1, -1, 0, 1, 1, 1, 0, -1];
            C=[0, 1, 1, 1, 0, -1, -1, -1];
            width, height  = im3.size
            sumatoria = 0
            for x in range(1, width, 3):
                for y in range(1, height, 3):
                    #if(((x+1)%3) == 0 and ((y+1)%3) == 0):
                    print ('('+str(x)+', '+str(y)+')')
                    r0 = im3.getpixel((x,y))
                    sumatoria+=r0
                    print('Valores dentro del subfor, vuelta en 8')
                    for i in range(0, 8):
                        m = x+F[i]
                        n = y+C[i]
                        print ('('+str(m)+', '+str(n)+')')
                        if ((((m >= 0) and (m <= width)) and ((n >= 0) and (n <= height))) and ((n != width) and (m != height))):
                            r = im3.getpixel((m,n))
                            sumatoria+=r
                    sumatoria/=9
                    im3.putpixel((x, y), int(sumatoria))
                    for i in range(0, 8):                            
                        m = x+F[i]
                        n = y+C[i]
                        if ((((m >= 0) and (m <= width)) and ((n >= 0) and (n <= height))) and ((n != width) and (m != height))):
                            r = im3.getpixel((m,n))
                            im3.putpixel((m, n), int(sumatoria))
                
            im3.save('EJERCICIO'+imageFinalName)
                    
class CamApp(App):
    def build(self):
        frame = MainFrame()
        return frame.build()
if __name__ == '__main__':
    CamApp().run()