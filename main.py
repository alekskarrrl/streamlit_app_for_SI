from datetime import datetime, date, time
import pandas as pd
import plotly.express as px
import requests
import streamlit as st


def main():
    # запрос списка активов
    url_asset = 'http://api.coincap.io/v2/assets'

    request_asset = requests.get(url_asset)
    response = request_asset.json()
    data = response['data']
    data_assets = {item['symbol']: item['id'] for item in data}

# Боковая панель
    with st.sidebar:
        # Выбор актива
        asset = st.selectbox("**Select an asset**", data_assets.keys())

        col1, col2 = st.sidebar.columns(2)

        # Выбор интервала дат
        with col1:
            input_start_date = st.date_input("**Date from**", value=datetime(2023, 1, 1), min_value=datetime(2010, 1, 1))

        with col2:
            input_end_date = st.date_input("**Date to**", value=datetime.today(), min_value=datetime(2010, 1, 1))

    interval = 'd1'
    asset_id = data_assets[asset]

    # Преобразование даты
    start_date = datetime.combine(input_start_date, datetime.min.time()) # добавила к введенной дате время 00H:00M:00S
    end_date = datetime.combine(input_end_date, datetime.max.time())  # добавила к введенной дате время 23H:59M:59S

    # Приведение к unix милисекундам
    unix_start_date_ms = datetime.timestamp(start_date) * 1000
    unix_end_date_ms = datetime.timestamp(end_date) * 1000

    # Запрос истории
    url_history = f'http://api.coincap.io/v2/assets/{asset_id}/history?interval={interval}&start={unix_start_date_ms}&end={unix_end_date_ms}'

    request_history = requests.get(url_history)
    resp = request_history.json()
    history = resp['data']
    df = pd.DataFrame([dict(priceUsd=item['priceUsd'], time=item['time'],
                            date=datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S.%f%z')) for item in history])
    # График
    fig = px.bar(df, y='priceUsd', x='date', log_y=True)
    fig.update_xaxes(title="TIME", title_font_size=25, title_font_color='black', showgrid=False)
    fig.update_yaxes(title="PRICE", title_font_size=25, title_font_color='black', showgrid=False)
    fig.update_layout(plot_bgcolor='#FFF9EC')

    st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()

