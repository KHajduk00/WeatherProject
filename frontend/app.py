import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Optional, List
import json

# Configuration
API_BASE_URL = "http://localhost:8000"  # Adjust this to your FastAPI server URL

# Page configuration
st.set_page_config(
    page_title="Weather Data Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class WeatherAPI:
    """Class to handle API interactions"""
    
    @staticmethod
    def check_health():
        try:
            response = requests.get(f"{API_BASE_URL}/health")
            return response.status_code == 200, response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return False, None
    
    @staticmethod
    def get_weather_data(city=None, country=None, start_date=None, end_date=None):
        try:
            params = {}
            if city:
                params['city'] = city
            if country:
                params['country'] = country
            if start_date:
                params['start_date'] = start_date.isoformat()
            if end_date:
                params['end_date'] = end_date.isoformat()
            
            response = requests.get(f"{API_BASE_URL}/api/v1/weather", params=params)
            return response.status_code == 200, response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return False, []
    
    @staticmethod
    def get_air_pollution_data(city=None, start_date=None, end_date=None):
        try:
            params = {}
            if city:
                params['city'] = city
            if start_date:
                params['start_date'] = start_date.isoformat()
            if end_date:
                params['end_date'] = end_date.isoformat()
            
            response = requests.get(f"{API_BASE_URL}/api/v1/air-pollution", params=params)
            return response.status_code == 200, response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return False, []
    
    @staticmethod
    def get_statistics(city=None, days=7):
        try:
            params = {'days': days}
            if city:
                params['city'] = city
            
            response = requests.get(f"{API_BASE_URL}/api/v1/statistics", params=params)
            return response.status_code == 200, response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return False, []
    
    @staticmethod
    def get_collector_status():
        try:
            response = requests.get(f"{API_BASE_URL}/api/v1/collector/status")
            return response.status_code == 200, response.json() if response.status_code == 200 else {}
        except requests.exceptions.RequestException:
            return False, {}
    
    @staticmethod
    def start_collector():
        try:
            response = requests.post(f"{API_BASE_URL}/api/v1/collector/start")
            return response.status_code == 200, response.json()
        except requests.exceptions.RequestException:
            return False, {"message": "Failed to connect to API"}
    
    @staticmethod
    def stop_collector():
        try:
            response = requests.post(f"{API_BASE_URL}/api/v1/collector/stop")
            return response.status_code == 200, response.json()
        except requests.exceptions.RequestException:
            return False, {"message": "Failed to connect to API"}

    @staticmethod
    def get_weather_pollution_correlation(city=None, days=7):
        try:
            params = {'days': days}
            if city:
                params['city'] = city
            
            response = requests.get(f"{API_BASE_URL}/api/v1/analytics/weather-pollution-correlation", params=params)
            return response.status_code == 200, response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return False, []
    
    @staticmethod
    def get_high_pollution_alerts(aqi_threshold=100, pm25_threshold=35.0, days=7):
        try:
            params = {
                'aqi_threshold': aqi_threshold,
                'pm25_threshold': pm25_threshold,
                'days': days
            }
            
            response = requests.get(f"{API_BASE_URL}/api/v1/analytics/high-pollution-alerts", params=params)
            return response.status_code == 200, response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return False, []
    
    @staticmethod
    def get_prediction_data(city=None, hours_back=168):
        try:
            params = {'hours_back': hours_back}
            if city:
                params['city'] = city
            
            response = requests.get(f"{API_BASE_URL}/api/v1/analytics/prediction-data-flexible", params=params)
            return response.status_code == 200, response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException:
            return False, []

def main():
    st.title("🌤️ Weather Data Dashboard")
    
    # Check API health
    health_ok, health_data = WeatherAPI.check_health()
    
    if not health_ok:
        st.error("⚠️ Cannot connect to the Weather API. Please ensure the backend server is running.")
        st.info(f"Expected API URL: {API_BASE_URL}")
        return
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Weather Data", "Air Pollution", "Statistics", "Analytics", "Data Collector"]
    )
    
    # Display API health status
    with st.sidebar.expander("API Status"):
        st.success("✅ API Connected")
        if health_data:
            st.json(health_data)
    
    # Route to different pages
    if page == "Dashboard":
        show_dashboard()
    elif page == "Weather Data":
        show_weather_data()
    elif page == "Air Pollution":
        show_air_pollution()
    elif page == "Statistics":
        show_statistics()
    elif page == "Analytics":
        show_analytics()
    elif page == "Data Collector":
        show_collector_control()

def show_dashboard():
    """Main dashboard with overview"""
    st.header("📊 Overview Dashboard")
    
    # Get recent statistics
    success, stats_data = WeatherAPI.get_statistics(days=7)
    
    if success and stats_data:
        # Create metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_temp = sum(stat['avg_temperature'] for stat in stats_data if stat['avg_temperature']) / len(stats_data)
            st.metric("Average Temperature", f"{avg_temp:.1f}°C")
        
        with col2:
            total_measurements = sum(stat['measurements_count'] for stat in stats_data)
            st.metric("Total Measurements", total_measurements)
        
        with col3:
            cities_count = len(stats_data)
            st.metric("Cities Monitored", cities_count)
        
        with col4:
            avg_aqi = sum(stat['avg_aqi'] for stat in stats_data if stat['avg_aqi']) / len([s for s in stats_data if s['avg_aqi']])
            st.metric("Average AQI", f"{avg_aqi:.0f}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Temperature by City")
            df_stats = pd.DataFrame(stats_data)
            fig = px.bar(df_stats, x='city', y='avg_temperature', 
                        title="Average Temperature by City",
                        labels={'avg_temperature': 'Temperature (°C)'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Air Quality Index by City")
            fig = px.bar(df_stats, x='city', y='avg_aqi',
                        title="Average AQI by City",
                        labels={'avg_aqi': 'AQI'})
            st.plotly_chart(fig, use_container_width=True)

def show_weather_data():
    """Weather data page with filtering options"""
    st.header("🌡️ Weather Data")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        city_filter = st.text_input("City (optional)")
    
    with col2:
        country_filter = st.text_input("Country (optional)")
    
    with col3:
        days_back = st.selectbox("Show data from last", [1, 3, 7, 14, 30], index=2)
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Fetch data
    success, weather_data = WeatherAPI.get_weather_data(
        city=city_filter if city_filter else None,
        country=country_filter if country_filter else None,
        start_date=start_date,
        end_date=end_date
    )
    
    if success and weather_data:
        df = pd.DataFrame(weather_data)
        df['measurement_timestamp'] = pd.to_datetime(df['measurement_timestamp'])
        
        st.subheader(f"📈 Weather Trends ({len(df)} records)")
        
        # Temperature chart
        fig = px.line(df, x='measurement_timestamp', y='temperature', 
                     color='city', title="Temperature Over Time",
                     labels={'temperature': 'Temperature (°C)'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='measurement_timestamp', y='humidity', 
                         color='city', title="Humidity Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(df, x='measurement_timestamp', y='wind_speed', 
                         color='city', title="Wind Speed Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("📋 Raw Data")
        st.dataframe(df.sort_values('measurement_timestamp', ascending=False))
        
    else:
        st.warning("No weather data available for the selected criteria.")

def show_air_pollution():
    """Air pollution data page"""
    st.header("🏭 Air Pollution Data")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        city_filter = st.text_input("City (optional)")
    
    with col2:
        days_back = st.selectbox("Show data from last", [1, 3, 7, 14, 30], index=2, key="air_days")
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Fetch data
    success, pollution_data = WeatherAPI.get_air_pollution_data(
        city=city_filter if city_filter else None,
        start_date=start_date,
        end_date=end_date
    )
    
    if success and pollution_data:
        df = pd.DataFrame(pollution_data)
        df['measurement_timestamp'] = pd.to_datetime(df['measurement_timestamp'])
        
        st.subheader(f"📈 Air Quality Trends ({len(df)} records)")
        
        # AQI chart
        fig = px.line(df, x='measurement_timestamp', y='aqi', 
                     color='city', title="Air Quality Index Over Time")
        st.plotly_chart(fig, use_container_width=True)
        
        # Pollutant charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='measurement_timestamp', y='pm2_5', 
                         color='city', title="PM2.5 Levels Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(df, x='measurement_timestamp', y='pm10', 
                         color='city', title="PM10 Levels Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        # Additional pollutants
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='measurement_timestamp', y='no2', 
                         color='city', title="NO2 Levels Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(df, x='measurement_timestamp', y='o3', 
                         color='city', title="O3 Levels Over Time")
            st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("📋 Raw Data")
        st.dataframe(df.sort_values('measurement_timestamp', ascending=False))
        
    else:
        st.warning("No air pollution data available for the selected criteria.")

def show_statistics():
    """Statistics page"""
    st.header("📊 Statistics")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        city_filter = st.text_input("City (optional)", key="stats_city")
    
    with col2:
        days_period = st.selectbox("Period (days)", [1, 3, 7, 14, 30], index=2, key="stats_days")
    
    # Fetch statistics
    success, stats_data = WeatherAPI.get_statistics(
        city=city_filter if city_filter else None,
        days=days_period
    )
    
    if success and stats_data:
        df = pd.DataFrame(stats_data)
        
        # Summary cards
        st.subheader("📈 Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Cities", len(df))
        
        with col2:
            total_measurements = df['measurements_count'].sum()
            st.metric("Total Measurements", total_measurements)
        
        with col3:
            avg_temp = df['avg_temperature'].mean()
            st.metric("Overall Avg Temperature", f"{avg_temp:.1f}°C")
        
        with col4:
            avg_aqi = df['avg_aqi'].mean()
            st.metric("Overall Avg AQI", f"{avg_aqi:.0f}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(df, x='avg_temperature', y='avg_aqi', 
                           size='measurements_count', hover_name='city',
                           title="Temperature vs Air Quality")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df, x='city', y='measurements_count',
                        title="Measurements Count by City")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed statistics table
        st.subheader("📋 Detailed Statistics")
        st.dataframe(df)
        
    else:
        st.warning("No statistics available for the selected criteria.")

def show_collector_control():
    """Data collector control page"""
    st.header("🔄 Data Collector Control")
    
    # Get collector status
    success, status_data = WeatherAPI.get_collector_status()
    
    if success:
        st.subheader("📊 Collector Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            is_running = status_data.get('is_running', False)
            status_color = "🟢" if is_running else "🔴"
            st.metric("Status", f"{status_color} {'Running' if is_running else 'Stopped'}")
        
        with col2:
            interval = status_data.get('collection_interval', 'N/A')
            st.metric("Collection Interval", f"{interval}s" if interval != 'N/A' else 'N/A')
        
        # Control buttons
        st.subheader("🎛️ Controls")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Start Collector", type="primary"):
                success, response = WeatherAPI.start_collector()
                if success:
                    st.success(response.get('message', 'Collector started'))
                    st.rerun()
                else:
                    st.error(response.get('message', 'Failed to start collector'))
        
        with col2:
            if st.button("⏹️ Stop Collector", type="secondary"):
                success, response = WeatherAPI.stop_collector()
                if success:
                    st.success(response.get('message', 'Collector stopped'))
                    st.rerun()
                else:
                    st.error(response.get('message', 'Failed to stop collector'))
        
        with col3:
            if st.button("🔄 Refresh Status"):
                st.rerun()
        
        # Display full status
        st.subheader("📋 Full Status")
        st.json(status_data)
        
    else:
        st.error("Failed to retrieve collector status")

def show_analytics():
    """Advanced analytics page for research questions"""
    st.header("🔬 Advanced Analytics")
    
    # Sub-navigation for different analytics
    analytics_tab = st.selectbox(
        "Choose Analysis Type",
        ["Weather-Pollution Correlation", "Smart Alerts Analysis", "AQI Prediction Analysis"]
    )
    
    if analytics_tab == "Weather-Pollution Correlation":
        show_weather_pollution_correlation()
    elif analytics_tab == "Smart Alerts Analysis":
        show_smart_alerts_analysis()
    elif analytics_tab == "AQI Prediction Analysis":
        show_aqi_prediction_analysis()

def show_weather_pollution_correlation():
    """Analysis of weather conditions vs pollution levels"""
    st.subheader("🌡️ Weather Conditions vs Pollution Levels")
    st.info("**Research Question**: What weather conditions are most associated with elevated PM2.5 or NO₂ levels?")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        city_filter = st.text_input("City (optional)", key="corr_city")
    with col2:
        days_back = st.selectbox("Analysis Period (days)", [7, 14, 30, 60, 90], index=2, key="corr_days")
    
    # Fetch correlation data
    success, corr_data = WeatherAPI.get_weather_pollution_correlation(
        city=city_filter if city_filter else None,
        days=days_back
    )
    
    if success and corr_data:
        df = pd.DataFrame(corr_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create pollution level categories
        df['pm25_level'] = pd.cut(df['pm2_5'], 
                                 bins=[0, 12, 35, 55, 150, float('inf')], 
                                 labels=['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Very Unhealthy'])
        df['no2_level'] = pd.cut(df['no2'], 
                                bins=[0, 53, 100, 360, 649, float('inf')], 
                                labels=['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Very Unhealthy'])
        
        # Weather condition categories
        df['humidity_category'] = pd.cut(df['humidity'], 
                                       bins=[0, 40, 60, 80, 100], 
                                       labels=['Low', 'Moderate', 'High', 'Very High'])
        df['wind_category'] = pd.cut(df['wind_speed'], 
                                   bins=[0, 2, 5, 10, float('inf')], 
                                   labels=['Calm', 'Light', 'Moderate', 'Strong'])
        
        st.subheader("📊 Key Insights")
        
        # Correlation matrix
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Correlation with PM2.5:**")
            corr_pm25 = df[['temperature', 'humidity', 'pressure', 'wind_speed', 'pm2_5']].corr()['pm2_5'].sort_values(key=abs, ascending=False)
            st.dataframe(corr_pm25.drop('pm2_5').to_frame('Correlation'))
            
        with col2:
            st.write("**Correlation with NO₂:**")
            corr_no2 = df[['temperature', 'humidity', 'pressure', 'wind_speed', 'no2']].corr()['no2'].sort_values(key=abs, ascending=False)
            st.dataframe(corr_no2.drop('no2').to_frame('Correlation'))
        
        # Scatter plots for key relationships
        st.subheader("🔗 Weather-Pollution Relationships")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(df, x='humidity', y='pm2_5', color='wind_category',
                           title="PM2.5 vs Humidity (colored by Wind Speed)",
                           labels={'humidity': 'Humidity (%)', 'pm2_5': 'PM2.5 (μg/m³)'})
            fig.add_hline(y=35, line_dash="dash", line_color="red", 
                         annotation_text="Unhealthy for Sensitive Groups")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(df, x='wind_speed', y='no2', color='humidity_category',
                           title="NO₂ vs Wind Speed (colored by Humidity)",
                           labels={'wind_speed': 'Wind Speed (m/s)', 'no2': 'NO₂ (μg/m³)'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Box plots showing distribution
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.box(df, x='humidity_category', y='pm2_5',
                        title="PM2.5 Distribution by Humidity Category")
            fig.add_hline(y=35, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.box(df, x='wind_category', y='no2',
                        title="NO₂ Distribution by Wind Speed Category")
            st.plotly_chart(fig, use_container_width=True)
        
        # Heatmap of average pollution by weather conditions
        st.subheader("🗺️ Pollution Heatmap by Weather Conditions")
        
        pivot_data = df.groupby(['humidity_category', 'wind_category'])['pm2_5'].mean().unstack()
        fig = px.imshow(pivot_data, 
                       title="Average PM2.5 by Humidity and Wind Speed Categories",
                       labels=dict(x="Wind Category", y="Humidity Category", color="PM2.5 (μg/m³)"))
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("No correlation data available for the selected criteria.")

def show_smart_alerts_analysis():
    """Analysis for smart pollution alerts"""
    st.subheader("🚨 Smart Pollution Alert Analysis")
    st.info("**Research Question**: How can real-time weather and air quality data trigger smart alerts under specific conditions?")
    
    # Alert thresholds
    col1, col2, col3 = st.columns(3)
    with col1:
        aqi_threshold = st.slider("AQI Alert Threshold", 50, 300, 100)
    with col2:
        pm25_threshold = st.slider("PM2.5 Alert Threshold (μg/m³)", 10.0, 100.0, 35.0)
    with col3:
        days_back = st.selectbox("Analysis Period", [7, 14, 30, 60], index=2, key="alert_days")
    
    # Fetch alert data
    success, alert_data = WeatherAPI.get_high_pollution_alerts(
        aqi_threshold=aqi_threshold,
        pm25_threshold=pm25_threshold,
        days=days_back
    )
    
    if success and alert_data:
        df = pd.DataFrame(alert_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        st.subheader(f"🔔 High Pollution Events ({len(df)} events)")
        
        # Alert frequency by city
        col1, col2 = st.columns(2)
        
        with col1:
            city_counts = df['city'].value_counts()
            fig = px.bar(x=city_counts.index, y=city_counts.values,
                        title="High Pollution Events by City",
                        labels={'x': 'City', 'y': 'Number of Events'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Weather conditions during high pollution events
            weather_counts = df['weather_description'].value_counts().head(10)
            fig = px.pie(values=weather_counts.values, names=weather_counts.index,
                        title="Weather Conditions During High Pollution Events")
            st.plotly_chart(fig, use_container_width=True)
        
        # Time series of events
        st.subheader("📈 High Pollution Events Timeline")
        fig = px.scatter(df, x='timestamp', y='aqi', size='pm2_5', color='city',
                        title="High Pollution Events Over Time",
                        labels={'aqi': 'Air Quality Index', 'pm2_5': 'PM2.5 (μg/m³)'})
        fig.add_hline(y=aqi_threshold, line_dash="dash", line_color="red",
                     annotation_text=f"AQI Alert Threshold: {aqi_threshold}")
        st.plotly_chart(fig, use_container_width=True)
        
        # Weather patterns during alerts
        st.subheader("🌡️ Weather Patterns During High Pollution Events")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(df, x='humidity', nbins=20,
                             title="Humidity Distribution During High Pollution Events",
                             labels={'humidity': 'Humidity (%)'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(df, x='wind_speed', nbins=20,
                             title="Wind Speed Distribution During High Pollution Events",
                             labels={'wind_speed': 'Wind Speed (m/s)'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Smart alert criteria summary
        st.subheader("💡 Smart Alert Criteria Recommendations")
        
        avg_humidity = df['humidity'].mean()
        avg_wind = df['wind_speed'].mean()
        avg_temp = df['temperature'].mean()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Avg Humidity During Alerts", f"{avg_humidity:.1f}%")
        with col2:
            st.metric("Avg Wind Speed During Alerts", f"{avg_wind:.1f} m/s")
        with col3:
            st.metric("Avg Temperature During Alerts", f"{avg_temp:.1f}°C")
        
        # Alert recommendations
        st.info(f"""
        **Recommended Smart Alert Criteria:**
        - AQI > {aqi_threshold} OR PM2.5 > {pm25_threshold} μg/m³
        - Additional risk factors: Humidity > {avg_humidity:.0f}% AND Wind Speed < {avg_wind:.1f} m/s
        - Weather conditions with highest risk: {df['weather_description'].mode().iloc[0] if not df.empty else 'N/A'}
        """)
        
    else:
        st.warning("No high pollution events found for the selected criteria.")

def show_aqi_prediction_analysis():
    """Analysis for AQI prediction modeling"""
    st.subheader("🔮 AQI Prediction Analysis")
    st.info("**Research Question**: Can patterns in weather and pollution data be used to forecast AQI levels?")
    
    # Add data availability check
    st.subheader("📊 Data Availability Check")
    
    # Check basic data availability with recent date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # Check last 7 days
    
    success_weather, weather_data = WeatherAPI.get_weather_data(
        start_date=start_date, 
        end_date=end_date
    )
    success_pollution, pollution_data = WeatherAPI.get_air_pollution_data(
        start_date=start_date, 
        end_date=end_date
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        weather_count = len(weather_data) if success_weather and weather_data else 0
        st.metric("Weather Records", weather_count)
    with col2:
        pollution_count = len(pollution_data) if success_pollution and pollution_data else 0
        st.metric("Pollution Records", pollution_count)
    with col3:
        if weather_count > 0 and pollution_count > 0:
            # Calculate data span using weather data timestamps
            try:
                timestamps = []
                for d in weather_data:
                    if isinstance(d['measurement_timestamp'], str):
                        # Handle string timestamps
                        timestamp_str = d['measurement_timestamp'].replace('Z', '+00:00')
                        timestamps.append(datetime.fromisoformat(timestamp_str))
                    else:
                        timestamps.append(d['measurement_timestamp'])
                
                if timestamps:
                    data_span = (max(timestamps) - min(timestamps)).total_seconds() / 3600  # hours
                    st.metric("Data Span (hours)", f"{data_span:.1f}")
                else:
                    st.metric("Data Span (hours)", "0")
            except Exception as e:
                st.metric("Data Span (hours)", "Error calculating")
        else:
            st.metric("Data Span (hours)", "0")
    
    # Show recommendation based on data availability
    if weather_count == 0 or pollution_count == 0:
        st.warning("⚠️ No weather or pollution data found. Please start the data collector and wait for data to be collected.")
        st.info("💡 Go to the 'Data Collector' page to start data collection.")
        return
    elif weather_count < 24 or pollution_count < 24:
        st.warning("⚠️ Insufficient data for prediction analysis. You need at least 24+ hours of continuous data.")
        st.info(f"💡 Current data: {weather_count} weather records, {pollution_count} pollution records. Please wait for more data to be collected.")
        return
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        city_filter = st.text_input("City (optional)", key="pred_city")
    with col2:
        hours_back = st.selectbox("Data History (hours)", [72, 168, 336, 720], index=1, key="pred_hours")
    
    # Fetch prediction data
    success, pred_data = WeatherAPI.get_prediction_data(
        city=city_filter if city_filter else None,
        hours_back=hours_back
    )
    
    if success and pred_data:
        df = pd.DataFrame(pred_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter for records that have some prediction data
        df_with_predictions = df.dropna(subset=['future_aqi_next'])

        if len(df_with_predictions) > 0:
            st.subheader(f"📊 Prediction Analysis ({len(df_with_predictions)} usable data points)")

            # Show data collection pattern info
            st.info(f"""
            **Data Collection Pattern Detected:**
            - Total records: {len(df)}
            - Records with next-step predictions: {len(df_with_predictions)}
            - Records with 24h approximations: {len(df.dropna(subset=['future_aqi_24h_approx']))}

            Note: Prediction accuracy depends on regular data collection intervals.
            """)
            
            # Feature correlation analysis
            features = ['temperature', 'humidity', 'pressure', 'wind_speed', 'aqi', 'pm2_5', 'no2']
            
            st.subheader("🎯 Next-Step AQI Prediction Analysis")

            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Correlations with Next AQI Value:**")
                corr_next = df_with_predictions[features + ['future_aqi_next']].corr()['future_aqi_next'].drop('future_aqi_next').sort_values(key=abs, ascending=False)
                st.dataframe(corr_next.to_frame('Correlation'))

            with col2:
                # Simple prediction accuracy
                fig = px.scatter(df_with_predictions, x='aqi', y='future_aqi_next',
                               color='city', title="Current AQI vs Next AQI Reading",
                               labels={'aqi': 'Current AQI', 'future_aqi_next': 'Next AQI'})
                # Add perfect prediction line
                min_val = min(df_with_predictions['aqi'].min(), df_with_predictions['future_aqi_next'].min())
                max_val = max(df_with_predictions['aqi'].max(), df_with_predictions['future_aqi_next'].max())
                fig.add_shape(type="line", x0=min_val, y0=min_val, x1=max_val, y1=max_val,
                             line=dict(color="red", dash="dash"))
                st.plotly_chart(fig, use_container_width=True)
            
            # Time series prediction visualization
            st.subheader("📈 Time Series Prediction Patterns")
            
            # Select a subset for visualization
            df_sample = df_with_predictions.head(100) if len(df_with_predictions) > 100 else df_with_predictions

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_sample['timestamp'], y=df_sample['aqi'],
                                   mode='lines+markers', name='Current AQI'))
            fig.add_trace(go.Scatter(x=df_sample['timestamp'], y=df_sample['future_aqi_next'],
                                   mode='lines+markers', name='Next AQI Reading'))

            # Add 24h approximation if available
            if 'future_aqi_24h_approx' in df_sample.columns:
                df_with_24h = df_sample.dropna(subset=['future_aqi_24h_approx'])
                if len(df_with_24h) > 0:
                    fig.add_trace(go.Scatter(x=df_with_24h['timestamp'], y=df_with_24h['future_aqi_24h_approx'],
                                           mode='lines+markers', name='24h Approx AQI'))

            fig.update_layout(title="AQI Time Series - Current vs Predicted Values",
                            xaxis_title="Time", yaxis_title="AQI")
            st.plotly_chart(fig, use_container_width=True)
            
            # Weather influence on prediction accuracy
            st.subheader("🌤️ Weather Influence on Prediction Accuracy")
            
            # Calculate prediction errors
            df_with_predictions['error_next'] = abs(df_with_predictions['future_aqi_next'] - df_with_predictions['aqi'])

            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(df_with_predictions, x='wind_speed', y='error_next', color='humidity',
                               title="Next-Step Prediction Error vs Wind Speed",
                               labels={'wind_speed': 'Wind Speed (m/s)', 'error_next': 'Next-Step Prediction Error'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.scatter(df_with_predictions, x='humidity', y='error_next', color='temperature',
                               title="Next-Step Prediction Error vs Humidity",
                               labels={'humidity': 'Humidity (%)', 'error_next': 'Next-Step Prediction Error'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Model performance metrics
            st.subheader("📏 Simple Prediction Model Performance")
            
            from sklearn.metrics import mean_absolute_error, mean_squared_error
            import numpy as np
            
            mae_next = mean_absolute_error(df_with_predictions['aqi'], df_with_predictions['future_aqi_next'])
            rmse_next = np.sqrt(mean_squared_error(df_with_predictions['aqi'], df_with_predictions['future_aqi_next']))

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Next-Step MAE", f"{mae_next:.2f}")
            with col2:
                st.metric("Next-Step RMSE", f"{rmse_next:.2f}")

            # Add 24h approximation metrics if available
            if 'future_aqi_24h_approx' in df.columns:
                df_with_24h = df.dropna(subset=['future_aqi_24h_approx'])
                if len(df_with_24h) > 0:
                    mae_24h = mean_absolute_error(df_with_24h['aqi'], df_with_24h['future_aqi_24h_approx'])
                    rmse_24h = np.sqrt(mean_squared_error(df_with_24h['aqi'], df_with_24h['future_aqi_24h_approx']))

                    with col3:
                        st.metric("24h Approx MAE", f"{mae_24h:.2f}")
                    with col4:
                        st.metric("24h Approx RMSE", f"{rmse_24h:.2f}")

            # Prediction insights
            st.info(f"""
            **Key Insights for AQI Prediction:**
            - Next-step predictions show MAE of {mae_next:.1f} AQI units
            - Best predictive features: {corr_next.head(3).index.tolist()}
            - Weather conditions significantly impact prediction accuracy
            - Consider using ensemble methods with weather pattern classification
            - Prediction quality improves with regular, continuous data collection
            """)
            
        else:
            st.warning("No usable prediction data available. This usually means:")
            st.markdown("""
            - Data collection gaps are too large
            - Need more continuous data collection
            - Consider running the collector continuously for better prediction analysis
            """)
    else:
        st.warning("No prediction data available for the selected criteria.")

if __name__ == "__main__":
    main()
