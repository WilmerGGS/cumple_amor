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
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

# 🔹 Vibración para Android (sin errores en VS Code)
VIBRATION_AVAILABLE = False
try:
    from jnius import autoclass  # type: ignore
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    Vibrator = autoclass('android.os.Vibrator')
    vibrator = PythonActivity.mActivity.getSystemService(Context.VIBRATOR_SERVICE)
    VIBRATION_AVAILABLE = True
except Exception:
    # En PC no hay vibración, pero no hay problema
    vibrator = None

Window.clearcolor = (1, 1, 1, 1)

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

        # 🎵 Cargar música (pon el nombre exacto de tu archivo)
        self.musica = SoundLoader.load('cumple_cancion.wav')  # 🔹 Cambia por tu archivo
        if self.musica:
            self.musica.volume = 0.7  # Volumen al 70%

        # Fondo
        self.fondo = Image(source='fondo_cumple.jpg', allow_stretch=True, keep_ratio=False)
        self.root.add_widget(self.fondo)

        # Imagen de ustedes
        self.foto = Image(
            source='foto_de_dos.jpg',
            size_hint=(0.6, 0.27),
            pos_hint={'center_x': 0.5, 'top': 0.88}
        )
        self.root.add_widget(self.foto)

        # Texto del mensaje (BLANCO CON BORDE)
        self.mensaje = Label(
            text='',
            font_size='14sp',
            color=(1, 1, 1, 1),  # 🔹 BLANCO
            halign='center',
            valign='top',
            size_hint=(0.92, 0.48),
            pos_hint={'center_x': 0.5, 'top': 0.60}
        )
        self.mensaje.bind(size=self.mensaje.setter('text_size'))
        # 🔹 Agregar borde negro al texto
        self.mensaje.outline_width = 2
        self.mensaje.outline_color = (0, 0, 0, 1)
        self.root.add_widget(self.mensaje)

        # --- BOTÓN CON ANIMACIÓN DE PULSO ---
        self.boton_layout = FloatLayout(
            size_hint=(0.6, 0.09),
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
            spacing=dp(8),
            size_hint=(0.9, 0.75),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Texto blanco
        self.boton_texto = Label(
            text='Ver tu sorpresa',
            font_size='15sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.boton_texto.bind(size=self.boton_texto.setter('text_size'))

        # Icono regalo
        self.icono_regalo = Image(
            source='regalo.png',
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            pos_hint={'center_y': 0.5}
        )

        self.contenido_boton.add_widget(self.boton_texto)
        self.contenido_boton.add_widget(self.icono_regalo)
        self.boton_layout.add_widget(self.contenido_boton)

        # Botón invisible
        self.boton = Button(
            background_normal='',
            background_color=(0, 0, 0, 0),
            size_hint=(0.6, 0.09),
            pos_hint={'center_x': 0.5, 'y': 0.05}
        )
        self.boton.bind(on_press=self.mostrar_mensaje)

        self.root.add_widget(self.boton_layout)
        self.root.add_widget(self.boton)

        # 🔹 INICIAR ANIMACIÓN DE PULSO DEL BOTÓN
        self.animar_pulso_boton()

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
            "No olvides que TE AMO Cumpleañera mia, Te Adoro con mi alma y siempre vas a estar en mi corazón. "
            "Este es el primero de muchos regalos que vas a recibir de todas las personas que te aman. "
            "Nunca olvides que eres muy importante para mi vida, y este regalo que lo hice con mucho cariño y amor es una prueba de ello. "
            "Te amo más de lo que las palabras pueden expresar. PD: Tú novio, marido, esposo, TÚ TODO."
        )
        self.index = 0

        return self.root

    def actualizar_fondo(self, *args):
        self.boton_fondo.pos = self.boton_layout.pos
        self.boton_fondo.size = self.boton_layout.size

    def animar_pulso_boton(self):
        """Animación de pulso continuo del botón como un corazón latiendo"""
        # Crecer
        anim_crecer = Animation(size_hint=(0.65, 0.095), duration=0.8)
        # Volver al tamaño normal
        anim_reducir = Animation(size_hint=(0.6, 0.09), duration=0.8)
        
        # Secuencia: crecer -> reducir -> repetir
        anim_crecer.bind(on_complete=lambda *args: anim_reducir.start(self.boton_layout))
        anim_reducir.bind(on_complete=lambda *args: anim_crecer.start(self.boton_layout))
        
        anim_crecer.start(self.boton_layout)

    def efecto_brillo(self):
        """Efecto de brillo al presionar el botón"""
        def hacer_brillar(*args):
            with self.boton_layout.canvas.before:
                Color(1, 0.7, 0.8, 1)  # Rosa más claro (brillo)
                self.boton_fondo = RoundedRectangle(radius=[30])
            self.boton_layout.bind(pos=self.actualizar_fondo, size=self.actualizar_fondo)
        
        def volver_normal(*args):
            with self.boton_layout.canvas.before:
                Color(1, 0.4, 0.6, 1)  # Color normal
                self.boton_fondo = RoundedRectangle(radius=[30])
            self.boton_layout.bind(pos=self.actualizar_fondo, size=self.actualizar_fondo)
        
        hacer_brillar()
        Clock.schedule_once(volver_normal, 0.3)

    def vibrar_celular(self):
        """Vibra el celular si está disponible"""
        if VIBRATION_AVAILABLE and vibrator:
            try:
                vibrator.vibrate(200)  # Vibra por 200ms
            except Exception:
                pass

    def mover_corazones(self, dt):
        for c in self.corazones:
            c.mover()

    def mostrar_mensaje(self, instance):
        # 🔹 VIBRAR
        self.vibrar_celular()
        
        # 🔹 EFECTO BRILLO
        self.efecto_brillo()
        
        # 🔹 REPRODUCIR MÚSICA
        if self.musica:
            self.musica.play()
        
        # Deshabilitar botón y hacer fade out
        self.boton.disabled = True
        anim_fade = Animation(opacity=0, duration=1.5)
        anim_fade.start(self.boton_layout)
        
        # Iniciar escritura del mensaje
        Clock.schedule_interval(self.escribir_letra, 0.05)

    def escribir_letra(self, dt):
        if self.index < len(self.texto_completo):
            self.mensaje.text += self.texto_completo[self.index]
            self.index += 1
        else:
            # Corazón final
            self.emoji_corazon = Image(
                source='corazon_pequeno.png',
                size_hint=(None, None),
                size=(dp(80), dp(80)),
                pos_hint={'center_x': 0.5, 'y': 0.15},
                opacity=0  # Empieza invisible
            )
            self.root.add_widget(self.emoji_corazon)
            
            # Animación de aparición del corazón
            anim_corazon = Animation(opacity=1, duration=1.5)
            anim_corazon.start(self.emoji_corazon)
            
            return False


if __name__ == '__main__':
    CumpleApp().run()