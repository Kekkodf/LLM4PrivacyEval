from src import pipeline as pipl
import pandas as pd
import os


if __name__ == '__main__':
    key_list = pipl.read_key('key.txt')
    collection = 'msmarco-dl19'
    mechanisms = ['CMP','Mahalanobis', 'VickreyCMP', 'VickreyMhl']
    epsilons = [1, 5, 10, 12.5, 15, 17.5, 20, 25, 30, 50]
    model = 'llama-3.3-70b-versatile'
    for mech in mechanisms:
        dfs = []
        for eps in epsilons:
            dfs.append(pd.read_csv(f'./data/{collection}/{mech}/obfuscatedText_{mech}_{eps}.csv'))
        
        for df in dfs:
            df = df.groupby('text').sample(n=10, random_state=1).reset_index(drop=True)            

            final = pipl.get_answers(df, key_list, model)

            #save the results
            if os.path.exists(f'./output/{collection}/{model}/{mech}/'):
                final.to_csv(f'./output/{collection}/{model}/{mech}/answers_{df["mechanism"][0]}_{df["epsilon"][0]}.csv', index=False)
            else:
                os.makedirs(f'./output/{collection}/{model}/{mech}/', exist_ok=True)
                final.to_csv(f'./output/{collection}/{model}/{mech}/answers_{df["mechanism"][0]}_{df["epsilon"][0]}.csv', index=False)
            

            