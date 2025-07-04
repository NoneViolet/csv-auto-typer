import tkinter as tk
from typing import Optional

class InfoLabel(tk.Label):
    """
    'category: value' の形式でテキストを表示するカスタムLabel。
    categoryは固定され、valueのみを動的に変更できる。
    また、valueの文字数が多い場合、自動で省略（ellipsis）する機能を持つ。

    Attributes:
        category (str): ラベルのcategory（例: キー設定、選択ファイルなど）。
        value (str or None): ラベルのvalue。
        max_length (int): ellipsisが有効な場合、これ以上の文字数は省略される。(例: 「category: ...hogehoge」等)
        ellipsis (bool): Trueの場合、max_length以上の文字列は省略される。
    """

    def __init__(
        self,
        master: tk.Misc,
        category: str = "value",
        max_length: int = 20,
        ellipsis: bool = True,
        **kwargs
    ) -> None:

        """
        InfoLabelの初期化

        Args:
            master: 親ウィジェット、tkinter.Label。
            category (str): ラベルのcategory（例: キー設定、選択ファイルなど）。
            max_length (int): valueの最大表示文字数。ellipsisが有効な場合に使用される。
            ellipsis (bool): Trueの場合、max_length以下の文字列は省略される。
            **kwargs: tkinter.Labelへ渡されるその他の引数。
        """

        super().__init__(master, **kwargs)
        self.category: str = category
        self.value: Optional[str] = None
        self.max_length: int = max_length
        self.ellipsis: bool = ellipsis
        self.set("未設定")

    def set(self, text: str) -> None:
        """
        ラベルのvalue部分を変更し、表示を更新する。

        Args:
            text (str): 表示される文字列。(value部のみ)
        """
        self.value = text
        ellipsis_value = self._ellipsize(text) if self.ellipsis else text
        full_text = self._format_label(ellipsis_value)
        self.config(text=full_text)

    def get(self) -> Optional[str]:
        """
        value部分の文字列を返す。

        Returns:
            str or None: 設定されたvalue部分の文字列。
        """
        return self.value

    def get_category(self) -> str:
        """
        category部分の文字列を返す。

        Returns:
            str: 設定されたcategory部分の文字列。
        """
        return self.category

    def _format_label(self, text: str) -> str:
        """
        'category: value'表示するために文字列を成形する。
        categoryはselfから参照される。

        Args:
            text (str): value部分に表示する文字列。

        Returns:
            str: 'category: value'の形式の文字列。
        """
        return f"{self.category}： {text}"

    def _ellipsize(self, text: str) -> str:
        """
        value部分を表示用に整形する。
        value部分の文字列がmax_lengthを超えている場合、'...hoge'のように省略する。

        Args:
            text (str): 対象の文字列。

        Returns:
            str: 省略された文字列。max_lengthを超えない場合はそのまま返される。
        """
        if len(text) <= self.max_length:
            return text
        return f"...{text[-(self.max_length - 3):]}"
