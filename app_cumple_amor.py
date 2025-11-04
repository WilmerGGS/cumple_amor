from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from random import randint
from kivy.graphics import Ellipse, Color
from kivy.uix.boxlayout import BoxLayout

Window.clearcolor = (1, 1, 1, 1)

class Corazon(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'corazon_brillante.png'  # imagen del corazón
        self.size_hint = (None, None)
        self.size = (40, 40)
        self.x = randint(0, Window.width - 40)
        self.y = randint(-100, 0)
        self.velocidad = randint(1, 3)

    def mover(self):
        self.y += self.velocidad
        if self.y > Window.height:
            self.y = randint(-100, 0)
            self.x = randint(0, Window.width - 40)


class CumpleApp(App):
    def build(self):
        self.root = FloatLayout()

        # Fondo personalizado
        self.fondo = Image(source='fondo.jpg', allow_stretch=True, keep_ratio=False)
        self.root.add_widget(self.fondo)

        # Imagen de ustedes (encima del fondo)
        self.foto = Image(source='foto.jpg', size_hint=(0.8, 0.4), pos_hint={'center_x': 0.5, 'top': 0.9})
        self.root.add_widget(self.foto)

        # Texto del mensaje (inicialmente vacío)
        self.mensaje = Label(
            text='',
            font_size='20sp',
            color=(1, 0, 0, 1),
            halign='center',
            valign='middle',
            size_hint=(0.9, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        self.mensaje.bind(size=self.mensaje.setter('text_size'))
        self.root.add_widget(self.mensaje)

        # Botón
        self.boton = Button(
            text=' Presiona para ver tu sorpresa ',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            background_color=(1, 0.7, 0.8, 1),
            font_size='18sp'
        )
        self.boton.bind(on_press=self.mostrar_mensaje)
        self.root.add_widget(self.boton)

        # Corazones animados
        self.corazones = [Corazon() for _ in range(25)]
        for c in self.corazones:
            self.root.add_widget(c)
        Clock.schedule_interval(self.mover_corazones, 1/30)

        # Texto romántico
        self.texto_completo = (
            "Feliz cumpleaños, mi catira hermosa.\n\n"
            "Eres la persona que hace que cada día valga la pena. "
            "Hoy celebro tu vida y todo lo hermoso que traes al mío. "  
            "Te amo más de lo que las palabras pueden expresar. "
        )
        self.index = 0

        return self.root

    def mover_corazones(self, dt):
        for c in self.corazones:
            c.mover()

    def mostrar_mensaje(self, instance):
        self.boton.disabled = True
        Clock.schedule_interval(self.escribir_letra, 0.05)

    def escribir_letra(self, dt):
        if self.index < len(self.texto_completo):
            self.mensaje.text += self.texto_completo[self.index]
            self.index += 1
        else:
            # Obtener posición del label para colocar el corazón al lado derecho
            # Usa la posición del label y ajusta con un pequeño offset
            x = self.mensaje.pos_hint.get('center_x', 0.5)
            y = self.mensaje.pos_hint.get('center_y', 0.4)

            # Crear el corazón pequeño justo al lado del texto
            self.emoji_corazon = Image(
                source='corazon_pequeno.png',
                size_hint=(None, None),
                size=(40, 40),
                pos_hint={'center_x': x + 0.08, 'center_y': y - 0.09}  # Mueve más o menos según necesites
            )
            self.root.add_widget(self.emoji_corazon)
            return False





if __name__ == '__main__':
    CumpleApp().run()
