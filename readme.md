# Aave V2 DeFi Credit Scoring Model

This project implements a machine learning model to assign a credit score between **0 and 1000** to wallets based on their transaction history on the Aave V2 protocol. The model leverages unsupervised learning to identify behavioral patterns in a data-driven way, providing a robust measure of user reliability.

---

## Complete Architecture and Processing Flow

The model's architecture is a hybrid approach that combines machine learning with rule-based scoring for both accuracy and transparency.

### 1. Feature Engineering
Raw transaction data is aggregated per wallet to create a comprehensive feature profile. This includes:
* **Core Metrics**: `wallet_age_days`, `transaction_count`.
* **Behavioral Ratios**: Key indicators like `repay_to_borrow_ratio` and `deposit_to_borrow_ratio` are calculated to quantify financial health.
* **Risk Indicators**: The model flags wallets with a `liquidation_count` > 0 as high-risk.

### 2. Unsupervised Clustering (K-Means)
* The feature set is scaled to ensure all metrics contribute fairly.
* It is then fed into a **K-Means clustering algorithm**.
* The algorithm groups wallets into **5 distinct clusters**, where each cluster represents a specific behavioral archetype (e.g., "Safe Savers," "Leveraged Borrowers," "Liquidated Wallets").

### 3. Cluster Scoring Logic
* Each cluster is analyzed based on its average features (e.g., average liquidation rate, average repay ratio).
* A **risk rank** is calculated for each cluster. Clusters with high liquidation rates and low repayment ratios are ranked as the highest risk.
* This rank is then mapped to a credit score, with the lowest-risk cluster receiving a score around **950** and the highest-risk cluster receiving a score around **50**.

### 4. Final Output
The script outputs a `wallet_scores.json` file containing the final scores for each wallet and a `score_distribution.png` visualization.

---

## How to Run the Code

The entire process is contained within the provided Jupyter Notebook (`.ipynb` file).

1.  **Prerequisites**: Ensure you have the required libraries installed:
    ```bash
    pip install pandas scikit-learn matplotlib seaborn
    ```
2.  **Data**: Place the `user-wallet-transactions.json` file in the same directory as the notebook.
3.  **Execute**: Run all cells in the notebook in order from top to bottom. The final outputs, including `wallet_scores.json` and `score_distribution.png`, will be generated in the same directory.