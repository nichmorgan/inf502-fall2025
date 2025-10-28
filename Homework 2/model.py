import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from loadData import Measure


def get_metrics(y_true, y_pred):
    return {
        "r2": r2_score(y_true, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        "mae": mean_absolute_error(y_true, y_pred),
    }


def compare_models(baseline, new_model):
    print(
        f"\nBaseline: R2={baseline['r2']:.4f}, RMSE={baseline['rmse']:.2f}, MAE={baseline['mae']:.2f}"
    )
    print(
        f"New: R2={new_model['r2']:.4f}, RMSE={new_model['rmse']:.2f}, MAE={new_model['mae']:.2f}"
    )
    print(
        f"Change: R2={new_model['r2']-baseline['r2']:+.4f}, RMSE={new_model['rmse']-baseline['rmse']:+.2f}, MAE={new_model['mae']-baseline['mae']:+.2f}"
    )


def plot_residuals(y_true, y_pred):
    residuals = y_true - y_pred
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].scatter(y_pred, residuals, alpha=0.1, s=1)
    axes[0].axhline(y=0, color="r", linestyle="--")
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Residuals")
    axes[0].set_title("Residuals vs Predicted")

    axes[1].scatter(y_true, y_pred, alpha=0.5, s=1)
    max_val = max(y_true.max(), y_pred.max())
    axes[1].plot([0, max_val], [0, max_val], "r--", label="Perfect Prediction")
    axes[1].set_xlabel("Actual")
    axes[1].set_ylabel("Predicted")
    axes[1].set_title("Predicted vs Actual")
    axes[1].legend()

    plt.tight_layout()
    return fig


def findBouts(
    dataFrame: pd.DataFrame,
    column_name: str,
    minimum_threshold: float,
    minimum_duration_in_minutes: int,
    tolerance: float,
):
    """Find bouts using DateTime differences, grouped by Subject."""
    # Filter to only active rows (above threshold)
    active_df = dataFrame[dataFrame[column_name] >= minimum_threshold].copy()

    bouts: list[pd.DataFrame] = []
    durations: list[int] = []

    # Process each subject separately
    for subject_id, subject_data in active_df.groupby("Subject"):
        subject_data = subject_data.sort_values("DateTime").copy()

        # Calculate time difference between consecutive rows (in minutes)
        subject_data["time_diff"] = (
            subject_data["DateTime"].diff().dt.total_seconds() / 60
        )

        # New bout starts when gap > 1 + tolerance minutes
        subject_data["is_new_bout"] = subject_data["time_diff"] > (1 + tolerance)
        subject_data["bout_id"] = subject_data["is_new_bout"].fillna(True).cumsum()

        # Group by bout and filter by minimum duration
        for _, group in subject_data.groupby("bout_id"):
            duration = len(group)  # Each row = 1 minute
            if duration >= minimum_duration_in_minutes:
                bouts.append(
                    group.drop(columns=["time_diff", "is_new_bout", "bout_id"])
                )
                durations.append(duration)

    return bouts, durations
