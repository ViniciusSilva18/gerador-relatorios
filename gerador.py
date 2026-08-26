"""Gerador de relatórios PDF profissionais a partir de dados CSV."""
import pandas as pd, matplotlib.pyplot as plt, matplotlib
matplotlib.use('Agg')
from fpdf import FPDF
from datetime import datetime
from io import BytesIO
import os

def gerar_demo_csv(path='dados.csv'):
    meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago']
    data = {'Mes':meses,'Receita':[3200,3800,3200,4100,3800,4320,4100,4320],'Despesa':[1800,2100,1750,2300,1900,2050,1800,1893],'Clientes':[12,15,11,18,14,16,15,17]}
    pd.DataFrame(data).to_csv(path, index=False)
    return path

def gerar_grafico(df):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.patch.set_facecolor('#090d16')
    for ax in [ax1, ax2]:
        ax.set_facecolor('#0f172a')
        ax.spines['bottom'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='#94a3b8')
    ax1.bar(df['Mes'], df['Receita'], color='#10b981', alpha=0.8, label='Receita')
    ax1.bar(df['Mes'], df['Despesa'], color='#f43f5e', alpha=0.8, label='Despesa')
    ax1.set_title('Receita vs Despesa', color='#f1f5f9', pad=10)
    ax1.legend(facecolor='#0f172a', labelcolor='#94a3b8')
    lucro = df['Receita'] - df['Despesa']
    ax2.plot(df['Mes'], lucro, color='#06b6d4', linewidth=2, marker='o')
    ax2.fill_between(range(len(df)), lucro, alpha=0.15, color='#06b6d4')
    ax2.set_title('Lucro Líquido', color='#f1f5f9', pad=10)
    ax2.set_xticks(range(len(df)))
    ax2.set_xticklabels(df['Mes'])
    plt.tight_layout()
    plt.savefig('chart.png', dpi=150, bbox_inches='tight', facecolor='#090d16')
    plt.close()
    return 'chart.png'

def gerar_pdf(df, chart_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(9, 13, 22)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(6, 182, 212)
    pdf.cell(0, 20, 'RELATÓRIO FINANCEIRO', align='C', ln=True)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 8, f'Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")}', align='C', ln=True)
    pdf.ln(8)
    total_r = df['Receita'].sum()
    total_d = df['Despesa'].sum()
    lucro_t = total_r - total_d
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(241, 245, 249)
    pdf.cell(0, 10, 'Resumo Executivo', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(60, 8, f'Total Receita: EUR {total_r:,.0f}', ln=False)
    pdf.set_text_color(244, 63, 94)
    pdf.cell(60, 8, f'Total Despesa: EUR {total_d:,.0f}', ln=False)
    pdf.set_text_color(6, 182, 212)
    pdf.cell(60, 8, f'Lucro Total: EUR {lucro_t:,.0f}', ln=True)
    pdf.ln(4)
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=10, y=None, w=190)
    pdf.output('relatorio.pdf')
    return 'relatorio.pdf'

if __name__ == '__main__':
    print('📄 VibePDF — Gerador de Relatórios')
    csv_path = gerar_demo_csv()
    df = pd.read_csv(csv_path)
    print('📊 A gerar gráficos...')
    chart = gerar_grafico(df)
    print('📄 A gerar PDF...')
    pdf = gerar_pdf(df, chart)
    print(f'✅ Relatório gerado: {pdf}')
