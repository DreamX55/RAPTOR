import os
import pandas as pd
import plotly.graph_objects as go

def main():
    out_dir = "reports/ieee_artifacts_phase4f"
    data_path = os.path.join(out_dir, "classified_attacks.csv")
    
    if not os.path.exists(data_path):
        print(f"Data file {data_path} not found. Run analysis script first.")
        return
        
    df = pd.read_csv(data_path)
    
    # Sankey Pipeline Stages:
    # 1. Total Injected (All rows)
    # 2. Retrieved vs Not Retrieved
    # 3. From Retrieved -> Failure Modes
    
    total = len(df)
    retrieved_df = df[df['retrieved_attack_top3'] == True]
    not_retrieved_df = df[df['retrieved_attack_top3'] == False]
    
    retrieved_count = len(retrieved_df)
    not_retrieved_count = len(not_retrieved_df)
    
    # Mode counts from retrieved
    mode_counts = retrieved_df['failure_mode'].value_counts().to_dict()
    
    # Nodes:
    # 0: Poison Injected
    # 1: Retrieved
    # 2: Retrieval Failure
    # 3: Successful Manipulation
    # 4: Prior Knowledge Dominance
    # 5: Prompt Resistance
    # 6: Partial Poison Adoption
    # 7: Generation Divergence
    
    labels = [
        "Poison Injected",
        "Retrieved",
        "Retrieval Failure",
        "Successful Manipulation",
        "Prior Knowledge Dominance",
        "Prompt Resistance",
        "Partial Poison Adoption",
        "Generation Divergence"
    ]
    
    label_to_idx = {l: i for i, l in enumerate(labels)}
    
    source = []
    target = []
    value = []
    
    # Injected -> Retrieved / Not Retrieved
    source.extend([0, 0])
    target.extend([1, 2])
    value.extend([retrieved_count, not_retrieved_count])
    
    # Retrieved -> Modes
    for mode, count in mode_counts.items():
        if mode in label_to_idx:
            source.append(1)
            target.append(label_to_idx[mode])
            value.append(count)
            
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = labels,
          color = "blue"
        ),
        link = dict(
          source = source,
          target = target,
          value = value
      ))])
      
    fig.update_layout(title_text="Attack Pipeline Transition (Sankey Diagram)", font_size=10)
    fig.write_image(os.path.join(out_dir, "attack_pipeline_sankey.png"), scale=3)
    
    print("Sankey diagram generated successfully.")

if __name__ == '__main__':
    main()
