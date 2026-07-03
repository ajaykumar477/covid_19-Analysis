import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load and preprocess data
df = pd.read_csv("state_wise_daily.csv")
df['parsed_date'] = pd.to_datetime(df['Date_YMD'], format='%d-%m-%Y')

# Sort chronologically
df = df.sort_values(by='parsed_date')

min_date = df['parsed_date'].min()
max_date = df['parsed_date'].max()

# State Mapping
STATE_MAP = {
    'MH': 'Maharashtra',
    'UP': 'Uttar Pradesh',
    'KA': 'Karnataka',
    'KL': 'Kerala',
    'TN': 'Tamil Nadu',
    'GJ': 'Gujarat',
    'TG': 'Telangana',
    'RJ': 'Rajasthan',
    'MP': 'Madhya Pradesh',
    'WB': 'West Bengal',
    'OR': 'Odisha',
    'HR': 'Haryana',
    'PB': 'Punjab',
    'JK': 'Jammu & Kashmir',
    'JH': 'Jharkhand',
    'GA': 'Goa',
    'HP': 'Himachal Pradesh',
    'UT': 'Uttarakhand',
    'AS': 'Assam',
    'AP': 'Andhra Pradesh',
    'BR': 'Bihar',
    'CT': 'Chhattisgarh',
    'DL': 'Delhi',
    'LA': 'Ladakh',
    'LD': 'Lakshadweep',
    'MN': 'Manipur',
    'ML': 'Meghalaya',
    'MZ': 'Mizoram',
    'NL': 'Nagaland',
    'PY': 'Puducherry',
    'SK': 'Sikkim',
    'TR': 'Tripura',
    'UN': 'Unassigned'
}

# Clean STATE_MAP to only include codes that are columns in df
STATE_MAP = {code: name for code, name in STATE_MAP.items() if code in df.columns}

# Styles
BODY_STYLE = {
    'background-color': '#0f172a',
    'font-family': 'Inter, system-ui, -apple-system, sans-serif',
    'min-height': '100vh',
    'color': '#f8fafc',
    'padding': '30px 15px',
}

HEADER_STYLE = {
    'color': '#f8fafc',
    'font-weight': '800',
    'margin-bottom': '10px',
    'letter-spacing': '-0.025em',
}

CARD_STYLE = {
    'background-color': '#1e293b',
    'border': '1px solid rgba(255,255,255,0.06)',
    'border-radius': '16px',
    'padding': '24px',
    'color': '#f8fafc',
    'box-shadow': '0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -4px rgba(0, 0, 0, 0.3)',
}

LABEL_STYLE = {
    'color': '#94a3b8',
    'font-size': '13px',
    'font-weight': '600',
    'text-transform': 'uppercase',
    'letter-spacing': '0.05em',
    'margin-bottom': '6px',
}

external_stylesheet = [
    {
        'href': "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        'rel': "stylesheet",
        'integrity': "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        'crossorigin': "anonymous"
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheet)

app.layout = html.Div(style=BODY_STYLE, children=[
    html.Div(className='container-fluid px-4', children=[
        # Title Banner
        html.Div(className='row mb-4 align-items-center', children=[
            html.Div(className='col', children=[
                html.H1('COVID-19 India Analytics Dashboard', style=HEADER_STYLE, className='text-start mb-1'),
                html.P('Interactive dashboard visualizing daily metrics, zoning footprints, and regional resources.', 
                       style={'color': '#94a3b8', 'font-size': '15px', 'margin-bottom': '0'}),
            ]),
        ]),
        
        # Interactive Controls Toolbar
        html.Div(className='row g-4 mb-4 p-4 align-items-end', 
                 style={'background-color': '#1e293b', 'border-radius': '16px', 'border': '1px solid rgba(255,255,255,0.06)'}, children=[
            # State Selector
            html.Div(className='col-12 col-md-6 col-lg-5', children=[
                html.Label('Select State / Territory', style=LABEL_STYLE),
                dcc.Dropdown(
                    id='state-selector',
                    options=[{'label': 'All India', 'value': 'All'}] + [
                        {'label': name, 'value': code} for code, name in sorted(STATE_MAP.items(), key=lambda x: x[1])
                    ],
                    value='All',
                    clearable=False,
                )
            ]),
            
            # Datepicker range
            html.Div(className='col-12 col-md-6 col-lg-5', children=[
                html.Label('Date Range Selector', style=LABEL_STYLE),
                html.Div(children=[
                    dcc.DatePickerRange(
                        id='date-picker',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        start_date=min_date,
                        end_date=max_date,
                        display_format='DD-MM-YYYY',
                    )
                ])
            ]),
        ]),
        
        # KPI Metric Cards
        html.Div(className='row g-4 mb-4', children=[
            # Confirmed
            html.Div(className='col-12 col-sm-6 col-lg-3', children=[
                html.Div(style=CARD_STYLE, children=[
                    html.H6('TOTAL CONFIRMED', style=LABEL_STYLE),
                    html.H2(id='total-confirmed-value', style={'color': '#f43f5e', 'font-weight': '800', 'margin': '10px 0 0 0'}),
                ])
            ]),
            # Active
            html.Div(className='col-12 col-sm-6 col-lg-3', children=[
                html.Div(style=CARD_STYLE, children=[
                    html.H6('ACTIVE CASES', style=LABEL_STYLE),
                    html.H2(id='active-cases-value', style={'color': '#0ea5e9', 'font-weight': '800', 'margin': '10px 0 0 0'}),
                ])
            ]),
            # Recovered
            html.Div(className='col-12 col-sm-6 col-lg-3', children=[
                html.Div(style=CARD_STYLE, children=[
                    html.H6('RECOVERED CASES', style=LABEL_STYLE),
                    html.H2(id='recovered-cases-value', style={'color': '#10b981', 'font-weight': '800', 'margin': '10px 0 0 0'}),
                ])
            ]),
            # Deaths
            html.Div(className='col-12 col-sm-6 col-lg-3', children=[
                html.Div(style=CARD_STYLE, children=[
                    html.H6('TOTAL DECEASED', style=LABEL_STYLE),
                    html.H2(id='deceased-value', style={'color': '#94a3b8', 'font-weight': '800', 'margin': '10px 0 0 0'}),
                ])
            ]),
        ]),
        
        # Charts Row 1: Line Chart & Donut Chart
        html.Div(className='row g-4 mb-4', children=[
            # Daily Trend Chart
            html.Div(className='col-12 col-lg-8', children=[
                html.Div(style=CARD_STYLE, children=[
                    dcc.Graph(id='trend-chart', config={'displayModeBar': False})
                ])
            ]),
            # Zone distribution Chart
            html.Div(className='col-12 col-lg-4', children=[
                html.Div(style=CARD_STYLE, children=[
                    dcc.Graph(id='zone-chart', config={'displayModeBar': False})
                ])
            ]),
        ]),
        
        # Charts Row 2: Resource Allocation & Comparison Chart
        html.Div(className='row g-4', children=[
            # Resource Allocation
            html.Div(className='col-12 col-lg-6', children=[
                html.Div(style=CARD_STYLE, children=[
                    dcc.Graph(id='resource-chart', config={'displayModeBar': False})
                ])
            ]),
            # Comparison Chart
            html.Div(className='col-12 col-lg-6', children=[
                html.Div(style=CARD_STYLE, children=[
                    html.Div(className='d-flex align-items-center justify-content-between mb-3', children=[
                        html.H5('State Standings & Insights', style={'color': '#f8fafc', 'margin': '0', 'font-weight': '600', 'font-size': '17px'}),
                        dcc.Dropdown(
                            id='comparison-metric',
                            options=[
                                {'label': 'Confirmed', 'value': 'Confirmed'},
                                {'label': 'Recovered', 'value': 'Recovered'},
                                {'label': 'Deceased', 'value': 'Deceased'}
                            ],
                            value='Confirmed',
                            clearable=False,
                            style={'width': '150px'}
                        )
                    ]),
                    dcc.Graph(id='comparison-chart', config={'displayModeBar': False})
                ])
            ]),
        ])
    ])
])

def apply_dark_theme(fig, title_text):
    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(size=16, family="Inter, sans-serif", color="#f8fafc", weight="bold"),
            x=0.02,
            y=0.96
        ),
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font=dict(family="Inter, sans-serif", color="#f8fafc"),
        margin=dict(t=70, r=20, l=40, b=40),
        xaxis=dict(
            gridcolor='#334155',
            showgrid=True,
            linecolor='#475569',
            tickfont=dict(color='#94a3b8'),
            title_font=dict(color='#94a3b8')
        ),
        yaxis=dict(
            gridcolor='#334155',
            showgrid=True,
            linecolor='#475569',
            tickfont=dict(color='#94a3b8'),
            title_font=dict(color='#94a3b8')
        )
    )
    return fig

# Callbacks
@app.callback(
    [Output('total-confirmed-value', 'children'),
     Output('active-cases-value', 'children'),
     Output('recovered-cases-value', 'children'),
     Output('deceased-value', 'children')],
    [Input('state-selector', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_kpis(state, start_date, end_date):
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    filtered = df[(df['parsed_date'] >= start_dt) & (df['parsed_date'] <= end_dt)]
    col = 'Total' if state == 'All' else state
    
    confirmed = filtered[filtered['Status'] == 'Confirmed'][col].sum()
    recovered = filtered[filtered['Status'] == 'Recovered'][col].sum()
    deceased = filtered[filtered['Status'] == 'Deceased'][col].sum()
    active = confirmed - recovered - deceased
    
    return f"{confirmed:,}", f"{active:,}", f"{recovered:,}", f"{deceased:,}"

@app.callback(
    Output('trend-chart', 'figure'),
    [Input('state-selector', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_trend_chart(state, start_date, end_date):
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    filtered = df[(df['parsed_date'] >= start_dt) & (df['parsed_date'] <= end_dt)]
    col = 'Total' if state == 'All' else state
    
    conf_data = filtered[filtered['Status'] == 'Confirmed']
    rec_data = filtered[filtered['Status'] == 'Recovered']
    dec_data = filtered[filtered['Status'] == 'Deceased']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=conf_data['parsed_date'],
        y=conf_data[col],
        name='Confirmed',
        mode='lines',
        line=dict(color='#f43f5e', width=3),
        hovertemplate='Date: %{x|%d %b %Y}<br>Cases: %{y:,}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=rec_data['parsed_date'],
        y=rec_data[col],
        name='Recovered',
        mode='lines',
        line=dict(color='#10b981', width=3),
        hovertemplate='Date: %{x|%d %b %Y}<br>Cases: %{y:,}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=dec_data['parsed_date'],
        y=dec_data[col],
        name='Deceased',
        mode='lines',
        line=dict(color='#64748b', width=2),
        hovertemplate='Date: %{x|%d %b %Y}<br>Cases: %{y:,}<extra></extra>'
    ))
    
    title_suffix = "All India" if state == 'All' else STATE_MAP.get(state, state)
    fig = apply_dark_theme(fig, f"Daily Timeline Trends ({title_suffix})")
    fig.update_layout(legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return fig

@app.callback(
    Output('zone-chart', 'figure'),
    [Input('state-selector', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_zone_chart(state, start_date, end_date):
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    filtered = df[(df['parsed_date'] >= start_dt) & (df['parsed_date'] <= end_dt)]
    
    if state != 'All':
        state_full_name = STATE_MAP.get(state)
        filtered = filtered[filtered['State'] == state_full_name]
        
    zone_sums = filtered[['Red Zone', 'Blue Zone', 'Green Zone', 'Orange Zone']].sum()
    
    fig = px.pie(
        names=zone_sums.index,
        values=zone_sums.values,
        hole=0.55,
        color=zone_sums.index,
        color_discrete_map={
            'Red Zone': '#f43f5e',
            'Orange Zone': '#f59e0b',
            'Blue Zone': '#3b82f6',
            'Green Zone': '#10b981'
        }
    )
    
    title_suffix = "All India" if state == 'All' else STATE_MAP.get(state, state)
    fig = apply_dark_theme(fig, f"Zoning Distribution ({title_suffix})")
    fig.update_layout(showlegend=False)
    fig.update_traces(textinfo='percent+label', textfont_size=10, hole=0.55)
    return fig

@app.callback(
    Output('resource-chart', 'figure'),
    [Input('state-selector', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_resource_chart(state, start_date, end_date):
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    filtered = df[(df['parsed_date'] >= start_dt) & (df['parsed_date'] <= end_dt)]
    
    if state != 'All':
        state_full_name = STATE_MAP.get(state)
        filtered = filtered[filtered['State'] == state_full_name]
        
    resource_sums = filtered[['Mask', 'Sanitizer', 'Oxygen']].sum()
    
    fig = px.bar(
        x=resource_sums.index,
        y=resource_sums.values,
        color=resource_sums.index,
        color_discrete_map={
            'Mask': '#a855f7',
            'Sanitizer': '#06b6d4',
            'Oxygen': '#f43f5e'
        },
        labels={'x': 'Resource Types', 'y': 'Total Allocation'}
    )
    
    title_suffix = "All India" if state == 'All' else STATE_MAP.get(state, state)
    fig = apply_dark_theme(fig, f"Resource Footprint ({title_suffix})")
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output('comparison-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('comparison-metric', 'value')]
)
def update_comparison_chart(start_date, end_date, metric):
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)
    
    filtered = df[(df['parsed_date'] >= start_dt) & (df['parsed_date'] <= end_dt)]
    status_filtered = filtered[filtered['Status'] == metric]
    
    state_sums = []
    for code, name in STATE_MAP.items():
        if code == 'UN': continue
        total = status_filtered[code].sum()
        state_sums.append({'State': name, 'Count': total})
        
    comp_df = pd.DataFrame(state_sums).sort_values(by='Count', ascending=True)
    
    # Select top 15 states to keep the bar chart neat and scannable
    comp_df = comp_df.tail(15)
    
    fig = px.bar(
        comp_df,
        y='State',
        x='Count',
        orientation='h',
        color='Count',
        color_continuous_scale='viridis',
        labels={'Count': 'Count', 'State': 'State'}
    )
    
    fig = apply_dark_theme(fig, f"Top States by {metric} Cases")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(margin=dict(t=70, r=20, l=120, b=40))
    return fig

if __name__ == '__main__':
    app.run(debug=True)
