from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class CalculatorApp(App):
    def build(self):
        self.title = 'آلة حاسبة بايثون'
        
        # شاشة العرض الخاصة بالآلة الحاسبة
        self.result_field = TextInput(
            font_size=36, 
            readonly=True, 
            halign='right', 
            multiline=False,
            size_hint=(1, 0.2)
        )
        
        # التخطيط الرئيسي للتطبيق
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(self.result_field)

        # زر مسح الشاشة (C)
        clear_btn = Button(
            text=' (C)', 
            font_size=20, 
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(1, 0.1)
        )
        clear_btn.bind(on_press=self.on_clear)
        main_layout.add_widget(clear_btn)

        # شبكة الأزرار (الأرقام والعمليات الحسابية)
        buttons_layout = GridLayout(cols=4, spacing=5, size_hint=(1, 0.7))
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', '=', '+'
        ]

        for char in buttons:
            btn = Button(text=char, font_size=28)
            btn.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(btn)

        main_layout.add_widget(buttons_layout)
        return main_layout

    # منطق الأزرار والعمليات الحسابية
    def on_button_press(self, instance):
        current_text = self.result_field.text
        text = instance.text
        
        if text == '=':
            try:
                # تنفيذ العملية الحسابية بلغة بايثون
                solution = str(eval(current_text))
                self.result_field.text = solution
            except Exception:
                self.result_field.text = 'خطأ'
        else:
            if current_text == 'خطأ':
                self.result_field.text = ''
            self.result_field.text += text

    # منطق زر التطهير
    def on_clear(self, instance):
        self.result_field.text = ''

if __name__ == '__main__':
    CalculatorApp().run()
