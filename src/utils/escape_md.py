#этот метод нужен для корректного отображения символов в MarkdownV2
def escape_md(text: str) -> str:
    """Экранирует спецсимволы для MarkdownV2."""
    if not isinstance(text, str):
        text = str(text)
    return text.translate(str.maketrans({
        '_': r'\_',
        '*': r'\*',
        '[': r'\[',
        ']': r'\]',
        '(': r'\(',
        ')': r'\)',
        '~': r'\~',
        '`': r'\`',
        '>': r'\>',
        '#': r'\#',
        '+': r'\+',
        '-': r'\-',
        '=': r'\=',
        '|': r'\|',
        '{': r'\{',
        '}': r'\}',
        '!': r'\!'
    }))