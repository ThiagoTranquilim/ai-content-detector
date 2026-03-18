from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


def save_confusion_matrix_figure(
    y_true: Sequence[int],
    y_pred: Sequence[int],
    output_path: str | Path,
    labels: Sequence[str] = ("human", "ai"),
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.array(labels))

    fig, ax = plt.subplots(figsize=(5, 5))
    disp.plot(ax=ax, colorbar=False)
    plt.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
