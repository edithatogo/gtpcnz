from pathlib import Path
import pandas as pd
from artifact_tool import Workbook, SpreadsheetFile

ROOT=Path(__file__).resolve().parents[1]
OUTPUTS=ROOT/'outputs'
TEMPLATES=ROOT/'data/templates'
xlsx_path=OUTPUTS/'mcda-workbook-v0.9.0.xlsx'
wb=Workbook.create()

def clean_matrix(df):
    data=[list(df.columns)]
    for row in df.itertuples(index=False, name=None):
        vals=[]
        for v in row:
            if pd.isna(v): vals.append('')
            elif isinstance(v,(str,int,float,bool)): vals.append(v)
            else: vals.append(str(v))
        data.append(vals)
    return data

def add_sheet(name, df, width=28):
    sh=wb.worksheets.add(name)
    data=clean_matrix(df)
    rows=len(data); cols=len(data[0]) if rows else 1
    sh.get_range_by_indexes(0,0,rows,cols).values=data
    header=sh.get_range_by_indexes(0,0,1,cols)
    header.format={"fill":"#1F4E79","font":{"bold":True,"color":"#FFFFFF"},"horizontal_alignment":"center","vertical_alignment":"center","wrap_text":True}
    if rows>1:
        sh.get_range_by_indexes(1,0,rows-1,cols).format.wrap_text=True
    sh.get_range_by_indexes(0,0,rows,cols).format.autofit_columns()
    for c in range(cols):
        sh.get_range_by_indexes(0,c,rows,1).format.column_width = width if c in [1,2,3] else min(width,16)
    try: sh.freeze_panes.freeze_rows(1)
    except Exception: pass
    return sh

# Dashboard
sh=wb.worksheets.add('Dashboard')
sh.get_range('A1').values=[['Game-informed MCDA decision-support layer v0.9.0']]
sh.get_range('A1:F1').format={"font":{"bold":True,"color":"#FFFFFF","size":14},"fill":"#1F4E79","horizontal_alignment":"left"}
sh.get_range('A3:B4').values=[['Status','Demonstrative, deliberative MCDA; not empirically calibrated'],['Core line','Demand-driven within rules; not demand-driven without rules.']]
sh.get_range('A3:A4').format={"font":{"bold":True},"fill":"#D9EAF7"}
top=pd.read_csv(OUTPUTS/'mcda-example-results-v0.9.0.csv')[['rank','option_id','option','weighted_total_before_penalty','risk_penalty','risk_adjusted_score']]
data=clean_matrix(top)
sh.get_range_by_indexes(6,0,len(data),len(data[0])).values=data
sh.get_range_by_indexes(6,0,1,len(data[0])).format={"fill":"#1F4E79","font":{"bold":True,"color":"#FFFFFF"},"wrap_text":True}
sh.get_range_by_indexes(7,0,len(data)-1,len(data[0])).format.wrap_text=True
for col,width in [('A',10),('B',12),('C',42),('D',18),('E',12),('F',18)]:
    sh.get_range(f'{col}1:{col}20').format.column_width=width
try: sh.get_range('F8:F17').conditional_formats.add_data_bar({"gradient":True})
except Exception: pass
try: sh.freeze_panes.freeze_rows(6)
except Exception: pass

add_sheet('Criteria', pd.read_csv(OUTPUTS/'mcda-criteria-v0.9.0.csv'), 34)
add_sheet('Policy Options', pd.read_csv(OUTPUTS/'mcda-policy-options-v0.9.0.csv'), 38)
add_sheet('Scorecard', pd.read_csv(OUTPUTS/'mcda-policy-option-scorecard-v0.9.0.csv'), 38)
add_sheet('Results', pd.read_csv(OUTPUTS/'mcda-example-results-v0.9.0.csv'), 30)
add_sheet('Weight Sensitivity', pd.read_csv(OUTPUTS/'mcda-weight-sensitivity-v0.9.0.csv'), 30)
add_sheet('Game Positions', pd.read_csv(OUTPUTS/'mcda-game-position-example-v0.9.0.csv'), 38)
add_sheet('Weight Sets', pd.read_csv(OUTPUTS/'mcda-weight-sets-v0.9.0.csv'), 30)
add_sheet('Option Template', pd.read_csv(TEMPLATES/'policy-option-mcda-template-v0.9.0.csv'), 38)
add_sheet('Game Template', pd.read_csv(TEMPLATES/'game-position-scoring-template-v0.9.0.csv'), 38)

check=wb.inspect({"kind":"table","range":"Dashboard!A1:F18","include":"values,formulas","table_max_rows":18,"table_max_cols":6})
print(check.ndjson[:1200])
errors=wb.inspect({"kind":"match","search_term":"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A","options":{"use_regex":True,"max_results":100},"summary":"formula error scan"})
print(errors.ndjson[:1000])
blob=wb.render({"sheet_name":"Dashboard","range":"A1:F18","scale":1})
blob.save(str(OUTPUTS/'mcda-workbook-dashboard-preview-v0.9.0.png'))
SpreadsheetFile.export_xlsx(wb).save(str(xlsx_path))
print('saved', xlsx_path, xlsx_path.stat().st_size)
