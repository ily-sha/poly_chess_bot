class Params:
    def __init__(self, text, reply_markup=None):
        self.text = text
        self.reply_markup = reply_markup

    def get_params(self):
        return {"text": self.text, "reply_markup": self.reply_markup}