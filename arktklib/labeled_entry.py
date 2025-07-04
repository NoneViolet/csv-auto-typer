import tkinter as tk
from typing import Optional, Literal, Any

class LabeledEntry(tk.Frame):
    """
    ラベル付きentryウィジェットを作成するGUIコンポーネント。
    入力と値の取得のみを目的とした簡易的なentryが必要な際に利用できる。

    attributes:
        master (tk.Misc): 親ウィジェット
        category (str): ラベルに表示するテキスト
        validate (Optional[str]): バリデーションチェックのトリガー
        validate_command (Optional[tuple[str, str]]): バリデーションコマンド
        pady (int): 上下の余白
        entry_width (int): entryウィジェットの幅
        **kwargs (Any): entryに追加で引数を渡します

    methods:
        get(): エントリーウィジェットの値を取得する。
    """
    
    def __init__(
            self,
            master: tk.Misc,
            category: str,
            validate: Optional[Literal['none', 'focus', 'focusin', 'focusout', 'key', 'all']] = None,
            validate_command: Optional[tuple[str, str]] = None,
            label_width: int = 15,
            entry_width: int = 15,
            **kwargs: Any
            ) -> None:
        """
        LabeledEntryの初期化。
        Attributes:
            master (tk.Misc): 親ウィジェット
            category (str): ラベルに表示するテキスト
            validate (Optional[str]): 入力検証の種類（例: "key"）
            validate_command (Optional[int]): 入力検証のコマンド
            pady (Optional[int]): フレームの上下の余白
            entry_width (Optional[int]): エントリーウィジェットの幅
        """
        super().__init__(master)

        frame = tk.Frame(self)
        frame.pack()

        label = tk.Label(frame, text=f"{category}：", width=label_width, anchor="e")
        label.pack(side=tk.LEFT)
        
        if validate and validate_command:
            self.entry = tk.Entry(frame, width=entry_width, validate=validate, validatecommand=validate_command, **kwargs)
            self.entry.pack(side=tk.LEFT)
        else:
            self.entry = tk.Entry(frame, width=entry_width)
            self.entry.pack(side=tk.LEFT)

    def get(self):
        """
        エントリーウィジェットの値を取得する。

        Returns:
            str: entryウィジェットに入力されたテキスト
        """
        return self.entry.get()
