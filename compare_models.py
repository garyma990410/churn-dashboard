from pathlib import Path
import pandas as pd


def main():
    p = Path('outputs/train_metrics.csv')
    if not p.exists():
        print('train_metrics.csv not found. Run python train.py first.')
        return
    df = pd.read_csv(p)
    df = df.sort_values(['auc', 'f1'], ascending=False).reset_index(drop=True)
    df.to_csv('outputs/model_comparison.csv', index=False)
    print(df)

if __name__ == '__main__':
    main()
