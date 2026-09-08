
import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.label import Label

class MainApp(App):
    def build(self):
        return Label(text='Game Running Successfully!')

if __name__ == '__main__':
    MainApp().run()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
import random
import os

class CustomButton(Button):
    """입체감 연출을 위한 커스텀 START 버튼"""
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.default_color = (0.2, 0.6, 1, 1)
        self.pressed_color = (0.1, 0.4, 0.8, 1)
        self.background_color = self.default_color

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = self.pressed_color
        return super(CustomButton, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = self.default_color
        return super(CustomButton, self).on_touch_up(touch)


class LottoBall(FloatLayout):
    """원형 로또 공 위젯"""
    def __init__(self, **kwargs):
        super(LottoBall, self).__init__(**kwargs)
        self.bg_color = (0.2, 0.2, 0.2, 1)
        
        with self.canvas.before:
            self.color_instruction = Color(*self.bg_color)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
            
        self.bind(pos=self.update_ellipse, size=self.update_ellipse)

        self.label = Label(
            text='',
            bold=True,
            color=(1, 1, 1, 1),
            pos_hint={'x': 0, 'y': 0},
            size_hint=(1, 1)
        )
        self.add_widget(self.label)
        self.bind(size=self.update_font_size)

    def update_ellipse(self, *args):
        side = min(self.width, self.height)
        offset_x = self.x + (self.width - side) / 2
        offset_y = self.y + (self.height - side) / 2
        self.ellipse.pos = (offset_x, offset_y)
        self.ellipse.size = (side, side)

    def update_font_size(self, *args):
        ball_size = min(self.width, self.height)
        if ball_size > 0:
            self.label.font_size = f'{int(ball_size * 0.22)}dp'

    def set_ball_data(self, number, color):
        self.label.text = str(number)
        self.bg_color = color
        self.color_instruction.rgba = color

    def reset_ball(self):
        self.label.text = ''
        self.bg_color = (0.2, 0.2, 0.2, 1)
        self.color_instruction.rgba = self.bg_color


class LottoGame(FloatLayout):
    def __init__(self, **kwargs):
        super(LottoGame, self).__init__(**kwargs)
        
        # Pydroid 3 및 안드로이드 효과음 파일 검사 및 안전 로드
        sound_path = os.path.join(os.path.dirname(__file__), 'click.wav')
        self.sound = None
        if os.path.exists(sound_path):
            try:
                self.sound = SoundLoader.load(sound_path)
            except Exception:
                self.sound = None

        # 메인 레이아웃
        self.main_box = BoxLayout(
            orientation='vertical',
            padding=[10, 10, 10, 10],
            spacing=10,
            size_hint=(1, 1)
        )
        self.add_widget(self.main_box)

        # 1. 상단 타이틀
        self.title_label = Label(
            text='[b]L[color=ff0000]O[/color][color=0000ff]TT[/color][color=ff0000]O[/color][/b]', 
            markup=True, 
            size_hint_y=0.2
        )
        self.main_box.add_widget(self.title_label)

        # 2. 중앙 로또 공 배치 영역 (6개)
        self.balls_layout = GridLayout(cols=6, spacing=4, size_hint_y=0.25)
        self.balls = []
        
        for _ in range(6):
            ball = LottoBall()
            self.balls.append(ball)
            self.balls_layout.add_widget(ball)
            
        self.main_box.add_widget(self.balls_layout)

        # 3. 당첨 축하 텍스트 레이블
        self.result_label = Label(
            text='',
            bold=True,
            color=(0.2, 0.8, 0.4, 1),
            size_hint_y=0.15,
            halign='center',
            valign='middle'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.main_box.add_widget(self.result_label)

        # 4. 하단 영역 (KYM, START 버튼)
        self.bottom_layout = FloatLayout(size_hint_y=0.4)

        # 좌측 하단 KYM
        self.kym_label = Label(
            text='KYM',
            bold=True,
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(0.25, 0.2),
            pos_hint={'x': 0.0, 'y': 0.05},
            halign='left',
            valign='bottom'
        )
        self.kym_label.bind(size=self.kym_label.setter('text_size'))
        self.bottom_layout.add_widget(self.kym_label)

        # 우측 하단 START 버튼
        self.draw_button = CustomButton(
            text='START', 
            bold=True,
            size_hint=(0.28, 0.22),
            pos_hint={'right': 1.0, 'y': 0.05}
        )
        self.draw_button.bind(on_press=self.start_draw_sequence)
        self.bottom_layout.add_widget(self.draw_button)

        self.main_box.add_widget(self.bottom_layout)

        self.bind(size=self.update_screen_layout)

    def update_screen_layout(self, instance, value):
        base_size = min(self.width, self.height)
        self.title_label.font_size = f'{int(base_size * 0.045)}dp'
        self.draw_button.font_size = f'{int(base_size * 0.022)}dp'
        self.kym_label.font_size = f'{int(base_size * 0.025)}dp'
        self.result_label.font_size = f'{int(base_size * 0.035)}dp'

    def start_draw_sequence(self, instance):
        if self.sound:
            self.sound.stop()
            self.sound.play()

        self.draw_button.disabled = True
        self.result_label.text = ''

        for ball in self.balls:
            ball.reset_ball()

        self.selected_numbers = sorted(random.sample(range(1, 46), 6))

        delays = [0.0, 0.7, 1.4, 2.1, 2.8, 4.3]

        for i in range(6):
            Clock.schedule_once(lambda dt, idx=i: self.reveal_ball(idx), delays[i])

        Clock.schedule_once(lambda dt: self.start_blink_effect(), 4.3)

    def reveal_ball(self, index):
        num = self.selected_numbers[index]
        color = self.get_ball_color(num)
        self.balls[index].set_ball_data(num, color)

    def start_blink_effect(self):
        text = 'CONGRATULATIONS!!!'
        
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', text), 0.0)
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', ''), 0.25)
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', text), 0.5)
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', ''), 0.75)
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', text), 1.0)
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', ''), 1.25)
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text', text), 1.5)
        
        self.draw_button.disabled = False

    def get_ball_color(self, num):
        if num <= 10:
            return (0.95, 0.76, 0.2, 1)   # 노란색
        elif num <= 20:
            return (0.27, 0.54, 0.82, 1)  # 파란색
        elif num <= 30:
            return (0.87, 0.31, 0.26, 1)  # 빨간색
        elif num <= 40:
            return (0.55, 0.55, 0.55, 1)  # 회색
        else:
            return (0.4, 0.73, 0.42, 1)   # 초록색


class Lotto365App(App):
    def build(self):
        return LottoGame()


if __name__ == '__main__':
    Lotto365App().run()
