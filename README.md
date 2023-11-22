# GrockStockBot

## Twitter API Client
A simple Python script to interact with the Twitter API and post tweets using Tweepy.

### Set up your environment variables:
export X_API_KEY=your_api_key
export X_API_SECRET=your_api_secret
export X_BEARER_TOKEN=your_bearer_token
export X_ACCESS_TOKEN=your_access_token
export X_ACCESS_TOKEN_SECRET=your_access_token_secret

Replace your_api_key, your_api_secret, your_bearer_token, your_access_token, and your_access_token_secret with your actual Twitter API credentials.

## Usage

### Run the script:
python main.py

This will authenticate with the Twitter API and post a test tweet.

## Notes
- Ensure that your Twitter API credentials are kept secret. Use environment variables to securely store sensitive information.
- This script uses Tweepy, a Python library for accessing the Twitter API. Check the Tweepy documentation for more details.
- Make sure to review the Twitter API documentation for any rate limits or restrictions that may apply to your use case.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
