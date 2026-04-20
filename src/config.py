from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

# Absolute root of the edge_aoi project, regardless of working directory.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Config:
    seed: int = 42

    data_root: Path = _PROJECT_ROOT / "data/mvtec"
    category: str = "bottle"

    img_size: int = 224
    resize_size: int = 256
    imagenet_mean: Tuple[float, float, float] = (0.485, 0.456, 0.406)
    imagenet_std: Tuple[float, float, float] = (0.229, 0.224, 0.225)

    backbone: str = "wide_resnet50_2"
    use_pretrained: bool = True

    coreset_ratio: float = 0.10
    use_coreset: bool = True

    layer2_weight: float = 1.0

    # Gaussian sigma for heatmap smoothing (pixels at img_size resolution).
    # Values in the range 4–8 produce meaningful spatial smoothing.
    heatmap_sigma: float = 4.0

    output_root: Path = _PROJECT_ROOT / "outputs"
    memory_bank_dir: Path = _PROJECT_ROOT / "outputs/memory_banks"
    results_dir: Path = _PROJECT_ROOT / "outputs/results"
    figures_dir: Path = _PROJECT_ROOT / "outputs/results/figures"
    evaluation_dir: Path = _PROJECT_ROOT / "outputs/evaluation"
    benchmarks_dir: Path = _PROJECT_ROOT / "outputs/benchmarks"

    @property
    def category_root(self) -> Path:
        return self.data_root / self.category

    @property
    def baseline_bank_path(self) -> Path:
        return self.memory_bank_dir / f"{self.category}_full_bank.pt"

    @property
    def coreset_bank_path(self) -> Path:
        return self.memory_bank_dir / f"{self.category}_coreset_bank.pt"

    @property
    def threshold_path(self) -> Path:
        return self.results_dir / f"{self.category}_threshold.txt"

    @property
    def metrics_path(self) -> Path:
        return self.results_dir / f"{self.category}_metrics.json"

    def ensure_dirs(self):
        self.output_root.mkdir(parents=True, exist_ok=True)
        self.memory_bank_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.evaluation_dir.mkdir(parents=True, exist_ok=True)
        self.benchmarks_dir.mkdir(parents=True, exist_ok=True)
