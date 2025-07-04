from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import requests
from dotenv import load_dotenv
import os
import asyncio
import chainlit as cl


set_tracing_disabled(disabled=True)
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


@function_tool
def fetch_crypto_data(symbol: str):
    """
    Fetch coin id from CoinLore ticker API using the symbol (e.g., BTC for Bitcoin),
    and fetch the required crypto data using that id.
    """
    try:
        # Get list of coins
        ticker_response = requests.get("https://api.coinlore.net/api/tickers/")
        if ticker_response.status_code != 200:
            return f"Failed to fetch ticker data. Status code: {ticker_response.status_code}"
        
        json_response = ticker_response.json()
        ticker_data = json_response.get("data", [])
        
        # Find the coin by symbol
        result = [coin for coin in ticker_data if symbol.upper() == coin["symbol"].upper()]
        if not result:
            return f"No coin found with symbol: {symbol}"

        coin = result[0]
        coin_id = coin["id"]
        
        # Get specific coin data
        specific_coin_data = requests.get(f"https://api.coinlore.net/api/ticker/?id={coin_id}")
        if specific_coin_data.status_code != 200:
            return f"Failed to fetch specific coin data. Status code: {specific_coin_data.status_code}"
        
        coin_json = specific_coin_data.json()
        if not coin_json:
            return f"No data returned for coin ID: {coin_id}"
        
        return coin_json[0]  # this contains all coin info

    except Exception as e:
        return f"An error occurred while fetching data: {str(e)}"

        
    



crypto_data_agent = Agent(
    name="CryptoDataAgent",
    instructions="You are a crypto agent, which fetches crypto data using the tools available. The tool will give you every available information about the coin, extract the one you need for example, 'price in usd'",
    model= OpenAIChatCompletionsModel("gemini-2.0-flash", openai_client=external_client),
    tools=[fetch_crypto_data]
)





@cl.on_chat_start
async def on_start():
    await cl.Message(content="👋 Hello! I'm your Crypto Data Agent. I can provide you with real-time cryptocurrency prices and insights. Just ask me about any coin, like 'What is the price of BTC?'").send()

        
        
        
@cl.on_message
async def on_message(message: cl.Message):
        result = await Runner.run(crypto_data_agent, message.content)
        await cl.Message(content=result.final_output).send()