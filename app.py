from dash import Dash, dcc, html, Input, Output
import plotly
import plotly.graph_objects as go
import pandas as pd
import numpy as np

theses = pd.read_csv("THESES-TOTAL.csv")

theses.head(5)

maitrises = theses.query("type == 'maîtrise'")

medianesMaitrisesUniv = maitrises.groupby("universite")["nbPages"].median().sort_values(ascending=False)
medianesMaitrisesUniv

medianesMaitrisesDiscipline = maitrises.groupby("discipline")["nbPages"].median().sort_values(ascending=False)
medianesMaitrisesDiscipline

# Manually update the values in the grandeDiscipline column
theses['grandeDiscipline'] = theses['grandeDiscipline'].str.replace('1. Sciences exactes et naturelles', 'Sciences exactes et naturelles')
theses['grandeDiscipline'] = theses['grandeDiscipline'].str.replace("2. Sciences de l'ingénieur et technologiques", "Sciences de l'ingénieur et technologiques")
theses['grandeDiscipline'] = theses['grandeDiscipline'].str.replace('3. Sciences médicales et sanitaires', 'Sciences médicales et sanitaires')
theses['grandeDiscipline'] = theses['grandeDiscipline'].str.replace('4. Sciences agricoles', 'Sciences agricoles')
theses['grandeDiscipline'] = theses['grandeDiscipline'].str.replace('5. Sciences sociales', 'Sciences sociales')
theses['grandeDiscipline'] = theses['grandeDiscipline'].str.replace('6. Sciences humaines', 'Sciences humaines')
theses['grandeDiscipline'] = theses['grandeDiscipline'].str.replace('7. Programme personnalisé', 'Programme personnalisé')

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("A Brief View of Page Numbers by Discipline and University"),
    html.P("Select a type:"),
    dcc.Checklist(
        id='type-checklist', 
        options=[
            {'label': 'Maîtrise', 'value': 'maîtrise'},
            {'label': 'Doctorat', 'value': 'doctorat'}
        ],
        value=['doctorat'],
        inline=True
    ),
    html.Div([
        html.Div([
            dcc.Graph(id="box-plot-graph-university"),
        ], className='six columns', style={'padding': '0 5px'}),  # Reduced padding or margin here

        html.Div([
            html.P("Select a grande discipline:"),
            dcc.Dropdown(
                id='grande-discipline-dropdown',
                options=[{'label': 'All Disciplines', 'value': 'All'}] +
                        [{'label': gd, 'value': gd} for gd in theses['grandeDiscipline'].unique()],
                value='All'
            ),
            dcc.Graph(id="box-plot-graph-discipline"),
        ], className='six columns', style={'padding': '0 -25px'}),  # Reduced padding or margin here
    ], className='row', style={'margin': '0 -20px'}),  # Adjusted margin here to offset padding
],style={'maxWidth': '1200px', 'margin': '0 auto'})  # You can adjust maxWidth to fit the size you want




@app.callback(
    Output("box-plot-graph-university", "figure"), 
    [Input("type-checklist", "value")]
)
def update_box_plot_by_university(selected_type):
    # Filter data based on selected type
    filtered_df = theses[theses['type'].isin(selected_type)]

    # Calculate median nbPages for each university
    universite_medians = filtered_df.groupby('universite')['nbPages'].median().sort_values(ascending=True)
    
    # Define the base color in HSL for the gradient
    base_hue = 240  # Modify as needed for the correct color
    base_saturation = 100
    min_lightness = 10
    max_lightness = 30
    
    # Generate an array of colors for the gradient
    colors = [f'hsl({base_hue}, {base_saturation}%, {l}%)' for l in np.linspace(max_lightness, min_lightness, len(universite_medians))]
    
    # Create the box plot data, sorted by median nbPages
    data1 = [
        go.Box(
            x=filtered_df[filtered_df['universite'] == universite]['nbPages'],
            name=universite,
            marker_color=colors[i],
            showlegend=False
        )
        for i, universite in enumerate(universite_medians.index)
    ]
    
    # Create the figure with the data
    fig1 = go.Figure(data=data1)
    
    # Format the layout
    fig1.update_layout(
        yaxis=dict(
            categoryorder='array',
            categoryarray=universite_medians.index,
            title="Université"
        ),
        xaxis=dict(title="Distribution du nombre de pages", zeroline=False, gridcolor='white'),
        plot_bgcolor='lightblue',
        font=dict(size=12),
        height=1500)

    # Apply the same styling as before for x-axis
    fig1.update_xaxes(range=[0, 650], showgrid=True, gridwidth=1, gridcolor='white')

    return fig1

@app.callback(
    Output("box-plot-graph-discipline", "figure"), 
    [Input("type-checklist", "value"),
     Input("grande-discipline-dropdown", "value")]
)
def update_box_plot_by_discipline(selected_type, selected_grande_discipline):
    # Filter data based on selected type and grandeDiscipline
    if selected_grande_discipline == 'All':
        filtered_df = theses[theses['type'].isin(selected_type)]
    else:
        filtered_df = theses[(theses['type'].isin(selected_type)) & (theses['grandeDiscipline'] == selected_grande_discipline)]

    # Calculate median nbPages for each discipline
    discipline_medians = filtered_df.groupby('discipline')['nbPages'].median().sort_values(ascending=True)
    
    # Define the base color in HSL for the gradient
    base_hue = 82  # Modify as needed for the correct color
    base_saturation = 100
    min_lightness = 10
    max_lightness = 30
    
    # Generate an array of colors for the gradient
    colors = [f'hsl({base_hue}, {base_saturation}%, {l}%)' for l in np.linspace(max_lightness, min_lightness, len(discipline_medians))]
    
    # Create the box plot data, sorted by median nbPages
    data = [
        go.Box(
            x=filtered_df[filtered_df['discipline'] == discipline]['nbPages'],
            name=discipline,
            marker_color=colors[i],
            showlegend=False
        )
        for i, discipline in enumerate(discipline_medians.index)
    ]
    
    # Create the figure with the data
    fig = go.Figure(data=data)
    
    # Format the layout
    fig.update_layout(
        yaxis=dict(
            categoryorder='array',
            categoryarray=discipline_medians.index,
            title="Discipline"
        ),
        xaxis=dict(title="Distribution du nombre de pages", zeroline=False, gridcolor='white'),
        plot_bgcolor='khaki',
        font=dict(size=12),
        height=1500
    )
    
    # Apply the same styling as before for x-axis
    fig.update_xaxes(range=[0, 800], showgrid=True, gridwidth=1, gridcolor='white')
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)