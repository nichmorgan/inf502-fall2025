import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


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
