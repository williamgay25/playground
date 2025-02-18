# High Level

## Inputs
PDF Files
No standard format
Some can be scanned
70% come from emails to pitchdeck@optoinvest.com
30% come from various channels that analysts upload

### metadata
Email
- Fund name
- Sender email domain
- Timestamp
- Original Filename
- Sometimes a date or version in filename

Portal Uploads
- Fund name
- Upload timestamp
- Analyst who uploaded
- Original filename
- Optional Notes

## Outputs:
Fund size
Returns
Strategy type
Management fee structure
Performance fee structure
Minimum investment amount
Fund inception date
Portfolio manager background
Risk metrics (sharpe and volatility)

## Queries
Seach across documents
Filter funds based on any metric
Compare metrics across funds
Export data for further analysis

# System Performance

Volume: 300 to 400 pdfs per week (can spike at quarter-end to 600 to 700)
Current Processing Speed: Analysts manually extract in 20 to 30 minutes. Looking to reduce this to near real time (sub 1 minute)
Accuracy: 95% currently with analysts. Want to maintain atleast 90%. Need system to flag low confidence extractions for human review.
LLM Usage: Can use OS and APIs. Need to consider cost, privacy, uptime & reliability.

# System Design

Intake
- Email Collection Service
- Web Portal Collection Service
- Shared Storage Service
Processing
- Extraction
    1. OCR vs PDF Service and Conversion
    2. Metric Extraction (Rule Based vs LLM Based)

- Validation
Output
- Queries
- Searches


Missing discussions
1. Security
2. Queries, searches and analyst interface
3. Testing strategy for the system