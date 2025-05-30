import pandas as pd

def extract_top_of_ticket(name):
    return name.split(" and ")[0].strip()

def assign_party(candidate_name):
    name = candidate_name.lower()
    if 'trump' in name:
        return 'REP'
    elif 'harris' in name:
        return 'DEM'
    else:
        return 'OTH'

def process_nebraska_plr(file_path):
    all_data = []
    sheet_dict = pd.read_excel(file_path, sheet_name=None, engine='xlrd', skiprows=5)

    for sheet_name, df in sheet_dict.items():
        if sheet_name == 'County Results':
            continue  # Skip county summary sheet

        # Normalize column names (remove whitespace)
        df.columns = df.columns.str.strip()

        if 'Precinct' not in df.columns:
            print(f"'Precinct' column not found in {sheet_name}. Skipping.")
            continue

        df = df[df['Precinct'].notnull()]
        df = df[~df['Precinct'].isin(['New or Former Resident', 'Countywide', 'TOTAL'])]

        candidate_cols = [col for col in df.columns if col not in ['Precinct', 'TOTALS']]

        for _, row in df.iterrows():
            precinct = row['Precinct']
            vote_counts = []

            for col in candidate_cols:
                try:
                    votes = int(row[col])
                except (ValueError, TypeError):
                    continue
                candidate_name = extract_top_of_ticket(col)
                vote_counts.append((candidate_name, votes))

            top_two = sorted(vote_counts, key=lambda x: x[1], reverse=True)[:2]

            for candidate, votes in top_two:
                all_data.append({
                    'county': sheet_name,
                    'precinct': precinct,
                    'candidate': candidate,
                    'votes': votes,
                    'party': assign_party(candidate)
                })

    final_df = pd.DataFrame(all_data)
    final_df.sort_values(by=['county', 'precinct'], inplace=True)
    final_df.to_csv('ne_plr_2024.csv', index=False)
    print(f"Processed {len(final_df)} rows across {len(sheet_dict) - 1} counties.")

process_nebraska_plr('NE_PLR_2024.xls')
