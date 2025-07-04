import tkinter as tk
from tkinter import filedialog
from typing import Callable, Optional, List, Tuple, Any
from .info_label import InfoLabel

class FileSelector(tk.Frame):
    """
    ファイル選択を行うWidgetを提供するGUIコンポーネント。
    - 選択するファイル種別を示すラベル表示
    - ボタンによるファイル選択
    - 選択中ファイルパスの取得が可能

    Attributes:
        category (str): ファイルの種別名（例: CSVファイル、設定ファイルなど）。ラベルやボタンに表示される。
        filetypes (List[Tuple[str, str]]): ファイル選択ダイアログで使用されるファイルフィルターの一覧。
        file_path (Optional[str]): 現在選択されているファイルの絶対パス。未選択ならNone。
        path_label (InfoLabel): ファイルパスを表示するためのカスタムラベル。
        button (tk.Button): ファイル選択用のボタン。
    """

    def __init__(
        self, 
        master: tk.Misc,
        category: str = "ファイル",
        filetypes: List[Tuple[str, str]] = [("すべてのファイル", "*.*")],
        on_select: Optional[Callable[[str], None]] = None,
        **kwargs: Any
    ) -> None:
        """
        FileSelectorの初期化。

        Args:
            master (tk.Misc): 親ウィジェット。
            category (str): ラベルやボタンに表示するファイルのカテゴリ名。
            filetypes (List[Tuple[str, str]]): filedialogで使用するファイルタイプフィルター。
            **kwargs: InfoLabelおよびtk.Labelに渡す追加設定（anchorなど）。
        """
        super().__init__(master)
        self.category: str = category
        self.filetypes: List[Tuple[str, str]] = filetypes
        self.file_path: Optional[str] = None
        self.on_select: Optional[Callable] = on_select

        file_selector_frame = tk.Frame(self)
        file_selector_frame.pack()

        self.button: tk.Button = tk.Button(file_selector_frame, text=f"{self.category}を選択", command=self._select_file)
        self.button.pack()

        self.path_label: InfoLabel = InfoLabel(file_selector_frame, category=self.category, **kwargs)
        self.path_label.pack()

    def get(self) -> Optional[str]:
        """
        現在選択されているファイルパスを取得する。

        Returns:
            Optional[str]: ファイルパス。ファイルが未選択の場合はNone。
        """
        return self.file_path
    
    def set(self, path: str) -> None:
        """
        現在選択されているファイルパスを変更する。
        """
        if path:
            self.file_path = path
            self.path_label.set(path)

    def _select_file(self) -> None:
        """
        ボタン押下時に実行する処理。
        ファイルダイアログを開き、選択したファイルパスを保持する。
        """

        path = filedialog.askopenfilename(filetypes=self.filetypes)
        self.set(path)
        if self.on_select:
            self.on_select(path)