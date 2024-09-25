### README.md

# Stock Data Scraper & Financial Data API Fetcher

This Python project scrapes stock data from a financial website and supplements the data with additional financial details from an external API. The script has been designed with a specific focus on gathering Halal stock data, but it can also retrieve general stock data. The dataset is valuable for users looking to perform stock analysis and valuations, particularly in the context of Sharia-compliant investments. It also allows users to see what stocks are undevalued compared to the market, thereby suggesting potential investment opportunities. 

## Features

### 1. **Web Scraping with Selenium**:
   - **Website Chosen**: The website chosen for scraping is Practical Islamic Finance, which provides comprehensive data on the Halal status of stocks. It was selected for its relevance to investors interested in ethically compliant stocks. 
   - **Data Gathered**: The scraper collects the following fields for each stock:
     - **Company Name**: The name of the company.
     - **Ticker**: The stock symbol.
     - **Halal Status**: The status of whether the stock is Sharia-compliant (e.g., "Comfortable").
   - **Purpose**: This data is useful for individuals looking to invest in ethically compliant stocks, particularly in the context of Islamic finance, which requires investors to ensure that their investments are free from prohibited industries.

### 2. **API Data Gathering**:
   - **FinancialModelingPrep API**: We utilize this API to retrieve additional financial data for each stock, including:
     - **Price**: The current stock price.
     - **DCF Value**: Discounted Cash Flow value, used for stock valuation.
     - **Industry**: The industry the company operates in.
     - **Sector**: The sector the company belongs to.
     - **Description**: A brief description of the company.
   - **Purpose**: This additional data helps in performing stock valuations by comparing the current price with the company's intrinsic value, which is derived from the DCF analysis.

## Value of the Dataset

This dataset provides **unique value** for the following reasons:
- **Ethical Investment Data**: It combines both financial performance data and Halal status, which is crucial for investors seeking ethical or Sharia-compliant investments.
- **Valuation Insights**: By incorporating DCF data, users can assess whether a stock is **undervalued**, **overvalued**, or **correctly valued**, providing actionable insights for investment decisions.
- **Focused Niches**: There are limited datasets available that combine both financial performance and ethical status in one source, making this dataset a valuable tool for investors in Islamic finance or other ethical investment markets.

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- `pip` for package management

### Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### Install Required Dependencies
Install all necessary Python packages by running:

```bash
pip install -r requirements.txt
```

### Environmental Variables
Ensure you set up your environment variable in a .env file:
```bash
API_KEY= "your api key here"
```

You can obtain an API key from [FinancialModelingPrep](https://financialmodelingprep.com/).

### Running the Program
To scrape the data and supplement it with API financial data, simply run the script:

```bash
python your_script_name.py
```

You will be prompted to:
- Enter the maximum number of stock entries you wish to scrape.
- Decide whether to scrape Halal-only stocks or the entire list. The output will depend on this selection. 

Once the scraping process is completed, the script will use the FinancialModelingPrep API to enrich the data with financial details and perform valuation analysis. The resulting data will be saved to a CSV file.

### Example CSV Output
You can expect the following columns in the output CSV:
- **UID**: Unique identifier for the stock.
- **Company Name**: Name of the company.
- **Ticker**: Stock symbol.
- **Halal Status**: Whether the stock is Halal or not.
- **Price**: Current stock price.
- **DCF Value**: Discounted cash flow value for valuation.
- **Industry**: The industry the company operates in.
- **Sector**: The sector of the company.
- **Description**: A description of the company.
- **Valuation**: Whether the stock is undervalued, overvalued, or correctly valued.

## Rate Limiting
The API calls are capped at 250 requests. If this limit is reached, no further API calls will be made, ensuring compliance with the API rate limits.

## NOTE:
The query part is not 100% complete yet, and is currently very basic. In the future, I will consdier linking it to an LLM to answer questions about the data more accurately. I did not want to include it in the initial version because I want to focus on scraping and API calling first.
# halal-stock
