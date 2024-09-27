import streamlit as st
import plotly.express as px
import plotly.graph_objects as go  # Added for candlestick chart
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

# Page setup
st.set_page_config(page_title="Pakistan Stock Exchange Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# Add some space before the title
st.markdown("<br>" * 5, unsafe_allow_html=True)  # Adds 5 line breaks for spacing
st.title(":chart_with_upwards_trend: Pakistan Stock Exchange Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


# Read stock symbols from the CSV file
try:
    stock_symbols_df = pd.read_csv("PSX.csv")
    stock_symbols = stock_symbols_df['Data'].tolist()
except FileNotFoundError:
    st.error("Error: Stock symbols CSV file not found.")
    st.stop()

st.sidebar.title("Navigation")
option = st.sidebar.radio("", ("Stock Data", "Stock Price", "Candlestick Chart"))

if option == "Stock Data":
    st.subheader("Stock Data")
    st.write(stock_symbols_df)

elif option == "Stock Price":
    selected_stock = st.selectbox("Select Stock", stock_symbols)

    # Function to fetch stock data
    def fetch_stock_data(stock_symbol):
        try:
            csv_filename = f"{stock_symbol}.csv"
            df = pd.read_csv(csv_filename)
            return df
        except FileNotFoundError:
            st.error(f"Error: CSV file '{csv_filename}' not found.")
            return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    # Fetch stock data based on selected stock
    stock_df = fetch_stock_data(selected_stock)

    if stock_df is not None:
        # Convert 'Date' column to datetime
        stock_df['Date'] = pd.to_datetime(stock_df['Date'])

        # Sidebar options
        start_date = st.sidebar.date_input("Start Date", stock_df['Date'].min().date())
        end_date = st.sidebar.date_input("End Date", stock_df['Date'].max().date())

        # Filter data based on selected date range
        filtered_df = stock_df[(stock_df['Date'] >= pd.to_datetime(start_date)) & (stock_df['Date'] <= pd.to_datetime(end_date))]

        # Main dashboard content
        st.subheader(f"Stock Data for {selected_stock}")
        st.write(filtered_df)

        # Plot selection section
        st.sidebar.subheader("Select Plot Type")
        plot_type = st.sidebar.selectbox("Plot Type", ["Line Chart", "Box Plot", "Bar Chart", "Price Over Time", "Price and Volume Over Time", "30-Day Rolling Mean", "High and Low Over Time"])

        # Plotting the selected plot type
        if plot_type == "Line Chart":
            st.subheader("Stock Price")
            fig = px.line(filtered_df, x='Date', y='Close', title=f"{selected_stock} Stock Price", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "Box Plot":
            st.subheader("Box Plot")
            fig = px.box(filtered_df, x='Date', y='Close', title=f"{selected_stock} Box Plot", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "Bar Chart":
            st.subheader("Bar Chart")
            fig = px.bar(filtered_df, x='Date', y='Close', title=f"{selected_stock} Bar Chart", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "Price Over Time":
            st.subheader("Price Over Time")
            fig = px.line(filtered_df, x='Date', y='Close', title=f"{selected_stock} Price Over Time", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "Price and Volume Over Time":
            st.subheader("Price and Volume Over Time")
            fig = px.line(filtered_df, x='Date', y=['Close', 'Volume'], title=f"{selected_stock} Price and Volume Over Time", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "30-Day Rolling Mean":
            st.subheader("30-Day Rolling Mean")
            filtered_df['Rolling_Mean'] = filtered_df['Close'].rolling(window=30).mean()
            fig = px.line(filtered_df, x='Date', y='Rolling_Mean', title=f"{selected_stock} 30-Day Rolling Mean", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        elif plot_type == "High and Low Over Time":
            st.subheader("High and Low Over Time")
            fig = px.line(filtered_df, x='Date', y=['High', 'Low'], title=f"{selected_stock} High and Low Over Time", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

elif option == "Candlestick Chart":
    st.subheader("Candlestick Chart")
    selected_stock = st.selectbox("Select Stock", stock_symbols)

    # Function to fetch stock data
    def fetch_stock_data(stock_symbol):
        try:
            csv_filename = f"{stock_symbol}.csv"
            df = pd.read_csv(csv_filename)
            return df
        except FileNotFoundError:
            st.error(f"Error: CSV file '{csv_filename}' not found.")
            return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None

    # Fetch stock data based on selected stock
    stock_df = fetch_stock_data(selected_stock)

    if stock_df is not None:
        # Convert 'Date' column to datetime
        stock_df['Date'] = pd.to_datetime(stock_df['Date'])

        # Creating candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=stock_df['Date'],
                                              open=stock_df['Open'],
                                              high=stock_df['High'],
                                              low=stock_df['Low'],
                                              close=stock_df['Close'])])

        # Update layout to add range slider and range selector
        fig.update_layout(title=f'{selected_stock} Candlestick Chart',
                          xaxis_title='Date',
                          yaxis_title='Price',
                          template='plotly_dark',
                          xaxis_rangeslider_visible=True,  # Enable range slider
                          xaxis=dict(type='date'),  # Set x-axis type to date
                          )

        # Display the candlestick chart
        st.plotly_chart(fig, use_container_width=True)