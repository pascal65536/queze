from openpyxl import Workbook
from openpyxl.drawing.image import Image


wb = Workbook()
ws = wb.active
ws['A1'] = 'You should see three logos below'
img = Image('logo.png')
ws.add_image(img, 'A1')
wb.save('logo.xlsx')
