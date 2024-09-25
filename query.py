import pandas as pd

data = input("Enter name of file to query: ")

df = pd.read_csv(data)

def display_instructions(df):
    # Extract unique options from the DataFrame
    tickers = ', '.join(df['Ticker'].unique())
    companies = ', '.join(df['Company Name'].unique())
    sectors = ', '.join(df['Sector'].unique())
    industries = ', '.join(df['Industry'].unique())
    halal_statuses = ', '.join(df['Halal Status'].unique())
    valuations = ', '.join(df['Valuation'].unique())

    instructions = f"""
    Welcome to the Financial Data Query System!
    
    # Instructions for Asking Questions Using the `query_loop` Function

    1. How many halal stocks are there?
    2. How is [X] stock valued?
    3. Is [X] stock halal?
    4. Give me a list of all undervalued stocks.
    5. What are the companies in [X] industry?
    6. Describe [X] company
    7. What is the price of [Ticker]?

      Available Options:
    - **Tickers**: {tickers}
    - **Company Names**: {companies}
    - **Sectors**: {sectors}
    - **Industries**: {industries}
    """
    return instructions

# Main loop to accept user queries
def query_loop(df):
    print(display_instructions(df))
    while True:
        query = input("Ask your question (type 'exit' to quit): ")

        if query.lower() == 'exit':
            break

        # 1. How many halal stocks are there, give me the company names and tickers?
        if "how many halal stocks" in query.lower() or "halal stocks" in query.lower():
            halal_companies = df[df['Halal Status'] == 'Halal']
            count = halal_companies.shape[0]
            if count > 0:
                print(f"There are {count} halal stocks:")
                for idx, row in halal_companies.iterrows():
                    print(f"- {row['Company Name']} ({row['Ticker']})")
            else:
                print("No halal stocks found.")

        # 2. How is [X] stock valued?
        elif "how is" in query.lower() and "valued" in query.lower():
            company_name = query.lower().replace("how is", "").replace("valued", "").strip().title()
            result = df[df['Company Name'].str.contains(company_name, case=False, na=False)]
            if not result.empty:
                valuation = result.iloc[0]['Valuation']
                print(f"{company_name} is {valuation}.")
            else:
                print(f"Company '{company_name}' not found.")
        
        # 3. Is [X] stock halal?
        elif "is" in query.lower() and "halal" in query.lower():
            company_name = query.lower().replace("is", "").replace("halal", "").strip().title()
            result = df[df['Company Name'].str.contains(company_name, case=False, na=False)]
            if not result.empty:
                halal_status = result.iloc[0]['Halal Status']
                print(f"{company_name} is {halal_status}.")
            else:
                print(f"Company '{company_name}' not found.")
        
        # 4. Give me a list of all undervalued stocks.
        elif "undervalued stocks" in query.lower() or "undervalued" in query.lower():
            undervalued_companies = df[df['Valuation'] == 'Undervalued']
            if not undervalued_companies.empty:
                print("Undervalued companies:")
                for company, ticker in zip(undervalued_companies['Company Name'], undervalued_companies['Ticker']):
                    print(f"- {company} ({ticker})")
            else:
                print("No undervalued companies found.")
        
        # 5. What are the companies in [X] industry?
        elif "what are the companies in" in query.lower() and "industry" in query.lower():
            industry = query.lower().replace("what are the companies in", "").replace("industry", "").strip().title()
            result = df[df['Industry'].str.contains(industry, case=False, na=False)]
            if not result.empty:
                print(f"Companies in the {industry} industry:")
                for company, ticker in zip(result['Company Name'], result['Ticker']):
                    print(f"- {company} ({ticker})")
            else:
                print(f"No companies found in the {industry} industry.")
        
        # 6. Describe [X] company
        elif "describe" in query.lower():
            company_name = query.lower().replace("describe", "").strip().title()
            result = df[df['Company Name'].str.contains(company_name, case=False, na=False)]
            if not result.empty:
                description = result.iloc[0]['Description']
                print(f"{company_name}: {description}")
            else:
                print(f"Company '{company_name}' not found.")
        
        # Handling "What is the price of [Ticker]"
        elif "price" in query.lower() and "of" in query.lower():
            ticker = query.split("of")[-1].strip().upper()
            result = df[df['Ticker'] == ticker]['Price']
            if not result.empty:
                print(f"The price of {ticker} is {result.values[0]}")
            else:
                print("Company not found.")

query_loop(df)