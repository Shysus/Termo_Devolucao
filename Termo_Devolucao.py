import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# Classe para criar o PDF
class PDF(FPDF):
    def __init__(self, orientation='L', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
    
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Milton Barbosa EPP - 06941034000167', 0, 1, 'C')
        self.ln(10)  # Adiciona uma linha em branco para espaçamento

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def add_serials_table(self, seriais, modelos):
        # Ajuste a largura da coluna 'Serial' com base no maior serial
        width_col_serial = max([self.get_string_width(s) for s in seriais]) + 10
        # Ajuste a largura da coluna 'Modelo' com base no maior modelo
        width_col_modelo = max([self.get_string_width(m) for m in modelos.values() if m != 'Não encontrado Modelo']) + 10
        self.set_font('Arial', 'B', 12)
        self.cell(width_col_serial, 10, 'Serial', 1, 0, 'C')
        self.cell(width_col_modelo, 10, 'Modelo', 1, 1, 'C')
        self.set_font('Arial', '', 12)
        for serial in seriais:
            modelo = modelos.get(serial, 'Não encontrado Modelo')
            self.cell(width_col_serial, 10, serial, 1, 0, 'C')
            self.cell(width_col_modelo, 10, modelo, 1, 1, 'C')

# Função para gerar o PDF
def gerar_pdf(nome_tecnico, seriais, modelos):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Termo de Devolução', 0, 1, 'C')
    pdf.ln(20)

    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, f'Nome do Técnico: {nome_tecnico}', 0, 1)
    pdf.cell(0, 10, f'Data e Hora: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1)
    pdf.ln(10)

    pdf.add_serials_table(seriais, modelos)

    pdf.ln(20)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Assinatura do Técnico:', 0, 1)
    pdf.cell(90, 10, '', 'B', 1)  # Campo para assinatura

    return pdf.output(dest='S').encode('latin-1')

# Função para ler a planilha
def ler_planilha(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                st.error('Formato de arquivo não suportado.')
                return None
            return df
        except Exception as e:
            st.error(f'Ocorreu um erro ao ler o arquivo: {e}')
            return None
    return None

# Interface Streamlit
st.title('Sistema de Devolução de Equipamentos')

# Lista de nomes para a caixa de seleção
nomes_tecnicos = [
    "ALEXANDRE AGNALDO RAMOS",
    "ALEXANDRE GRANJEIRO VENTURA",
    "GUILHERME DUARTE BARBOSA",
    "JOSE CARLOS DA SILVA JUNIOR",
    "LUIZ FELIPE BALBUENA ARIA",
    "SAMUEL JUNIOR DE LIMA SCHNEIDER",
    "WELLYNGTON GABRIEL MARTINES PERES",
    "JEFFERSON BARBOSA DE CARVALHO",
    "THIAGO CARVALHO DE SOUSA",
    "EMERSON DE LIMA COUTRIM",
    "GUILHERME MATOS ZANDONA",
    "JOAO VITOR DA SILVA OLIVEIRA",
    "MAICON JUNIOR CORDEIRO DE CARVALHO",
    "NAYSON GUSTAVO DE OLIVEIRA BARBOSA",
    "WILSON JUNIOR ANTUNES DA SILVA",
    "DANIEL ANTUNES SANCHES",
    "ELIMAR SOUZA GODOY",
    "LUIS HENRIQUE ALFONZO GAYOSO"
]

nome_tecnico = st.selectbox('Selecione o Nome do Técnico', nomes_tecnicos)
uploaded_file = st.file_uploader("Faça upload da planilha de equipamentos", type=['csv', 'xlsx', 'xls'])

df = ler_planilha(uploaded_file)
if df is not None:
    modelos = pd.Series(df['Modelo'].values, index=df['Endereçável Principal']).to_dict()
else:
    modelos = {}

seriais = st.text_area('Seriais dos Equipamentos (separe por linha)')
seriais = seriais.split('\n')  # Divide os seriais em uma lista

if st.button('Gerar Termo de Devolução'):
    pdf = gerar_pdf(nome_tecnico, seriais, modelos)
    st.download_button('Baixar PDF', data=pdf, file_name='termo_devolucao.pdf')
