import streamlit as st
import requests
import plotly.graph_objects as go

API_KEY = "2585e7a98b5037d7c491d5b307cfc154"

st.set_page_config(page_title="날씨 API ", page_icon="🌤️")
st.title("🌤️ 세계 지역 날씨 시각화 프로그램")
st.write("지역 이름을 **한글 또는 영어**로 입력하세요.")

city = st.text_input("지역 이름 (예: 서울, 부산, Seoul)")

if st.button("날씨 조회"):
    if city == "":
        st.warning("지역 이름을 입력하세요.")
    else:
        geo_url = (
            "http://api.openweathermap.org/geo/1.0/direct"
            + "?q=" + city
            + "&limit=1"
            + "&appid=" + API_KEY
        )

        geo_response = requests.get(geo_url)

        if geo_response.status_code != 200 or len(geo_response.json()) == 0:
            st.error("지역을 찾을 수 없습니다.")
        else:
            geo_data = geo_response.json()[0]
            lat = geo_data["lat"]
            lon = geo_data["lon"]
            location_name = geo_data["name"]

            weather_url = (
                "https://api.openweathermap.org/data/2.5/weather"
                + "?lat=" + str(lat)
                + "&lon=" + str(lon)
                + "&appid=" + API_KEY
                + "&units=metric"
                + "&lang=kr"
            )

            weather_response = requests.get(weather_url)
            data = weather_response.json()

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            weather = data["weather"][0]["description"]


            st.success( location_name + " 현재 날씨")
            st.write("☁️ 날씨 상태: " + weather)
            st.write("💧 습도: " + str(humidity) + "%")
            st.metric("현재 온도", str(temp) + "°C")
            st.metric("체감 온도", str(feels_like) + "°C")


            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                x=["현재 온도", "체감 온도"],
                y=[temp, feels_like],
                 width=0.4
                )
            )   

            fig.update_layout(
                title=" 온도 비교 (°C)",
                yaxis_title="섭씨 온도 (°C)",
                xaxis_title="구분"
            )

            st.plotly_chart(fig)