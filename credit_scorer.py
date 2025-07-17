import json
from collections import defaultdict
import matplotlib.pyplot as plt

def calculate_credit_scores(transactions):
    """
    Calculates credit scores for each wallet based on their transaction history.

    Args:
        transactions (list): A list of transaction dictionaries.

    Returns:
        dict: A dictionary with wallet addresses as keys and their credit scores as values.
    """
    wallet_scores = defaultdict(lambda: 500)
    wallet_transactions = defaultdict(list)

    for tx in transactions:
        wallet_transactions[tx['userWallet']].append(tx)

    for wallet, txs in wallet_transactions.items():
        score = 500
        total_volume = 0
        deposits_count = 0
        borrows_count = 0
        repays_count = 0
        redeems_count = 0
        liquidations_count = 0

        for tx in txs:
            amount = float(tx['actionData'].get('amount', 0))
            total_volume += amount

            if tx['action'] == 'deposit':
                score += 1
                deposits_count += 1
            elif tx['action'] == 'borrow':
                score -= 2 
                borrows_count += 1
            elif tx['action'] == 'repay':
                score += 2
                repays_count += 1
            elif tx['action'] == 'redeemunderlying':
                score += 1
                redeems_count += 1
            elif tx['action'] == 'liquidationcall':
                score -= 100 
                liquidations_count += 1

        # Adjust score based on transaction counts
        if deposits_count > 10:
            score += 20
        if borrows_count > 10:
            score -= 20
        if repays_count > 5:
            score += 15
        if redeems_count > 10:
            score += 10
        if liquidations_count > 0:
            score -= liquidations_count * 50

        # Normalize the score to be between 0 and 1000
        wallet_scores[wallet] = max(0, min(1000, score))

    return wallet_scores

def main():
    """
    Main function to load transactions, calculate scores, and save the results.
    """
    with open('user-wallet-transactions.json', 'r') as f:
        transactions = json.load(f)

    wallet_scores = calculate_credit_scores(transactions)

    with open('wallet_scores.json', 'w') as f:
        json.dump(wallet_scores, f, indent=4)

    print("Credit scores calculated and saved to wallet_scores.json")

    # Analysis
    scores = list(wallet_scores.values())
    
    # Score distribution graph
    plt.hist(scores, bins=10, range=(0, 1000), edgecolor='black')
    plt.title('Score Distribution')
    plt.xlabel('Credit Score')
    plt.ylabel('Number of Wallets')
    plt.xticks(range(0, 1001, 100))
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('score_distribution.png')
    
    # Behavior analysis
    lower_range_wallets = {wallet: score for wallet, score in wallet_scores.items() if score < 300}
    higher_range_wallets = {wallet: score for wallet, score in wallet_scores.items() if score > 700}

    print("\nWallets with lower scores (< 300):")
    for wallet, score in list(lower_range_wallets.items())[:5]:
        print(f"  Wallet: {wallet}, Score: {score}")

    print("\nWallets with higher scores (> 700):")
    for wallet, score in list(higher_range_wallets.items())[:5]:
        print(f"  Wallet: {wallet}, Score: {score}")

if __name__ == '__main__':
    main()