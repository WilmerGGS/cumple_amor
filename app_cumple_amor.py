from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from random import randint
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

# 🔹 NO fuerces el tamaño en celular
Window.clearcolor = (1, 1, 1, 1)

# --- Escalador mejorado para Android ---
def escalar(valor):
    """Escala valores usando dp (density-independent pixels) para Android."""
    return dp(valor)


class Corazon(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'corazon_brillante.png'
        self.size_hint = (None, None)
        self.size = (escalar(35), escalar(35))
        self.x = randint(0, int(Window.width) - 40)
        self.y = randint(-100, 0)
        self.velocidad = randint(1, 3)

    def mover(self):
        self.y += self.velocidad
        if self.y > Window.height:
            self.y = randint(-100, 0)
            self.x = randint(0, int(Window.width) - 40)


class CumpleApp(App):
    def build(self):
        self.root = FloatLayout()

        # Fondo
        self.fondo = Image(source='fondo_cumple.jpg', allow_stretch=True, keep_ratio=False)
        self.root.add_widget(self.fondo)

        # Imagen de ustedes
        self.foto = Image(
            source='foto_de_dos.jpg',
            size_hint=(0.65, 0.3),
            pos_hint={'center_x': 0.5, 'top': 0.88}
        )
        self.root.add_widget(self.foto)

        # Texto del mensaje
        self.mensaje = Label(
            text='',
            font_size='16sp',
            color=(1, 0, 0, 1),
            halign='center',
            valign='middle',
            size_hint=(0.9, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.38}
        )
        self.mensaje.bind(size=self.mensaje.setter('text_size'))
        self.root.add_widget(self.mensaje)

        # --- BOTÓN MEJORADO ---
        self.boton_layout = FloatLayout(
            size_hint=(0.6, 0.09),  # 🔹 Un poco más ancho
            pos_hint={'center_x': 0.5, 'y': 0.05}
        )

        # Fondo redondeado rosado
        with self.boton_layout.canvas.before:
            Color(1, 0.4, 0.6, 1)
            self.boton_fondo = RoundedRectangle(radius=[30])
        self.boton_layout.bind(pos=self.actualizar_fondo, size=self.actualizar_fondo)

        # Contenedor texto + icono
        self.contenido_boton = BoxLayout(
            orientation='horizontal',
            spacing=dp(8),  # 🔹 Más espacio
            size_hint=(0.9, 0.75),  # 🔹 Más grande dentro del botón
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Texto blanco
        self.boton_texto = Label(
            text='Ver tu sorpresa',
            font_size='15sp',  # 🔹 Tamaño fijo en sp
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.boton_texto.bind(size=self.boton_texto.setter('text_size'))

        # Icono regalo MUCHO MÁS GRANDE 🎁
        self.icono_regalo = Image(
            source='regalo.png',
            size_hint=(None, None),
            size=(dp(40), dp(40)),  # 🔹 MUCHO más grande usando dp()
            pos_hint={'center_y': 0.5}
        )

        self.contenido_boton.add_widget(self.boton_texto)
        self.contenido_boton.add_widget(self.icono_regalo)
        self.boton_layout.add_widget(self.contenido_boton)

        # Botón invisible
        self.boton = Button(
            background_normal='',
            background_color=(0, 0, 0, 0),
            size_hint=(0.6, 0.09),  # 🔹 Mismo tamaño que el layout
            pos_hint={'center_x': 0.5, 'y': 0.05}
        )
        self.boton.bind(on_press=self.mostrar_mensaje)

        self.root.add_widget(self.boton_layout)
        self.root.add_widget(self.boton)

        # Corazones animados
        self.corazones = [Corazon() for _ in range(25)]
        for c in self.corazones:
            self.root.add_widget(c)
        Clock.schedule_interval(self.mover_corazones, 1 / 30)

        # Texto romántico
        self.texto_completo = (
            "Feliz cumpleaños, mi catira hermosa.\n\n"
            "Te deseo lo mejor para tú vida mi amor, eres un gran ser humano soy muy afortunado de haberte conocido. "
            "Un año mas de vida, de experiencias y vivencias, que se te cumplan todos los deseos de tu corazón mi amor. "
            "No olvides que TE AMO Cumpleañera mia, Te Adoro con mi alma y siempre vas a estar en mi corazón."
            "Este es el primero de muchos regalos que vas a recibir de todas las personas que te aman."
            "Nunca olvides que eres muy importante para mi vida, y este regalo que lo hice con mucho cariño y amor es una prueba de ello."
            "Te amo más de lo que las palabras pueden expresar PD: Tú novio, marido, esposo, TÚ TODO. "
        )
        self.index = 0

        return self.root

    def actualizar_fondo(self, *args):
        self.boton_fondo.pos = self.boton_layout.pos
        self.boton_fondo.size = self.boton_layout.size

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
            # 🔹 Corazón final MUCHO MÁS GRANDE ❤️
            self.emoji_corazon = Image(
                source='corazon_pequeno.png',
                size_hint=(None, None),
                size=(dp(80), dp(80)),  # 🔹 MUCHO más grande (antes 60)
                pos_hint={'center_x': 0.5, 'center_y': 0.19}
            )
            self.root.add_widget(self.emoji_corazon)
            return False


if __name__ == '__main__':
    CumpleApp().run()