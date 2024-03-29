# %% Imports
import numpy as np
import streamlit as st
from itertools import cycle
import pandas as pd
from io import BytesIO
import json
import random

# %% Params
import data.farm.params as fp
farmMaterials, farmStats, numColsPriceTab = fp.loadParams()

# %% Inputs (setting default)
import data.farm.inputs as fi
farmQuantities = fi.loadInputs()

if 'materialPrices' not in st.session_state:
    import data.inputs as di
    materialsPrices = di.loadInputs()
    st.session_state['materialPrices'] = materialsPrices
else:
    materialsPrices = st.session_state['materialPrices']

# %% Functions
def computeTotalCost(farmStats, farmQuantities):
    for mat in farmStats:
        farmStats = {**farmStats, mat:{**farmStats[mat], 'totalCost':farmStats[mat]['cost']*farmQuantities[mat]}}
    return farmStats

def computeProfit(farmStats, materialsPrices, farmQuantities):
    productsProfits = {}
    for mat in farmStats:
        productsProfits = {**productsProfits, mat:{'profitWorst':(farmStats[mat]['worst']*farmStats[mat]['collect']*materialsPrices[mat]*farmQuantities[mat]- farmStats[mat]['totalCost']),
                                                  'profitBest':(farmStats[mat]['best']*farmStats[mat]['collect']*materialsPrices[mat]*farmQuantities[mat] - farmStats[mat]['totalCost'])}}
    return productsProfits

def splitOutput(farmStats, productsProfits):
    materialCollect = {mat:farmStats[mat]['collect'] for mat in farmStats}
    materialWorst = {mat:farmStats[mat]['worst'] for mat in farmStats}
    materialBest = {mat:farmStats[mat]['best'] for mat in farmStats}
    materialCost = {mat:farmStats[mat]['cost'] for mat in farmStats}
    materialTotalCost = {mat:farmStats[mat]['totalCost'] for mat in farmStats}
    materialProfitWorst = {mat:productsProfits[mat]['profitWorst'] for mat in farmStats}
    materialProfitBest = {mat:productsProfits[mat]['profitBest'] for mat in farmStats}
    return materialCollect, materialWorst, materialBest, materialCost, materialTotalCost, materialProfitWorst, materialProfitBest

def createDataFrame(farmStats, materialsPrices, farmQuantities):
    farmStats = computeTotalCost(farmStats=farmStats, farmQuantities=farmQuantities)
    productsProfits = computeProfit(farmStats, materialsPrices, farmQuantities)
    materialCollect, materialWorst, materialBest, materialCost, materialTotalCost, materialProfitWorst, materialProfitBest = splitOutput(farmStats, productsProfits)
    df = pd.DataFrame({'Coletas (x vezes)': materialCollect,
                       'Pior cenário': materialWorst,
                       'Melhor cenário': materialBest,
                       'Custo de plantação': materialCost,
                       'Quantidade': farmQuantities,
                       'Custo Total': materialTotalCost,
                       'Lucro Pior Cenário':materialProfitWorst,
                       'Lucro Melhor Cenário':materialProfitBest})
    return df

def onChangeDataFrame():
    df = st.session_state['farmDf']
    st.write(df)
    for mat in df.index:
        farmQuantities[mat] = df.loc[mat,'Quantidade']
    st.session_state['farmDf'] = createDataFrame(farmStats=farmStats, materialsPrices=materialsPrices, farmQuantities=farmQuantities)
    

# %% Page Header
st.set_page_config(layout='wide')
st.markdown("""
<style>
.small-font {
    font-size:15px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('# RavenStats <p class="small-font">(Feito por Vish. Ravendawn nick (Angerhorn): Vish Tankao)</p>', unsafe_allow_html=True)

cols = st.columns(4)

with cols[0]:
    if st.button(":house: Home"):
        st.switch_page("app.py")
with cols[1]:
    if st.button(":package: Tradepacks"):
        st.switch_page("pages/tradepack.py")
with cols[2]:
    if st.button(":female-farmer: Fazenda"):
        st.switch_page("pages/farm.py")
with cols[3]:
    if st.button(":hammer_and_wrench: Crafting"):
        st.switch_page("pages/crafting.py")

# %% Page Body
st.markdown('# Calculadora de Cultivo')
st.write('Atualize a quantidade de pés na própria tabela e o preço em sua respectiva aba. Manual para salvar os dados [aqui](https://github.com/gcastro-vish/tradepack-calculator/tree/main?tab=readme-ov-file#como-salvar-os-dados) e manual para inclusão de dados [aqui](https://github.com/gcastro-vish/tradepack-calculator/tree/main?tab=readme-ov-file#como-incluir-novos-dados)')
st.write('Utilize o botão lateral para atualizar a tabela: :red[dê 2 cliques para atualizar, funciona meio esquisito, mas funciona :skull:]')
with st.sidebar:
    # bonusPerCent = st.number_input(label='Bonus Gather (%) - ainda nao funciona',min_value=0)
    uploadedMaterialPrices = st.file_uploader(':arrow_up_small: Upload Preços',
                                            type='xlsx')    

tabs = st.tabs(['Lucros', 'Preços'])

with tabs[1]:
    if uploadedMaterialPrices is not None:
        dfaux = pd.read_excel(uploadedMaterialPrices,index_col=0)
        materialsPrices = dfaux.to_dict()['valor']
    cols = st.columns(numColsPriceTab)
    for mat, col in zip(farmMaterials,cycle(np.arange(0,numColsPriceTab))):
        materialsPrices = {**materialsPrices, mat:cols[col].number_input(label=mat,min_value=20,value=materialsPrices[mat])}
        st.session_state['materialPrices'] = materialsPrices
    bufferMaterialPrices = BytesIO()
    with pd.ExcelWriter(bufferMaterialPrices, engine='xlsxwriter') as writer:
        pd.DataFrame({'valor':materialsPrices}).to_excel(writer, sheet_name='Preços')
        
    with st.sidebar:
        st.download_button(':small_red_triangle_down: Download Preços',
                        bufferMaterialPrices,
                        file_name='precos.xlsx',
                        mime='application/vnd.ms-excel')

with tabs[0]:
    if 'farmDf' not in st.session_state:
        st.session_state['farmDf'] = createDataFrame(farmStats, materialsPrices, farmQuantities)

    editedDf = st.data_editor(st.session_state['farmDf'],
                column_config={
                            'Coletas (x vezes)':None,
                            'Coletas (x vezes)': None,
                            'Pior cenário': None,
                            'Melhor cenário': None,
                            'Custo de plantação': None,
                            'Quantidade':st.column_config.Column(
                                'Quantidade',
                                help = 'Número de pés referentes a esse cultivo'
                        ),
                            'Custo Total':st.column_config.ProgressColumn(
                                'Custo Total',
                                format = '$%d',
                                min_value = int(st.session_state['farmDf']['Custo Total'].min()),
                                max_value = int(st.session_state['farmDf']['Custo Total'].max()),
                        ),
                            'Lucro Pior Cenário':st.column_config.ProgressColumn(
                                'Lucro Pior Cenário',
                                help = 'Lucro Pior Cenário',
                                format = '$%d',
                                min_value = int(st.session_state['farmDf']['Lucro Pior Cenário'].min()),
                                max_value = int(st.session_state['farmDf']['Lucro Pior Cenário'].max()),
                        ),
                            'Lucro Melhor Cenário':st.column_config.ProgressColumn(
                                'Lucro Melhor Cenário',
                                help = 'Lucro Melhor Cenário',
                                format = '$%d',
                                min_value = int(st.session_state['farmDf']['Lucro Melhor Cenário'].min()),
                                max_value = int(st.session_state['farmDf']['Lucro Melhor Cenário'].max()),
                        ),
                        },
                        # on_change=onChangeDataFrame,
                        use_container_width=True)
    with st.sidebar:
        if st.button(''':arrows_clockwise: :green[Atualizar Tabela de Lucros]'''):
            st.session_state['farmDf'] = editedDf
            onChangeDataFrame()
            st.rerun()