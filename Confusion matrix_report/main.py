import pandas as pd

df = pd.read_json("eval_compliance_demo.jsonl", lines=True)

label_map = {"Y": 1, "N": 0}

df["y_true"] = df["ground_truth"].apply(lambda x: label_map[x["Compliant"]])
df["y_pred"] = df["slm_prediction"].apply(lambda x: label_map[x["Compliant"]])

from sklearn.metrics import confusion_matrix, classification_report

cm = confusion_matrix(df["y_true"], df["y_pred"])
print(cm)

print(classification_report(
    df["y_true"],
    df["y_pred"],
    target_names=["Non-Compliant", "Compliant"]
))

cm = confusion_matrix(df["y_true"], df["y_pred"])

import numpy as np

cm_normalized = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

import matplotlib.pyplot as plt
import seaborn as sns

labels = ["Non-Compliant", "Compliant"]

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm_normalized,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    xticklabels=labels,
    yticklabels=labels
)

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Confusion Matrix (Normalized)")

plt.tight_layout()
plt.show()

report = classification_report(
    df["y_true"],
    df["y_pred"],
    target_names=["Non-Compliant", "Compliant"],
    output_dict=True
)
metrics_text = (
    f"Compliant → Precision: {report['Compliant']['precision']:.2f}, "
    f"Recall: {report['Compliant']['recall']:.2f}, "
    f"F1: {report['Compliant']['f1-score']:.2f}\n"
    f"Accuracy: {report['accuracy']:.2f}"
)

plt.figure(figsize=(7, 6))

plt.suptitle(
    "SLM Compliance Evaluation",
    fontsize=14,
    fontweight="bold"
)

plt.title(metrics_text, fontsize=10)

sns.heatmap(
    cm_normalized,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    xticklabels=labels,
    yticklabels=labels
)

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.show()

plt.savefig(
    "confusion_matrix_compliance.png",
    dpi=300,
    bbox_inches="tight"
)
