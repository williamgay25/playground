# Requirements
Speed
5 to 10 seconds max
2 to 3 new funds per day

Current Data
~1000 previously analyzed fund
Document store in S3
Postgres Database of extracted metrics

Accuracy
False positives are more costly than false negatives
2 to 3 highly relevant comparables in the top 5 suggestions
Will search up to 10 to find a good match
Err on the side of precision over recall

# Architecture
Data Connectors
- PostgresSQL for structuredd
- S3 for documents
- Processing pipeline?

Matching Engine
- Calculate a similarity score between each funds information
- Background job to monitor and precompute additional information
- Maybe caching for frequently queried funds?

External API
- Handle authentication (forgot to talk about this last time)
- Coordinate the comparison flow
- Return standardized response


# Dataflow
1. Fund id comes in
2. Retrieve fund information
3. Compare with other funds
4. Return a list of 10 funds

# Fund Information
Investment Strategy
- Textual dsecription in the investment memorandum

Protfolio Construction & Risk
- Asset allocations
- Geographic Exposure
- Sector concentrations
- Leverage levels

Performance
- Return patterns
- Volatility metrics
- Correlation with indices
- Drawdowns

Note: Can define dataclasses for all of this information for the funds. Can create a fund comparison class that compares on each of these different areas.