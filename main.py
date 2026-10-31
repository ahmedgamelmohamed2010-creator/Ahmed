from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import ast
import operator

_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculatorApp(App):
    def build(self):
        self.title = 'آلة حاسبة'

        self.result_field = TextInput(
            font_size=36,
            readonly=True,
            halign='right',
            multiline=False,
            size_hint=(1, 0.2)
        )

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(self.result_field)

        clear_btn = Button(
            text='C',
            font_size=20,
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(1, 0.1)
        )
        clear_btn.bind(on_press=self.on_clear)
        main_layout.add_widget(clear_btn)

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

    def safe_eval_expression(self, expression):
        expression = expression.strip()
        if not expression:
            raise ValueError('المدخلات فارغة')

        tree = ast.parse(expression, mode='eval')
        return self._eval_node(tree.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type not in _ALLOWED_BINOPS:
                raise ValueError('عملية غير مسموح بها')
            return _ALLOWED_BINOPS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type not in _ALLOWED_UNARYOPS:
                raise ValueError('عملية غير مسموح بها')
            return _ALLOWED_UNARYOPS[op_type](operand)

        raise ValueError('صيغة غير مدعومة')

    def on_button_press(self, instance):
        current_text = self.result_field.text
        text = instance.text

        if text == '=':
            try:
                solution = self.safe_eval_expression(current_text)
                self.result_field.text = str(solution)
            except Exception:
                self.result_field.text = 'خطأ'
        else:
            if current_text == 'خطأ':
                self.result_field.text = ''
            self.result_field.text += text

    def on_clear(self, instance):
        self.result_field.text = ''


if __name__ == '__main__':
    CalculatorApp().run()
